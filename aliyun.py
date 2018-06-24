# coding: utf-8
__author__ = 'machao'

import json

from hades.views import my_render
from django.http import HttpResponse
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeInstanceAttributeRequest
from django.contrib.auth.decorators import login_required, permission_required
from asset_api.models import PhysicalMachine, Idc, Cmdb
import difflib
from django.db.models import Q
import time


class diff_aliyun_cmdb(object):
    def __init__(self):
        self.ALIYUN_KEY = 'VHh49P2sa6Ab9fcV'
        self.ALIYUN_SECRET_KEY = 'Y5iRE9Idsz6krQNpiCt80ubyD9WtIh'
        # self.ALIYUN_REGIONID = 'cn-beijing'
        self.ALIYUN_FORMAT = 'json'

    def aliyun_connect(self, request, page_size=None, page_number=None, ALIYUN_REGIONID='cn-beijing'):
        """
        阿里云API，连接函数
        :param request:
        :param page_size:
        :param page_number:
        :return:
        """
        clt = client.AcsClient(self.ALIYUN_KEY, self.ALIYUN_SECRET_KEY, ALIYUN_REGIONID)
        request.set_accept_format(self.ALIYUN_FORMAT)
        if page_number:
            request.set_PageNumber(page_number)
        if page_size:
            request.set_PageSize(page_size)
        result = clt.do_action(request)
        return result

    def get_cout(self):
        from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest

        req = DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
        connect = self.aliyun_connect(req)

        ali_count = eval(connect)['TotalCount']

        return ali_count

    def aliyun_list(self):
        """
        获取阿里云主机SN列表
        :return:
        """
        page_size = 100
        page_number = 1
        true = True
        false = False
        all_ali = []


        while 1:
            request = DescribeInstancesRequest.DescribeInstancesRequest()
            connect = self.aliyun_connect(request, page_size, page_number)
            page_number += 1
            req = eval(connect)
            connect = ''

            if req['Instances']['Instance'] != []:
                all_ali += req['Instances']['Instance']
                # tmplist = req['Instances']['Instance']
                # for info in tmplist:
                #     all_ali.append(info['SerialNumber'])
            else:
                break

        return all_ali

    def cmdb_list(self):
        """
        获取CMDB主机SN列表
        :return:
        """
        all_cmdb = []
        cmdb_ali = PhysicalMachine.objects.filter(Q(idc__name='阿里云') & ~Q(status__name='报废'))

        # for info in cmdb_ali.values('sn'):
        #     all_cmdb.append(info['sn'].encode())

        return cmdb_ali

    def diff_in_ali(self):
        """
        阿里云中有，但CMDB中没有的机器
        :return:
        """

        ali_diff = []
        cmdb = []

        ali = self.aliyun_list()
        cmdb_list = self.cmdb_list()

        for info in cmdb_list.values('sn'):
            cmdb.append(info['sn'].encode())

        return [info for info in ali if info['SerialNumber'] not in cmdb]

    def diff_in_cmdb(self):
        """
        CMDB中有，但阿里云中没有的机器
        :return:
        """
        ali_sn = []
        ali = self.aliyun_list()
        cmdb = self.cmdb_list()

        for info in ali:
            ali_sn.append(info['SerialNumber'])

        return [info for info in cmdb if info.sn not in ali_sn]

    def get_aliyun_info(self, InstanceId):
        """
        获取阿里云单机详细信息
        """
        request = DescribeInstanceAttributeRequest.DescribeInstanceAttributeRequest()
        request.set_InstanceId(InstanceId)
        connect = self.aliyun_connect(request)

        return eval(connect)

    def get_instance_type(self):
        """
        获取阿里云类型列表
        """
        from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest

        request = DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
        connect = self.aliyun_connect(request)
        tmp = eval(connect)

        return tmp['InstanceTypes']['InstanceType']

    def get_memory_cpu(self, InstanceTypeName):
        """
        获取CPU内存信息
        """

        instance_types = self.get_instance_type()

        for instanctype in instance_types:
            if instanctype['InstanceTypeId'] == InstanceTypeName:
                return instanctype

    def add_2_cmdb(self, InstanceId, Status):
        """
        增加信息到CMDB中
        """
        ali = self.get_aliyun_info(InstanceId)
        sn = ali['SerialNumber']
        instance_dict = self.get_memory_cpu(ali['InstanceType'])

        try:
            ip = ali['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]
        except:
            ip = ''

        systeminfo = self.get_image_info(ali['ImageId'])
        if not systeminfo['Platform']:
            systeminfo['Platform'] = '未知'

        try:
            machine = PhysicalMachine.objects.get(sn=sn)
        except:
            machine = ''

        if machine:
            """升级"""
            cmdb = Cmdb.objects.filter(machine_id=machine.id).update(
                hostname=ali['HostName'],
                system_arch=systeminfo['Architecture'],
                system_name=systeminfo['Platform'],
                system_version=systeminfo['ImageName']
            )
            # machine.cmdb.hostname = ali['HostName']
            # machine.cmdb.system_arch = systeminfo['Architecture']
            # machine.cmdb.system_name = systeminfo['Platform']
            # machine.cmdb.system_version = systeminfo['ImageName']
            # machine.cmdb.save()

            machine.cpu_n = int(instance_dict['CpuCoreCount'] * 1)
            machine.mem_total_size = int(instance_dict['MemorySize'] * 1024)
            machine.drac_ip = ip
            machine.comment = ali['InstanceName']
            # machine.status_id = Status
            machine.save()
        else:
            """新建"""
            idc = Idc.objects.get(name__startswith='阿里云')
            machine = PhysicalMachine.objects.create(
                idc_id=idc.id,
                sn=ali['SerialNumber'],
                drac_ip=ip,
                status_id=1,
                asset_number=ali['SerialNumber'],
                cpu_n=int(instance_dict['CpuCoreCount'] * 1),
                mem_total_size=int(instance_dict['MemorySize'] * 1024),
                comment=ali['InstanceName']
            )
            cmdb = Cmdb.objects.create(
                hostname=ali['HostName'],
                machine_id=machine.id,
                system_arch=systeminfo['Architecture'],
                system_name=systeminfo['Platform'],
                system_version=systeminfo['ImageName']
            )

        return machine

    def check_2_cmdb(self):
        """
        增加信息到CMDB中
        """
        ali = self.aliyun_list()

        for ecs in ali:
            print ecs['InstanceId']
            self.add_2_cmdb(ecs['InstanceId'], 2)

    def get_vnc_password(self, InstanceId):
        """
        获取VNC链接密码
        :param InstanceId:
        :return:
        """

        from aliyunsdkecs.request.v20140526 import DescribeInstanceVncPasswdRequest

        request = DescribeInstanceVncPasswdRequest.DescribeInstanceVncPasswdRequest()
        request.set_InstanceId(InstanceId)
        connect = self.aliyun_connect(request)
        result = eval(connect)
        return result

    def get_vnc_url(self, InstanceId):
        """
        获取VNC链接
        :param InstanceId:
        :return:
        """

        from aliyunsdkecs.request.v20140526 import DescribeInstanceVncUrlRequest

        request = DescribeInstanceVncUrlRequest.DescribeInstanceVncUrlRequest()
        request.set_InstanceId(InstanceId)
        connect = self.aliyun_connect(request)
        result = eval(connect)
        return result['VncUrl']

    def get_image_list(self, ImageId=None, ImageOwnerAlias=None):
        """
        获取所有镜像列表
        :return:
        """
        from aliyunsdkecs.request.v20140526 import DescribeImagesRequest

        page_size = 100
        page_number = 1
        true = True
        false = False
        all_img = []
        request = DescribeImagesRequest.DescribeImagesRequest()
        if ImageId:
            request.set_ImageId(ImageId)
        if ImageOwnerAlias:
            request.set_ImageOwnerAlias(ImageOwnerAlias)

        while 1:
            connect = self.aliyun_connect(request, page_size, page_number)
            page_number += 1

            req = eval(connect)

            if req.has_key('Images'):
                len(all_img)
                all_img += req['Images']['Image']

        return all_img

    def get_image_info(self, ImageId):
        """
        获取镜像信息
        :return:
        """
        true = True
        false = False
        from aliyunsdkecs.request.v20140526 import DescribeImagesRequest
        typelist = [None, 'marketplace']

        for imagetype in typelist:

            request = DescribeImagesRequest.DescribeImagesRequest()
            request.set_ImageId(ImageId)
            if imagetype:
                request.set_ImageOwnerAlias(imagetype)
            connect = self.aliyun_connect(request)
            req = eval(connect)

            if req.has_key('Images'):
                if req['Images'].has_key('Image'):
                    info = req['Images']['Image']
                    if info:
                        return req['Images']['Image'][0]

        return {"ImageName":ImageId, "Platform":'NoHave', "Architecture":'x86_64'}