# coding: utf-8
from hades.views import my_render
# Create your views here.
from django.shortcuts import get_object_or_404, redirect
import json

from asset_api.forms import *
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from asset_api.sdk import asset_connect
from hades.tasks import add_to_cmdb, add_all_to_cmdb
from aliyun import diff_aliyun_cmdb
from zabbix import Zabbix


@login_required
def index(request, messages=None):
    return my_render(request, 'asset_web/index.html', {
    })


# @permission_required('cmdb.view_asset')
@permission_required('asset_api.view_physicalmachine', login_url='/', raise_exception=False)
@login_required
def asset(request, messages=None):
    """
    固定资产首页，简单展示目前机器状态及机器列表。
    :param request:
    :return:
    """
    context = {}
    context['messages'] = messages
    all_machine = PhysicalMachine.objects.all()
    context['all_count'] = all_machine.count()
    context['m6_count'] = all_machine.filter(Q(idc__name='M6') & ~Q(status__name='报废')).count()
    context['yq_count'] = all_machine.filter(Q(idc__name='园区') & ~Q(status__name='报废')).count()
    context['al_count'] = all_machine.filter(Q(idc__name='阿里云') & ~Q(status__name='报废')).count()
    context['m6_online'] = all_machine.filter(Q(idc__name='M6') & Q(status__name='在线')).count()
    context['yq_online'] = all_machine.filter(Q(idc__name='园区') & Q(status__name='在线')).count()
    context['al_online'] = all_machine.filter(Q(idc__name='阿里云') & Q(status__name='在线')).count()
    context['all_online'] = all_machine.filter(Q(status__name='在线')).count()
    context['m6_broken'] = all_machine.filter(
            Q(idc__name='M6') & Q(status__name='停机')).count()
    context['yq_broken'] = all_machine.filter(
            Q(idc__name='园区') & Q(status__name='停机')).count()
    context['al_broken'] = all_machine.filter(
            Q(idc__name='阿里云') & Q(status__name='停机')).count()
    context['all_broken'] = all_machine.filter(Q(status__name='停机')).count()
    context['m6_idle'] = all_machine.filter(
            Q(idc__name='M6') & Q(project=None)).count()
    context['yq_idle'] = all_machine.filter(
            Q(idc__name='园区') & Q(project=None)).count()
    context['al_idle'] = all_machine.filter(
            Q(idc__name='阿里云') & Q(project=None)).count()
    context['all_idle'] = all_machine.filter(Q(project=None)).count()

    context['machineform'] = PhysicalMachineForm()

    return my_render(request, 'asset_web/asset.html', context)


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def add_new_machine(request):
    """
    添加新的主机
    :param request:
    :return:
    """

    messages = None
    c = {}
    if request.method == 'POST':

        url = 'http://%s:%s/api/machine/' % (settings.API_HOST, settings.API_PORT)
        connect = asset_connect(url)
        messages = connect.post(request.POST)

    else:
        messages = '未知错误!'

    return asset(request, messages=messages)


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def update_machine(request, id=None):
    """
    修改主机信息
    :param request:
    :return:
    """
    messages = None
    c = {}

    if request.method == 'POST':
        url = 'http://%s:%s/api/machine/%s/' % (settings.API_HOST, settings.API_PORT, id)
        connect = asset_connect(url)
        messages = connect.update(request.POST)

    else:
        messages = '未知错误!'

    return info(request, id, messages=messages)


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def add_new_cmdb(request, id):
    """
    修改主机信息
    :param request:
    :return:
    """
    messages = None
    c = {}
    try:
        qt_cmdb = Cmdb.objects.get(machine_id=id)
    except:
        qt_cmdb = None

    if request.method == 'POST':
        data = request.POST
        if qt_cmdb:
            url = 'http://%s:%s/api/cmdb/%s/' % (settings.API_HOST, settings.API_PORT, qt_cmdb.id)
            connect = asset_connect(url)
            messages = connect.update(data)
            # print messages.read()
        else:
            url = 'http://%s:%s/api/cmdb/' % (settings.API_HOST, settings.API_PORT)
            connect = asset_connect(url)
            messages = connect.post(data)
    else:
        messages = '未知错误!'

    return info(request, id, messages=messages)


@permission_required('asset_api.view_cmdb', login_url='/', raise_exception=False)
@login_required
def cmdb(request):
    """
    CMDB主机系统配置信息展示
    :param request:
    :return:
    """
    return my_render(request, 'asset_web/cmdb.html')


@permission_required('asset_api.view_project', login_url='/', raise_exception=False)
@login_required
def app(request):
    """
    应用树展示
    :param request:
    :return:
    """

    return my_render(request, 'asset_web/app.html', {
        'productionform': ProductionForm(),
        'appform': AppForm(),
        'projectform': ProjectForm(),
        'projectconfigform1': ProjectConfigAddForm1(),
        'projectconfigform2': ProjectConfigAddForm2(),
        'projectconfigform3': ProjectConfigAddForm3(),
        'env': Environment.objects.all(),
    })


@permission_required('asset_api.view_physicalmachine', login_url='/', raise_exception=False)
@login_required
def info(request, id, messages=None):
    """
    主机详细信息.
    :param request:
    :param id:
    :return:
    """
    net = []
    form_disk = []
    form_project = []

    # qt_machine = get_object_or_404(PhysicalMachine, pk=id)

    qt_machine = PhysicalMachine.objects.filter(pk=id).prefetch_related('project', 'project__env', 'project__project')[
        0]

    form_machine = PhysicalMachineForm(instance=qt_machine)
    try:
        qt_net = NetAddress.objects.filter(machine_id=id)
        for qt in qt_net:
            # form_net.append(ipstatus=check_ip(qt.ip_address))
            # print qt
            # qt.ip_status = check_ip(qt.ip_address)
            net_instance = NetAddressForm(instance=qt)
            net.append(net_instance)
        ip = qt_net[0].ip_address
    except:
        net = ''
        ip = 'null'

    try:
        qt_cmdb = Cmdb.objects.get(machine_id=id)
        form_cmdb = CmdbForm(instance=qt_cmdb)
    except:
        form_cmdb = CmdbForm()

    try:
        qt_disk = Disk.objects.filter(machine_id=id)
        for qt in qt_disk:
            form_disk.append(DiskForm(instance=qt))
    except:
        form_disk = ''

    # try:
    #     qt_project = Projectconfig.objects.filter(machine__id=id)
    #     for qt in qt_project:
    #         form_project.append(ProjectForm(instance=qt))
    # except:
    #     form_project = ''

    # for pconfig in qt_machine.project.all():
    #     print pconfig.project.name, pconfig.env.name

    return my_render(request, 'asset_web/info.html', {
        'user': request.user,
        'machineinfo': qt_machine,
        'machine': form_machine,
        'net': net,
        'net_form': NetAddressForm(),
        'cmdb': form_cmdb,
        'disk': form_disk,
        # 'project': form_project,
        # 'mlogs': mlogs,
        'messages': messages
    })


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def add_project_2_machine(request, id):
    qt_machine = get_object_or_404(PhysicalMachine, pk=id)

    if request.method == 'POST':
        if request.POST.has_key('project'):
            project_list = request.POST.getlist('project')
            qt_machine.project = project_list

            return redirect('/cmdb/info/%s/' % qt_machine.id)
        else:
            qt_machine.project.clear()
            return redirect('/cmdb/info/%s/' % qt_machine.id)

    return my_render(request, 'asset_web/add_project_2_machine.html', {
        'user': request.user,
        'projectlist': Project.objects.all(),
        'machineinfo': PhysicalMachine.objects.get(pk=id),
    })


@permission_required('asset_api.change_project', login_url='/', raise_exception=False)
@login_required
def add_machine_2_project(request, id):
    qt_project = get_object_or_404(Project, pk=id)

    if request.method == 'POST':
        if request.POST.has_key('machine'):
            machine_list = request.POST.getlist('machine')
            qt_project.machine = machine_list

            return redirect('/cmdb/appinfo/%s/' % qt_project.id)
        else:
            qt_project.machine.clear()
            return redirect('/cmdb/appinfo/%s/' % qt_project.id)

    return my_render(request, 'asset_web/add_machine_2_project.html', {
        'user': request.user,
        'machinelist': PhysicalMachine.objects.all(),
        'projectinfo': Project.objects.get(pk=id),
    })


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def add_network_2_machine(request, id):
    try:
        qt = NetAddress.objects.get(pk=request.POST['netid'])
    except:
        qt = ''

    if request.method == 'POST':
        data = request.POST

        if qt:
            url = 'http://%s:%s/api/net/%s/' % (settings.API_HOST, settings.API_PORT, qt.id)
            connect = asset_connect(url)
            req = connect.update(data)
            if 'read' in dir(req):
                messages = req.read()
            else:
                messages = req
        else:
            url = 'http://%s:%s/api/net/' % (settings.API_HOST, settings.API_PORT)
            connect = asset_connect(url)
            req = connect.post(data)
            if 'read' in dir(req):
                messages = req.read()
            else:
                messages = req
    else:
        messages = '未知错误!'

    return info(request, id, messages=messages)


@permission_required('asset_api.view_project', login_url='/', raise_exception=False)
@login_required
def appinfo(request, id):
    """
    应用信息.
    :param request:
    :param id:
    :return:
    """
    qt_config = get_object_or_404(Projectconfig, pk=id)
    form_config = ProjectConfigtForm(instance=qt_config)

    qt_project = qt_config.project
    form_project = ProjectForm(instance=qt_project)

    qt_app = qt_config.project.app
    form_app = AppForm(instance=qt_app)

    qt_production = qt_config.project.app.production
    form_production = ProductionForm(instance=qt_production)

    qt_machine = PhysicalMachine.objects.filter(project=id)

    form_monitor = MonitorForm()

    return my_render(request, 'asset_web/appinfo.html', {
        'user': request.user,
        'config': form_config,
        'project': form_project,
        'app': form_app,
        'production': form_production,
        'monitor': form_monitor,
        'machine': qt_machine,
        'pid': id,
    })


@permission_required('asset_api.change_project', login_url='/', raise_exception=False)
@login_required
def appconfig(request, messages=None):
    """
    APP应用设置
    :param request:
    :return:
    """
    software = Software.objects.all()
    softwareform = SoftwareForm()

    return my_render(request, 'asset_web/appconfig.html', {
        'software': software,
        'softwareform': softwareform,
        'messages': messages,
    })


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def diff_with_aliyun_cmdb(request, messages=None):
    aliyun = ''
    cmdb = ''

    if request.method == 'POST':
        InstanceId = request.POST['InstanceId']
        add_to_cmdb.delay(InstanceId)
        # add_to_cmdb(InstanceId)

    connect = diff_aliyun_cmdb()
    cmdb_count = PhysicalMachine.objects.filter(idc__name='阿里云').count()

    if cmdb_count != connect.get_cout():
        aliyun = connect.diff_in_ali()
        cmdb = connect.diff_in_cmdb()

    return my_render(request, 'aliyun/diff.html', {
        'aliyun': aliyun,
        'cmdb': cmdb,
        'messages': messages
    })


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def check_all_ali_to_cmdb(request, messages=None):
    add_all_to_cmdb.delay()
    messages = '已添加新的阿里云同步进程。'

    return asset(request, messages)


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def get_vnc_password(request, id, messages=None):
    try:
        machine = PhysicalMachine.objects.get(pk=id)
    except:
        machine = None

    if machine is not None:
        hostname = machine.cmdb.hostname
        instanceid = 'i-' + hostname[2:-1]
        connect = diff_aliyun_cmdb()
        result = connect.get_vnc_password(instanceid)
        result['InstanceId'] = instanceid
    else:
        result = {'VncPasswd': 'not found '}

    return HttpResponse(json.dumps(result), content_type="application/json")


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def zabbix_monitor(request):
    result = {'result': False}
    zc = Zabbix()
    if request.method == 'POST':
        reqargs = request.POST
        if reqargs.has_key('id'):
            nets = NetAddress.objects.filter(machine_id=reqargs['id'])
            machine = PhysicalMachine.objects.get(pk=reqargs['id'])
            if nets:
                for net in nets:
                    try:
                        zc.edit_monitor(net.machine.idc_id, net.ip_address, request.POST['action'])
                        result['result'] = True
                    except:
                        pass
            elif machine:
                try:
                    zc.edit_monitor(machine.idc_id, machine.drac_ip, request.POST['action'])
                    result['message'] = 'With drac_ip.'
                    result['result'] = True
                except:
                    pass
            else:
                result['message'] = 'No have ip address.'
        elif reqargs.has_key('ip') and reqargs.has_key('idc'):
            zc.edit_monitor(reqargs['idc'], reqargs['ip'], reqargs['action'])
            result['result'] = True
        else:
            result['message'] = '参数错误.'

    return HttpResponse(json.dumps(result), content_type="application/json")


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def cmdb_search(request, messages=None):
    return my_render(request, 'asset_web/search.html', {
        'messages': messages,
        'idc': Idc.objects.all(),
        'app': Project.objects.all().prefetch_related('app', 'app__production'),
        'env': Environment.objects.all(),
    })


@permission_required('asset_api.change_physicalmachine', login_url='/', raise_exception=False)
@login_required
def data_report(request, messages=None):
    ### 通过使用人生成报表
    user_list = User.objects.select_related(
            'userprofile'
    ).prefetch_related(
            'machine',
    ).all()

    userreport = []
    tmp = {}

    for u in user_list:

        if u.machine.all():

            tmp['uid'] = u.id
            try:
                tmp['username'] = u.userprofile.name
            except:
                tmp['username'] = ''
            tmp['mcount'] = u.machine.count()
            # print [x.worth for x in u.machine.all()]
            tmp['worth'] = reduce((lambda x, y: x + y), [x.worth for x in u.machine.all()])

            userreport.append(tmp)
            tmp = {}
    ### 通过使用人生成报表 END###

    ### 通过产品线生成报表
    project_list = Project.objects.select_related(
            'app'
    ).prefetch_related(
            'app',
            'app__production',
            'config',
            'config__machine',
    ).all()

    projectreport = []
    for project in project_list:
        tmp['name'] = '%s > %s > %s' % (project.app.production.name, project.app.name, project.name)

        tmp['pid'] = project.id

        configlist = [config for config in project.config.all()]

        # print '%s %s' % (tmp['name'], configlist)

        if configlist:

            tmp['mcount'] = reduce((lambda x, y: x + y),
                                   [x.machine.count() for x in configlist if x.machine.count() is not []])

            machine_worth = [x.worth for m in configlist for x in m.machine.all() if m.machine.count() is not []]
            # print machine_worth
            if machine_worth:
                tmp['worth'] = reduce((lambda x, y: x + y), machine_worth)

        projectreport.append(tmp)
        tmp = {}

    #### 通过产品线生成报表 END

    return my_render(request, 'asset_web/datareport.html', {
        'messages': messages,
        'userlist': userreport,
        'projectlist': projectreport,
    })


def data_report_iplist(request, messages=None):
    uid = request.GET.get('uid', None)
    pid = request.GET.get('pid', None)

    if uid is not None:
        userinfo = User.objects.get(pk=uid)
        # result = [ip.ip_address for x in userinfo.machine.all() for ip in x.net.all()]
        result = [machine for machine in userinfo.machine.all()]

    elif pid is not None:
        projectinfo = Project.objects.get(pk=pid)
        # result = [ip.ip_address for project in projectinfo.config.all() for machine in project.machine.all() for ip in
        #           machine.net.all()]
        result = [machine for project in projectinfo.config.all() for machine in project.machine.all()]
    else:
        result = []

    print result

    return my_render(request, 'asset_web/datareportiplist.html', {
        'messages': messages,
        'result': result,

    })


def testing_api(request):
    result = []
    productions = Production.objects.all()

    for production in productions:
        productiontmp = {}
        productiontmp['id'] = production.id
        productiontmp['name'] = production.name
        productiontmp['enname'] = production.enname
        for app in production.app:
            apptmp = {}
            apptmp['id'] = app.id
            apptmp['name'] = app.name
            apptmp['enname'] = app.enname
            for project in app.project:
                projecttmp = {}
                projecttmp['id'] = project.id
                projecttmp['name'] = project.name
                projecttmp['enname'] = project.name
                apptmp['project'].append(projecttmp)
            productiontmp['app'].append(apptmp)

        result.append(productiontmp)

    return HttpResponse(json.dumps(result), content_type="application/json")
