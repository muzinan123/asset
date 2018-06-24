# coding: utf-8

from rest_framework import pagination
from math import ceil
from base64 import b64decode, b64encode
from collections import OrderedDict, namedtuple

from django.core.paginator import Paginator as DjangoPaginator
from django.core.paginator import InvalidPage
from django.template import Context, loader
from django.utils import six

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.utils.urls import remove_query_param, replace_query_param


class CustomPagination(pagination.PageNumberPagination):
    ##jquery-datatable特殊参数处理
    draw = None
    num_pages = None

    def get_page_number(self, start, page_size):
        print dir(self)
        hits = max(1, self.page.paginator.count - start)
        self.num_pages = int(ceil(hits / float(page_size)))

        return self.num_pages

    def get_paginated_response(self, data):

        return Response({
            'Page': self.page.number,
            'Page_Size': self.page_size,
            # 'Max_Page': self.page.paginator.count / int(self.page_size),
            'Max_Page': int(ceil(self.page.paginator.count / float(self.page_size))),
            'Start': self.page.start_index(),
            'End': self.page.end_index(),
            'Total': self.page.paginator.count,
            'Data': data,
            'Error': None,

        })

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        ##根据客户端返回结果设置分页大小.
        pages = request.query_params.get('page_size', None)
        if pages is not None:
            self.page_size = pages
        else:
            self.page_size = self.get_page_size(request)

        if not self.page_size:
            return None

        paginator = DjangoPaginator(queryset, self.page_size)
        page_number = request.query_params.get(self.page_query_param, 1)

        if page_number in self.last_page_strings:
            page_number = self.num_pages

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if self.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request

        return list(self.page)

    """
    {
        "draw": 3,
        "iTotalRecords": 57,
        "iTotalDisplayRecords": 57,
        "aaData": [
            [
                "Gecko",
                "Firefox 1.0",
                "Win 98+ / OSX.2+",
                "1.7",
                "A"
            ],
            [
                "Gecko",
                "Firefox 1.5",
                "Win 98+ / OSX.2+",
                "1.8",
                "A"
            ],
            ...
        ]
    }

    http://127.0.0.1:8000/api/machine/?draw=2columns[0][data]=project&columns[0][name]=&columns[0][searchable]=true&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=idc&columns[1][name]=&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=cmdb.system_name&columns[2][name]=&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=sn&columns[3][name]=&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=comment&columns[4][name]=&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]=&columns[4][search][regex]=false&columns[5][data]=cpu_n&columns[5][name]=&columns[5][searchable]=true&columns[5][orderable]=true&columns[5][search][value]=&columns[5][search][regex]=false&columns[6][data]=mem_total_size&columns[6][name]=&columns[6][searchable]=true&columns[6][orderable]=true&columns[6][search][value]=&columns[6][search][regex]=false&columns[7][data]=drac_ip&columns[7][name]=&columns[7][searchable]=true&columns[7][orderable]=true&columns[7][search][value]=&columns[7][search][regex]=false&columns[8][data]=asset_number&columns[8][name]=&columns[8][searchable]=true&columns[8][orderable]=true&columns[8][search][value]=&columns[8][search][regex]=false&columns[9][data]=status&columns[9][name]=&columns[9][searchable]=true&columns[9][orderable]=true&columns[9][search][value]=&columns[9][search][regex]=false&columns[10][data]=net&columns[10][name]=&columns[10][searchable]=true&columns[10][orderable]=true&columns[10][search][value]=&columns[10][search][regex]=false&columns[11][data]=id&columns[11][name]=&columns[11][searchable]=true&columns[11][orderable]=true&columns[11][search][value]=&columns[11][search][regex]=false&order[0][column]=3&order[0][dir]=asc&start=10&length=10&search[value]=&search[regex]=false&_=1447654505461
    """
