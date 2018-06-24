# coding: utf-8

from django.contrib.auth.models import User
from django.db import models


ARCH_CHOICES = (
    ('64', 'x86_64'),
    ('86', 'i386'),
)

TYPE_STATUS = (
    ("1", "开发"),
    ("2", "集测"),
    ("3", "模拟"),
    ("4", "线上"),
)


class Idc(models.Model):
    name = models.CharField('名称', max_length=20, unique=True)
    enname = models.CharField('英文名称', max_length=20, blank=True)
    line = models.CharField('线路类型', max_length=20, blank=True)
    size = models.CharField('容量', max_length=20, blank=True)
    description = models.CharField('描述', max_length=100, blank=True)

    # machine = models.ForeignKey(PhysicalMachine,related_name='idc')

    def __unicode__(self):
        return 'id:%s, name:%s' % (self.id, self.name)


class MachineStatus(models.Model):
    name = models.CharField('状态名称', max_length=20, unique=True)
    enname = models.CharField('英文名称', max_length=20, blank=True)

    def __unicode__(self):
        return 'name:%s' % (self.name)


class MachineCompany(models.Model):
    name = models.CharField('状态名称', max_length=20, unique=True)
    enname = models.CharField('英文名称', max_length=20, blank=True)

    def __unicode__(self):
        return 'id:%s, name:%s' % (self.id, self.name)


# class MachineSystem(models.Model):

#    name = models.CharField('系统名称', max_length=20)
#    version = models.CharField('版本', max_length=20)
#    architecture = models.CharField('架构体系',choices=ARCH_CHOICES, max_length=5)

#    def __unicode__(self):
#        return 'id:%s, name:%s %s %s' %(self.id, self.name, self.version, self.architecture)

class PhysicalMachine(models.Model):
    """
    物理机信息
    """
    idc = models.ForeignKey(Idc, related_name='machine')
    sn = models.CharField('服务器序列号', max_length=50, unique=True)
    vendor = models.CharField('服务器厂商', max_length=100, blank=True, default='')
    # vendor = models.ForeignKey(MachineCompany, related_name='machine')

    machine_model = models.CharField('服务器型号', max_length=30, null=True, blank=True)

    cpu_n = models.IntegerField('cpu总核数', null=True, default=0)
    cpu_details = models.CharField('cpu详细信息', max_length=100, null=True, blank=True)

    mem_total_size = models.IntegerField('内存总容量（MB）', null=True, default=0)
    mem_details = models.CharField('内存详细信息', max_length=100, null=True, blank=True)

    ld_total_size = models.IntegerField('逻辑硬盘总容量（GB）', null=True, default=0)
    ld_details = models.CharField('逻辑硬盘详细信息', max_length=100, null=True, blank=True)
    pd_details = models.CharField('物理硬盘详细信息', max_length=200, null=True, blank=True)
    # RaidCACHE大小
    raid_adptr = models.CharField('raid卡信息', max_length=50, null=True, blank=True)
    raid_cache = models.CharField('raid卡Cache大小', max_length=50, null=True, blank=True)

    # idc = models.CharField('机房代号', max_length=1, default='0', choices=IDC_NAME_CHOICES)
    rack = models.CharField('机柜代号', max_length=20, null=True, default='')
    shelf = models.CharField('机框编号', max_length=20, null=True, default='')

    power = models.IntegerField('电源数量', null=True, default=0)
    power_details = models.CharField('电源详细信息', max_length=50, null=True, blank=True)

    drac_ip = models.CharField('远程管理卡ip', max_length=15)
    drac_user = models.CharField('管理卡用户名', max_length=20, null=True, blank=True)
    drac_passwd = models.CharField('管理卡密码', max_length=20, null=True, blank=True)

    #    price = models.FloatField('采购价格', null=True, default='0.0')
    purchase_date = models.DateTimeField('购买日期', auto_now_add=True, null=True)
    asset_number = models.CharField('资产编号', max_length=100)
    worth = models.IntegerField('资产价值', null=True, default=0)

    # status = models.IntegerField('机器状态', null=True, default=1, choices=MACHINE_STATUS_CHOICE)
    status = models.ForeignKey(MachineStatus, related_name='machine')
    comment = models.CharField('备注信息', max_length=200, null=True, blank=True)

    # mac_user = models.CharField('申请人', max_length=100, null=True, blank=True)
    m_user = models.ForeignKey(User, verbose_name='使用人', related_name='machine', null=True, blank=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return self.sn
        # if self.net:
        #     tmp = []
        #     for ip in self.net.values_list('ip_address'):
        #         tmp.append(ip[0])
        #     ip = ','.join(tmp)
        #     return "%s - %s " % (ip, self.sn)
        # else:
        #     return self.sn

    class Meta:
        permissions = (
            ("view_physicalmachine", "查看固定资产列表"),
        )


class Cmdb(models.Model):
    """
    cmdb
    """
    # machine = models.ForeignKey(PhysicalMachine, related_name='cmdb', unique=True)
    machine = models.OneToOneField(PhysicalMachine)
    # system = models.IntegerField('操作系统', choices=SYSTEM_CHOICES,default='0')
    # system = models.ForeignKey(MachineSystem,related_name='system')

    system_arch = models.CharField('架构体系', max_length=10, blank=True, default='x86_64')
    system_name = models.CharField('操作系统', max_length=100, blank=True, default='')
    system_version = models.CharField('操作系统版本', max_length=100, blank=True, default='')
    puppet = models.CharField('PUPPET组', max_length=20, blank=True)
    hostname = models.CharField('主机名', max_length=50, unique=True)
    # mac_user = models.CharField('使用人', max_length=100, blank=True)
    # deploy_type = models.CharField('部署类型', max_length=10, blank=True, default='1')

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return 'id:%s, hostname:%s' % (self.id, self.hostname)

    class Meta:
        permissions = (
            ("view_cmdb", "查看CMDB列表"),
        )


class NetAddress(models.Model):
    """
    网络配置信息
    """
    machine = models.ForeignKey(PhysicalMachine, related_name='net')
    device_name = models.CharField('网卡名称', max_length=50, default='eth0')
    ip_address = models.CharField('IP地址', max_length=100, unique=True, default='')
    ip_status = models.CharField('IP状态', max_length=50, default='False')
    mask_address = models.CharField('掩码地址', max_length=100, default='255.255.255.0')
    mac_address = models.CharField('MAC地址', max_length=100, unique=True, default='')
    gateway_address = models.CharField('网关地址', max_length=100, blank=True, null=True)
    descriptions = models.CharField('描述信息', max_length=500, null=True, blank=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    change_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return 'id:%s, device_name:%s, ip_address:%s' % (self.id, self.device_name, self.ip_address)


class Disk(models.Model):
    """
    主机硬盘信息
    """
    DISK_STATUS_CHOICES = (
        ('Active', '正常'),
        ('Error', '故障'),
    )
    # machine = models.ForeignKey(PhysicalMachine, related_name='disk')
    device_name = models.CharField('硬盘名称', max_length=10, default='sda')
    size = models.IntegerField('硬盘大小(T)')
    company = models.CharField('硬盘厂商', max_length=20, blank=True)
    model = models.CharField('硬盘型号', max_length=20, blank=True)
    sn = models.CharField('硬盘SN', max_length=20, unique=True)
    raid = models.CharField('raid', max_length=10, blank=True)
    status = models.CharField('状态', choices=DISK_STATUS_CHOICES, max_length=10)

    def __unicode__(self):
        return 'id:%s, device_name:%s, size:%s' % (self.id, self.device_name, self.size)


class Environment(models.Model):
    name = models.CharField('状态名称', max_length=20, unique=True)
    enname = models.CharField('英文名称', max_length=20, blank=True)

    def __unicode__(self):
        return '%s环境' % (self.name)


class Software(models.Model):
    """
    软件版本信息
    """
    name = models.CharField('名称', max_length=200)
    version = models.CharField('版本', max_length=100)
    website = models.CharField('官网', max_length=300, blank=True)
    person = models.ForeignKey(User, verbose_name='负责人', related_name='softwarecharge', blank=True, null=True)

    def __unicode__(self):
        return '%s: %s' % (self.name, self.version)


class Production(models.Model):
    """
    产品线
    """
    name = models.CharField('名称', max_length=100)
    enname = models.CharField('英文名称', max_length=100)

    def __unicode__(self):
        return '%s' % (self.name)


class App(models.Model):
    """
    应用
    """
    production = models.ForeignKey(Production, related_name='app')
    name = models.CharField('名称', max_length=100)
    enname = models.CharField('英文名称', max_length=100)

    def __unicode__(self):
        return '%s' % (self.name)


class Project(models.Model):
    """
    工程
    """
    app = models.ForeignKey(App, related_name='project')
    name = models.CharField('名称', max_length=100)
    enname = models.CharField('英文名称', max_length=100)

    def __unicode__(self):
        return '%s' % (self.name)

    class Meta:
        permissions = (
            ("view_project", "查看应用列表"),
        )


class Projectconfig(models.Model):
    """
    工程
    """
    project = models.ForeignKey(Project, related_name='config')

    # deploy_type = models.CharField('部署类型', max_length=2, default='1', choices=TYPE_STATUS)
    env = models.ForeignKey(Environment, related_name='project', verbose_name='环境类型', default=1)
    tag = models.CharField('TAG', max_length=500, blank=True)
    # developer = models.CharField('开发负责人', max_length=200, blank=True)
    # operator = models.CharField('运维负责人', max_length=200, blank=True)
    developer = models.ManyToManyField(User, verbose_name='开发负责人', related_name='appdev', blank=True, default='')
    operator = models.ManyToManyField(User, verbose_name='运维负责人', related_name='appop', blank=True, default='')
    comment = models.CharField('备注信息', max_length=200, blank=True)
    vip = models.CharField('虚拟IP', max_length=50, blank=True)
    svn_site = models.CharField('SVN地址', max_length=500, blank=True)
    svn_version = models.CharField('SVN版本号', max_length=50, blank=True)
    domain = models.CharField('域名', max_length=100, blank=True)
    software = models.ManyToManyField(Software, verbose_name='基础软件', related_name='project', blank=True, default='')
    # software = models.ManyToManyField(SoftwareConfig, verbose_name='软件信息', related_name='project', blank=True, default='')

    '''cache '''
    # cache = models.ManyToManyField(Software, verbose_name='Cache软件', related_name='projectcache', blank=True, default='')
    cache = models.CharField('Cache软件', max_length=100, blank=True)
    cache_info = models.CharField('CacheInfo', max_length=100, blank=True)
    #
    # '''NoSQL'''
    # nosql = models.ManyToManyField(Software, verbose_name='NoSQL软件', related_name='projectNoSQL', blank=True, default='')
    nosql = models.CharField('NoSQL软件', max_length=100, blank=True)
    nosql_info = models.CharField('NoSQLInfo', max_length=100, blank=True)
    #
    # '''MQ'''
    # queue = models.ManyToManyField(Software, verbose_name='MQ软件', related_name='projectMQ', blank=True, default='')
    queue = models.CharField('MQ软件', max_length=100, blank=True)
    queue_info = models.CharField('MQInfo', max_length=100, blank=True)
    #
    # '''DB'''
    # db = models.ManyToManyField(Software, verbose_name='DB软件', related_name='projectDB', blank=True, default='')
    db = models.CharField('DB软件', max_length=100, blank=True)
    db_info = models.CharField('DBInfo', max_length=100, blank=True)

    machine = models.ManyToManyField(PhysicalMachine, verbose_name='工作主机', related_name='project', blank=True,
                                     default='')

    create_time = models.DateTimeField('记录创建时间', auto_now_add=True)
    update_time = models.DateTimeField('记录更新时间', auto_now=True)

    omonitor = models.CharField('其他监控', max_length=1000, blank=True)

    def __unicode__(self):
        return '%s' % (self.id)


MONITOR_STATUS = (
    ('1', '正常'),
    ('2', '告警'),
    ('3', '关闭'),
    ('4', '未知'),
)

WORK_TYPE_STATUS = (
    ('1', 'GET'),
    ('2', 'POST'),
)


# from django.core.urlresolvers import reverse


class Monitor(models.Model):
    project = models.ForeignKey(Projectconfig, related_name='monitor')
    name = models.CharField('名称', max_length=100, blank=True)
    idc = models.ForeignKey(Idc, related_name='monitor', default=1)
    # server = models.CharField('监控节点', max_length=100, blank=True)
    workurl = models.CharField('URL', max_length=100)
    httpcode = models.CharField('HTTP返回值', max_length=100, default='200')
    worktype = models.CharField('调用方式', max_length=100, blank=True, choices=WORK_TYPE_STATUS, default='1')
    postdata = models.CharField('POST-data', max_length=1000, blank=True)
    timeout = models.CharField('超时', max_length=500, blank=True, default='15')
    workresult = models.CharField('正确返回值', max_length=500, blank=True)
    realresult = models.CharField('实际返回值', max_length=500, blank=True)
    httptestid = models.CharField('httptestid', max_length=100, blank=True)
    stepsid = models.CharField('stepsid', max_length=100, blank=True)
    monitoruser = models.ManyToManyField(User, verbose_name='接收人', related_name='monitor', blank=True, default='')
    status = models.CharField('状态', max_length=100, blank=True, choices=MONITOR_STATUS, default='4')

    def __unicode__(self):
        return '%s' % (self.name)
        #
        # def get_absolute_url(self):
        #     return reverse('zaupdate', kwargs={'pk': self.pk})


class Department(models.Model):
    name = models.CharField('部门名称', max_length=100, unique=True)
    supervisor = models.CharField('部门负责人', max_length=100)

    project = models.ManyToManyField(Projectconfig, verbose_name='管理项目', related_name='department', blank=True,
                                     default='')

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        permissions = (
            ("view_department", "查看CMDB列表"),
        )
