# coding:utf-8

from django.contrib.auth.models import Permission
from rest_framework import serializers
from hades.models import *
from models import *


###固定资产树

class IdcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idc


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineCompany


class MachineStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineStatus


# class MachineSystemSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = MachineSystem


class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk


class SoftwareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Software

        # person = serializers.SlugRelatedField(
        #         read_only=True,
        #         slug_field='username'
        # )


class CMDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cmdb


class NetAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetAddress


class PhysicalMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMachine
        # fields = ['mac_user','sn']

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('idc', 'status')

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'idc',
                # 'net',
                # 'cmdb',
                'status',
                # 'project',
                # 'm_user'
        )

        return queryset


###APP树

class ProjectConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projectconfig


class AppProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project

    config = ProjectConfigSerializer(read_only=True, many=True)


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App

    project = AppProjectSerializer(read_only=True, many=True)


class ProductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Production

    app = AppSerializer(read_only=True, many=True)


'''
class ContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContainerBase
'''


# class ApplicationSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Application

# class MachineSystemSerializerList(serializers.ModelSerializer):
#    architecture = serializers.ChoiceField(choices=ARCH_CHOICES)
#    class Meta:
#        model = MachineSystem

class ProjectConfigSerializer4M(serializers.ModelSerializer):
    # deploy_type = serializers.ChoiceField(choices=TYPE_STATUS)
    env = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )
    project = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )

    class Meta:
        model = Projectconfig

    def setup_eager_loading(cls, queryset):
        """ Perform necessary eager loading of data. """
        queryset = queryset.prefetch_related('env', 'project').only('project__name', 'env__name')
        return queryset


class PhysicalMachineSerializerList(serializers.ModelSerializer):
    # vendor = serializers.SlugRelatedField(
    #     read_only=True,
    #     slug_field='name'
    # )
    idc = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )
    status = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )
    net = NetAddressSerializer(read_only=True, many=True)
    # project = ProjectConfigSerializer4M(read_only=True, many=True)
    # project = serializers.SlugRelatedField(
    #    many=True,
    #    read_only=True,
    #    slug_field='name'
    # )
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    change_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    cmdb = CMDBSerializer(read_only=True)

    class Meta:
        model = PhysicalMachine

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('idc', 'status')

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'idc',
                'net',
                'project__project',
                'cmdb',
                'status',
                'project',
                'm_user'
        )

        return queryset


class CMDBSerializerList(serializers.ModelSerializer):
    machine = PhysicalMachineSerializerList(read_only=True)

    class Meta:
        model = Cmdb


class ProjectConfigSerializerList(serializers.ModelSerializer):
    # deploy_type = serializers.ChoiceField(choices=TYPE_STATUS)
    env = serializers.SlugRelatedField(
            read_only=True,
            slug_field='enname'
    )
    project = AppProjectSerializer
    create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    machine = PhysicalMachineSerializerList(read_only=True, many=True)

    class Meta:
        model = Projectconfig


class AppProjectSerializerList(serializers.ModelSerializer):
    # deploy_type = serializers.ChoiceField(choices=TYPE_STATUS)
    # create_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    # update_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    # machine = PhysicalMachineSerializerList(read_only=True, many=True)
    # config = ProjectConfigSerializerList(read_only=True, many=True)

    class Meta:
        model = Project
        # exclude = ['name','enname']
        # fields = ['name','enname', 'machine',]


class AppSerializerList(serializers.ModelSerializer):
    project = AppProjectSerializerList(read_only=True, many=True)

    class Meta:
        model = App


class ProductionSerializerList(serializers.ModelSerializer):
    app = AppSerializerList(read_only=True, many=True)

    class Meta:
        model = Production


##自定义API选项部分
##APP组特殊需求专用。
class AppProjectSerializerAll(serializers.ModelSerializer):
    config = ProjectConfigSerializerList(read_only=True, many=True)

    class Meta:
        model = Project
        # exclude = ['name','enname']
        # fields = ['id', 'name', 'enname']


class AppSerializerAll(serializers.ModelSerializer):
    project = AppProjectSerializerAll(read_only=True, many=True)

    class Meta:
        model = App


class ProductionSerializerAll(serializers.ModelSerializer):
    app = AppSerializerAll(read_only=True, many=True)

    class Meta:
        model = Production


##APP属性结构专用
class AppProjectSerializerMenu(serializers.ModelSerializer):
    class Meta:
        model = Project
        # exclude = ['name','enname']
        fields = ['id', 'name', 'enname']


class AppSerializerMenu(serializers.ModelSerializer):
    project = AppProjectSerializerMenu(read_only=True, many=True)

    class Meta:
        model = App


class ProductionSerializerMenu(serializers.ModelSerializer):
    app = AppSerializerMenu(read_only=True, many=True)

    class Meta:
        model = Production


class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission


class UserInfoSerializer(serializers.ModelSerializer):
    user_permissions = UserPermissionsSerializer(read_only=True, many=True)
    date_joined = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    last_login = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    # userprofile = UserProfileSerializer(read_only=True)
    class Meta:
        model = User


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Userprofile


class LogsSerializer(serializers.ModelSerializer):
    # user = UserInfoSerializer(read_only=True)
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='username'
    )
    time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Logs


'''
class ContainerSerializerList(serializers.ModelSerializer):

    software = SoftwareSerializer(read_only=True)
    project = AppProjectSerializerList(read_only=True)
    machine = PhysicalMachineSerializerList(read_only=True)
    create_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d")
    update_time = serializers.DateTimeField(read_only=True,format="%Y-%m-%d")

    class Meta:
        model = ContainerBase
'''

"""asdfasdf"""

"""API测试"""


class ProjectConfigSerializerAsset(serializers.ModelSerializer):
    class Meta:
        model = Projectconfig
        fields = ['project']

    project = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )


class PhysicalMachineSerializerAsset(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMachine
        fields = ['id', 'idc', 'status', 'net', 'project', 'cmdb', 'sn', 'cpu_n', 'mem_total_size', 'drac_ip',
                  'asset_number', 'comment']

    idc = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )
    status = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )
    cmdb = serializers.SlugRelatedField(
            read_only=True,
            slug_field='system_name'
    )
    net = serializers.SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='ip_address'
    )
    # project = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='project__name'
    #  )
    project = ProjectConfigSerializerAsset(read_only=True, many=True)

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('idc', 'status')

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'idc',
                'net',
                'project__project',
                'cmdb',
                'status',
                'project',
                'm_user'
        )

        return queryset


class PhysicalMachineSerializerAllIPList(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMachine
        fields = ['id', 'net', 'sn', 'idc']

    net = serializers.SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='ip_address'
    )
    idc = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('idc', 'status')

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'idc',
                'net',
                'project__project',
                'cmdb',
                'status',
                'project',
                'm_user'
        )

        return queryset


class ProjectConfigSerializerforPhysical(serializers.ModelSerializer):
    class Meta:
        model = Projectconfig
        fields = ['project']

    project = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )


class PhysicalMachineSerializerIndex(serializers.ModelSerializer):
    class Meta:
        model = PhysicalMachine
        fields = ['id', 'net', 'sn', 'idc', 'project', 'cmdb']

    cmdb = serializers.SlugRelatedField(
            read_only=True,
            slug_field='hostname'
    )

    # project = ProjectConfigSerializerforPhysical()
    project = ProjectConfigSerializerforPhysical(many=True)

    net = serializers.SlugRelatedField(
            many=True,
            read_only=True,
            slug_field='ip_address'
    )
    idc = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related('idc', 'status')

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'idc',
                'net',
                'project__project',
                'cmdb',
                'status',
                'project',
                'm_user',
        )

        return queryset


class UserProfileSerializerAllList(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
            read_only=True,
            slug_field='id'
    )

    # user = UserInfoSerializer()
    class Meta:
        model = Userprofile
        fields = ['user', 'email', 'name']


class EnvironmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Environment
        # fields = ['id', 'name', 'enname']


MONITOR_STATUS = (
    (1, '正常'),
    (2, '告警'),
    (3, '关闭'),
    (4, '未知'),
)

WORK_TYPE_STATUS = (
    (1, 'GET'),
    (2, 'POST'),
)


class MonitorSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        exclude = ['project']

    idc = serializers.SlugRelatedField(
            read_only=True,
            slug_field='name'
    )

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """
        # select_related for "to-one" relationships
        queryset = queryset.select_related(
                'project__project__name',
                'idc'
        )

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'project__project',
                'project__project__api',
                'monitoruser'
        )

        return queryset


class MonitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitor
        # fields = ['id', 'name', 'enname']
        # exlude = []

    # project = serializers.StringRelatedField()
    # idc = serializers.StringRelatedField()

    @staticmethod
    def setup_eager_loading(queryset):
        """ Perform necessary eager loading of data. """

        # prefetch_related for "to-many" relationships
        queryset = queryset.prefetch_related(
                'project__project',
                'monitoruser'
        )

        # select_related for "to-one" relationships
        # queryset = queryset.select_related(
        #         'project__project__name'
        # )

        return queryset


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department


        # @staticmethod
        # def setup_eager_loading(queryset):
        #     """ Perform necessary eager loading of data. """
        #     # select_related for "to-one" relationships
        #     queryset = queryset.select_related('project')
        #
        #     # prefetch_related for "to-many" relationships
        #     queryset = queryset.prefetch_related(
        #         'project',
        #         'project__project',
        #         'project__project__app',
        #         'project__project__app__production'
        #     )
        #
        #     return queryset
