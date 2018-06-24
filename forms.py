# coding: utf-8
__author__ = 'machao'

from django import forms

from models import *


class PhysicalMachineForm(forms.ModelForm):
    class Meta:
        model = PhysicalMachine
        # fields = []
        exclude = []

    status = forms.ModelChoiceField(
            label='系统状态',
            queryset=MachineStatus.objects.all(),
            widget=forms.Select()
    )
    vendor = forms.ModelChoiceField(
            label='品牌',
            queryset=MachineCompany.objects.all(),
            widget=forms.Select()
            # widget=forms.RadioSelect()
    )
    m_user = forms.ModelChoiceField(
            label='申请人',
            queryset=User.objects.all(),
            widget=forms.Select(
                    attrs={
                        'id': 'm_user',
                        'class': 'chosen-select',
                        'tabindex': '4',
                        'data-placeholder': '请选择申请人',
                    }

            )
    )

    def __init__(self, *args, **kwargs):
        super(PhysicalMachineForm, self).__init__(*args, **kwargs)


class CmdbForm(forms.ModelForm):
    class Meta:
        model = Cmdb
        # fields = []
        exclude = ['machine']

    def __init__(self, *args, **kwargs):
        super(CmdbForm, self).__init__(*args, **kwargs)


# class ApplicationForm(forms.ModelForm):
#    class Meta:
#        model = Application
#        #fields = []
#        exclude = []

#    def __init__(self, *args, **kwargs):
#        super(ApplicationForm, self).__init__(*args, **kwargs)


class NetAddressForm(forms.ModelForm):
    class Meta:
        model = NetAddress
        # fields = []
        exclude = ['machine']

    def __init__(self, *args, **kwargs):
        super(NetAddressForm, self).__init__(*args, **kwargs)


class DiskForm(forms.ModelForm):
    class Meta:
        model = Disk
        # fields = []
        exclude = []

    def __init__(self, *args, **kwargs):
        super(DiskForm, self).__init__(*args, **kwargs)


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        exclude = []

    def __init__(self, *args, **kwargs):
        super(SoftwareForm, self).__init__(*args, **kwargs)


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        exclude = []

    def __init__(self, *args, **kwargs):
        super(ProductionForm, self).__init__(*args, **kwargs)


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        exclude = ['production']

    def __init__(self, *args, **kwargs):
        super(AppForm, self).__init__(*args, **kwargs)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['app']

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)


class ProjectConfigAddForm1(forms.ModelForm):
    class Meta:
        model = Projectconfig
        exclude = ['project']
        fields = ['env', 'developer', 'operator', 'svn_site', 'svn_version', 'software', 'machine', 'domain', 'vip']

    def __init__(self, *args, **kwargs):
        super(ProjectConfigAddForm1, self).__init__(*args, **kwargs)

    # env = forms.ChoiceField(
    #     required=True,
    #     label='环境',
    #     queryset=Environment.objects.all(),
    #     widget=forms.RadioSelect(),
    # )

    developer = forms.CharField(
            required=True,
            label='开发负责人',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        # 'required': True,
                        'data-placeholder': '加载中...',
                    }
            ),
    )

    operator = forms.CharField(
            required=True,
            label='运维负责人',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        # 'required': True,
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    software = forms.CharField(
            required=True,
            label='基础软件信息',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )

    machine = forms.CharField(
            required=True,
            label='主机信息',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )


class ProjectConfigAddForm2(forms.ModelForm):
    class Meta:
        model = Projectconfig
        fields = ['db', 'db_info', 'cache', 'cache_info', 'nosql', 'nosql_info', 'queue', 'queue_info']

    def __init__(self, *args, **kwargs):
        super(ProjectConfigAddForm2, self).__init__(*args, **kwargs)

    db = forms.CharField(
            required=True,
            label='db软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    cache = forms.CharField(
            required=True,
            label='cache软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    nosql = forms.CharField(
            required=True,
            label='nosql软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    queue = forms.CharField(
            required=True,
            label='MQ软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )


class ProjectConfigAddForm3(forms.ModelForm):
    class Meta:
        model = Projectconfig
        fields = ['comment']

    def __init__(self, *args, **kwargs):
        super(ProjectConfigAddForm3, self).__init__(*args, **kwargs)


class ProjectConfigtForm(forms.ModelForm):
    class Meta:
        model = Projectconfig
        exclude = ['project']

    def __init__(self, *args, **kwargs):
        super(ProjectConfigtForm, self).__init__(*args, **kwargs)

    software = forms.CharField(
            required=True,
            label='基础软件信息',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    db = forms.CharField(
            required=True,
            label='db软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    cache = forms.CharField(
            required=True,
            label='cache软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    nosql = forms.CharField(
            required=True,
            label='nosql软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    queue = forms.CharField(
            required=True,
            label='MQ软件及版本',
            widget=forms.Select(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    machine = forms.CharField(
            required=True,
            label='主机信息',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )
    developer = forms.CharField(
            required=True,
            label='开发负责人',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )

    operator = forms.CharField(
            required=True,
            label='运维负责人',
            widget=forms.SelectMultiple(
                    attrs={
                        'class': 'chosen-select',
                        'data-placeholder': '加载中...',
                    }
            ),
    )


class MonitorForm(forms.ModelForm):
    class Meta:
        model = Monitor
        exclude = ['project', 'httptestid', 'stepsid', 'status', 'realresult']

    def __init__(self, *args, **kwargs):
        super(MonitorForm, self).__init__(*args, **kwargs)

    postdata = forms.CharField(
            required=True,
            label='POST-data',
            widget=forms.Textarea(attrs={
                "rows": 3,
                "cols": 2,
            }),
    )


class MonitorFormUse(forms.ModelForm):
    class Meta:
        model = Monitor
        exclude = []

    def __init__(self, *args, **kwargs):
        super(MonitorFormUse, self).__init__(*args, **kwargs)

        # monitoruser = forms.CharField(
        #         required=True,
        #         label='发送人',
        #         widget=forms.SelectMultiple(
        #                 attrs={
        #                     'class': 'chosen-select',
        #                 }
        #         ),
        # )
