# coding: utf-8

from django.conf.urls import url, patterns, include
from django.contrib import admin

from asset_api import views

admin.autodiscover()

from viewsets import *
from rest_framework import routers

# Routers provide an easy way of automatically determining the URL conf
router = routers.DefaultRouter()
router.register(r'machine', PhysicalMachineViewSet, base_name='machine')
router.register(r'cmdb', CMDBViewSet, base_name='cmdb')
router.register(r'net', NetAddressViewSet)
router.register(r'disk', DiskViewSet)
router.register(r'soft', SoftwareViewSet)
router.register(r'product', ProductionViewSet, base_name='product')
router.register(r'app', AppViewSet, base_name='app')
router.register(r'project', AppProjectViewSet, base_name='project')
router.register(r'pconfig', ProjectConfigViewSet, base_name='config')
router.register(r'env', EnvironmentViewSet, base_name='env')
router.register(r'user', UserInfoViewSet)
router.register(r'mstatus', MachineStatusViewSet)
router.register(r'logs', LogsViewSet)
router.register(r'monitor', MonitorViewSet)
router.register(r'department', DepartmentViewSet)
# router.register(r'test', PhysicalMachineViewSetAsset)
# router.register(r'pro_with_ip', AppProject_Haveinfo_ViewSet)
# router.register(r'container', ContainerViewSet)

router.register(r'appmenu', ProjectMenuViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
                       # API相关
                       url(r'^', include(router.urls), name='api'),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^t/', views.UserCountView.as_view()),
                       )
