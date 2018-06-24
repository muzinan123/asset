# coding: utf-8

import datetime

from django.db.models import Q
from rest_framework import viewsets, filters, permissions
from rest_framework.response import Response

import CustomPagination
from hades.tasks import addlog
from serializers import *


class NetAddressViewSet(viewsets.ModelViewSet):
    """
    网络配置API， 提交格式如下：\n
    `{
    "device_name": "eth0",
    "ip_address": "10.15.2.71",
    "ip_status": "1",
    "mask_address": "255.255.240.0",
    "mac_address": "18:03:73:fa:9e:83",
    "gateway_address": "10.17.4.1",
    "descriptions": "",
    "create_time": "2015-07-20T07:41:54Z",
    "change_time": "2015-07-20T07:41:54Z",
    "machine": 101
    }`
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = NetAddress.objects.all()
    serializer_class = NetAddressSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'mac_address',
        'ip_address',
        'mask_address',
        'gateway_address',
    ]

    def create(self, request, *args, **kwargs):
        # self.serializer_class = NetAddressSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        addlog.delay(request.user.username, 'NetAddress', '', 'asset_api.viewsets', '新增', request.data)
        self.perform_create(serializer)
        # logger.info('user: %s, create:(Net)new, set:%s ', request.user.username, request.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = NetAddressSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        addlog.delay(request.user.username, 'NetAddress', instance.id, 'asset_api.viewsets', '修改', instance.__dict__,
                     request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # logger.info('user:%s, update:(Net)%s, set:%s', request.user.username, instance.__dict__, request.data)
        return Response(serializer.data)


class DiskViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
    ]

    # def create(self, request, *args, **kwargs):
    #     self.serializer_class = DiskSerializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     addlog.delay(request.user.username, 'Disk', '', 'asset_api.viewsets', '新增', request.data)
    #     self.perform_create(serializer)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     self.serializer_class = DiskSerializer
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     addlog.delay(request.user.username, 'Disk', instance.id, 'asset_api.viewsets', '修改', instance.__dict__,
    #                  request.data)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     # logger.info('user:%s, update:(Disk)%s, set:%s', request.user.username, instance.__dict__, request.data)
    #     return Response(serializer.data)

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = self.queryset
    #
    #     queryset = queryset.select_related('machine__net__ip_address')
    #
    #     return queryset


# class ApplicationViewSet(viewsets.ModelViewSet):
#    permission_classes = (permissions.IsAuthenticated,)
#    queryset = Application.objects.all()
#    serializer_class = ApplicationSerializer
#    filter_backends = (filters.DjangoFilterBackend,)
#    filter_fields = [
#        'id',
#        'name',
#        'app_user',
#    ]

class CMDBViewSet(viewsets.ModelViewSet):
    """
    CMDB信息API，提交格式如下：\n
    `{
    "puppet": "asdfasdf",
    "hostname": "testing-chanjet.com",
    "mac_user": "马超",
    "machine": 4,
    "system": 6
    }`\n
    查询参数：\n
    'id',
    'system',
    'hostname',
    'puppet',
    'mac_user',
    'machine_id',
    'machine__sn'
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Cmdb.objects.all()
    serializer_class = CMDBSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    # renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'hostname',
        'puppet',
        'machine_id',
        'machine__sn'
    ]

    # def create(self, request, *args, **kwargs):
    #     self.serializer_class = CMDBSerializer
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     addlog.delay(request.user.username, 'CMDB', '', 'asset_api.viewsets', '新增', request.data)
    #     self.perform_create(serializer)
    #     # logger.info('user: %s, create:(CMDB)new, set:%s ', request.user.username, request.data)
    #     return Response(serializer.data)
    #
    # def update(self, request, *args, **kwargs):
    #     self.serializer_class = CMDBSerializer
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     addlog.delay(request.user.username, 'CMDB', instance.id, 'asset_api.viewsets', '修改', instance.__dict__,
    #                  request.data)
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     # logger.info('user:%s, update:(CMDB)%s, set:%s', request.user.username, instance.__dict__, request.data)
    #     return Response(serializer.data)


class PhysicalMachineViewSet(viewsets.ModelViewSet):
    """
    主机信息API,提交格式如下：\n
    `{
    "sn": "CNG005S4P1",
    "machine_model": "ProLiant DL360 G6",
    "cpu_n": 8,
    "cpu_details": null,
    "mem_total_size": 145203,
    "mem_details": null,
    "ld_total_size": null,
    "ld_details": null,
    "pd_details": null,
    "raid_adptr": "None",
    "raid_cache": null,
    "rack": "E012",
    "shelf": "10",
    "power": null,
    "power_details": null,
    "drac_ip": "172.18.7.148",
    "drac_user": null,
    "drac_passwd": null,
    "purchase_date": "2015-07-05T16:00:00Z",
    "asset_number": "105820100306",
    "comment": "陈强测试机器",
    "mac_user": "ochenqiangh",
    "create_time": "2014-03-24T16:29:29Z",
    "change_time": "2015-07-08T08:54:13Z",
    "idc": 1,
    "vendor": 4,
    "status": 3
    }`

    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = PhysicalMachine.objects.all()
    serializer_class = PhysicalMachineSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BaseRenderer,JSONRenderer,BrowsableAPIRenderer,YAMLRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'sn',
        'drac_ip',
        'idc',
        'cmdb__hostname',
        'idc__name',
        'status__name',
        'project',
        'project__id',
        'project__project__id',
        'project__project__name',
        'project__env',
        'net__ip_address',
    ]

    # def filter_queryset(self, queryset):
    #    queryset = super(PhysicalMachineViewSet, self).filter_queryset(queryset)
    #    return queryset.order_by('id')
    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = PhysicalMachine.objects.all().distinct()

        # queryset = queryset.prefetch_related('idc', 'net', 'project__project', 'cmdb', 'status', 'project', 'm_user')
        queryset = self.get_serializer_class().setup_eager_loading(queryset)

        project = self.request.query_params.get('noproject', None)
        m_user = self.request.query_params.get('m_user', None)
        asset = self.request.query_params.get('asset', None)
        search = self.request.query_params.get('search', None)
        checklist = self.request.query_params.get('checklist', None)
        projectid = self.request.query_params.get('projectid', None)
        projectenv = self.request.query_params.get('projectenv', None)
        index = self.request.query_params.get('index', None)

        if checklist is not None:
            self.serializer_class = PhysicalMachineSerializerAllIPList

        if index is not None:
            self.serializer_class = PhysicalMachineSerializerIndex

        if search is not None:
            queryset = queryset.filter(
                    Q(sn__icontains=search) |
                    Q(drac_ip__icontains=search) |
                    Q(net__ip_address__icontains=search) |
                    Q(cmdb__hostname=search)

            )
            # queryset = queryset.filter(drac_ip__icontains=search)
            # queryset = queryset.filter(net__ip_address__icontains=search)

        if asset is not None:
            self.serializer_class = PhysicalMachineSerializerAsset
            self.pagination_class = CustomPagination.CustomPagination

        if project is not None:
            queryset = queryset.filter(project__isnull=True)
            queryset = queryset.exclude(status__name='报废')
        if m_user is not None:
            queryset = queryset.filter(m_user__userprofile__ldap_username=m_user)

        if projectid is not None:
            if projectenv is not None and projectenv:
                queryset = queryset.filter(Q(project__project__id=projectid) & Q(project__env=projectenv))
            else:
                queryset = queryset.filter(project__project__id=projectid)

        return queryset

    def list(self, request, *args, **kwargs):
        self.serializer_class = PhysicalMachineSerializerList
        # queryset = self.queryset.prefetch_related('project__project')
        # queryset = self.filter_queryset(queryset)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, pk):
        machine = self.get_object(pk)
        serializer = PhysicalMachineSerializerList(machine)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = PhysicalMachineSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        addlog.delay(request.user.username, 'Machine', '', 'asset_api.viewsets', '新增', request.data)
        self.perform_create(serializer)
        # logger.info('user: %s, create:(Machine)new, set:%s ', request.user.username, request.data)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = PhysicalMachineSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        addlog.delay(request.user.username, 'Machine', instance.id, 'asset_api.viewsets', '修改', instance.__dict__,
                     request.data)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class MachineStatusViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = MachineStatus.objects.all()
    serializer_class = MachineStatusSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'name',
    ]


class SoftwareViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset

        queryset = queryset.prefetch_related('person')
        return queryset


class ProductionViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Production.objects.all()
    serializer_class = ProductionSerializerList
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'name',
        'enname',
        'app__enname',
        'app__id',
        'app__project__enname',
        'app__project__id',
        'app__project__config__machine__net__ip_address'
    ]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        # queryset = queryset.prefetch_related('app__project')

        return queryset

    def list(self, request, *args, **kwargs):
        action = self.request.query_params.get('action', None)

        if action is not None:
            if action == 'all':
                self.serializer_class = ProductionSerializerAll
                queryset = self.queryset.prefetch_related(
                        'app__project',
                        'app__project__config',
                        'app__project__config__machine',
                        'app__project__config__machine__net',
                        'app__project__config__machine__cmdb',
                        'app__project__config__machine__status',
                        'app__project__config__machine__idc',
                        'app__project__config__operator',
                        'app__project__config__developer',
                        'app__project__config__software',
                        'app__project__config__env'
                )
                # queryset = queryset.prefetch_related('app__project__config', 'app__project__config__machine')
            elif action == 'menu':
                queryset = self.queryset.prefetch_related('app__project')
                self.serializer_class = ProductionSerializerMenu
            elif action == 'list':
                queryset = self.queryset.prefetch_related(
                        'app__project',
                        'app__project__config',
                        'app__project__config__machine',
                        'app__project__config__operator',
                        'app__project__config__developer',
                        'app__project__config__software'
                )
                self.serializer_class = ProductionSerializer
        else:
            queryset = self.queryset.prefetch_related('app__project')

        queryset = self.filter_queryset(queryset)
        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.serializer_class = ProductionSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ProductionSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AppViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = App.objects.all()
    serializer_class = AppSerializerList
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'name',
        'enname',
        'production__enname',
        'production__id',
        'project__id',
        'project__name',
    ]

    def create(self, request, *args, **kwargs):
        self.serializer_class = AppSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = AppSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        queryset = queryset.prefetch_related('project')

        return queryset


class AppProjectViewSet(viewsets.ModelViewSet):
    """
    工程API

    """
    queryset = Project.objects.all()
    serializer_class = AppProjectSerializerList
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'name',
        'enname',
        'app__id',
        'app__enname',
    ]

    def create(self, request, *args, **kwargs):
        self.serializer_class = AppProjectSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = AppProjectSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ProjectConfigViewSet(viewsets.ModelViewSet):
    """
    工程详细API

    """
    queryset = Projectconfig.objects.all()
    serializer_class = ProjectConfigSerializerList
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)

    filter_fields = [
        'id',
        'project',
        'env',
        'project__name',
        'project__id',
        'project__enname',
        'machine__net__ip_address',
    ]

    def create(self, request, *args, **kwargs):
        self.serializer_class = ProjectConfigSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.serializer_class = ProjectConfigSerializer
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset

        queryset = queryset.prefetch_related('software', 'operator', 'developer', 'machine', 'project',
                                             'env').select_related(
                'project__id')

        machine = self.request.query_params.get('machine', None)

        if machine:
            self.serializer_class = ProjectConfigSerializerAsset
        return queryset


class ProjectMenuViewSet(viewsets.ModelViewSet):
    """
    Menu API
    """
    queryset = Production.objects.all()
    serializer_class = ProductionSerializerMenu
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'name',
    ]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        queryset = queryset.prefetch_related('app__project')
        name = self.request.query_params.get('name', None)

        if name:
            queryset = queryset.filter(Q(name__contains=name) | Q(app__name__contains=name))
        return queryset


class UserInfoViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Userprofile.objects.all()
    serializer_class = UserProfileSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    ##renderer_classes = (BrowsableAPIRenderer,JSONRenderer,YAMLRenderer,JSONPRenderer,XMLRenderer)
    filter_fields = [
        'id',
        'user__username',
        'name'
    ]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        queryset = self.queryset
        queryset = self.queryset.prefetch_related('user')

        list = self.request.query_params.get('list', None)

        if list is not None:
            self.serializer_class = UserProfileSerializerAllList

        return queryset


class LogsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Logs.objects.all().order_by('-id')
    serializer_class = LogsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = [
        'id',
        'user',
        'model',
        'action',
        'modelid',
    ]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset

        queryset = queryset.prefetch_related('user')

        message_contains = self.request.query_params.get('message_contains', None)
        today = self.request.query_params.get('today', None)
        SearchDate = self.request.query_params.get('SearchDate', None)
        SearchUserName = self.request.query_params.get('SearchUserName', None)
        MachineId = self.request.query_params.get('MachineId', None)

        if message_contains is not None:
            queryset = queryset.filter(
                    Q(message_new__contains=message_contains) | Q(message_old__contains=message_contains))

        if today:
            queryset = queryset.filter(time__gte=datetime.date.today())

        if SearchDate:
            st = SearchDate.split(' - ')[0]
            sp = SearchDate.split(' - ')[1]

            start_date = datetime.datetime.strptime(st, '%Y-%m-%d %H:%M')
            stop_date = datetime.datetime.strptime(sp, '%Y-%m-%d %H:%M')
            queryset = queryset.filter(time__range=(start_date, stop_date))

        if SearchUserName:
            queryset = queryset.filter(user__username=SearchUserName)

        if MachineId:
            queryset = queryset.filter(Q(message_new__contains=MachineId) | Q(message_old__contains=MachineId) | Q(
                    modelid=MachineId)).order_by('-id')

        return queryset


class EnvironmentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Environment.objects.all()
    serializer_class = EnvironmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = [
        'id',
        'name'
    ]


class MonitorViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Monitor.objects.all()
    serializer_class = MonitorSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = [
        'id',
        'project_id'
    ]

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = self.queryset
        # queryset = self.get_serializer_class().setup_eager_loading(queryset)
        queryset = queryset.prefetch_related('monitoruser', 'project__project')
        menu = self.request.query_params.get('menu', None)

        if menu is not None:
            self.serializer_class = MonitorSerializer
            # self.serializer_class = MonitorSerializerList

        return queryset


class DepartmentViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = [
        'id',
    ]

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned purchases to a given user,
    #     by filtering against a `username` query parameter in the URL.
    #     """
    #     queryset = self.queryset
    #     # queryset = self.get_serializer_class().setup_eager_loading(queryset)
    #     queryset = queryset.prefetch_related('monitoruser', 'project__project')
    #     menu = self.request.query_params.get('menu', None)
    #
    #     if menu is not None:
    #         self.serializer_class = MonitorSerializer
    #         # self.serializer_class = MonitorSerializerList
    #
    #     return queryset
