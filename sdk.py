#coding: utf-8
import urllib2, urllib, json, cookielib
from django.conf import settings

API_URL = 'http://%s:%s/api/' % (settings.API_HOST,settings.API_PORT)
API_USER = settings.API_USER
API_PASS = settings.API_PASSWD


class asset_connect(object):

    def __init__(self, url):
        self.api_url = API_URL
        self.api_user = API_USER
        self.api_pass = API_PASS
        self.url = url
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, self.api_url, self.api_user, self.api_pass)
        urllib2.install_opener(urllib2.build_opener(urllib2.HTTPBasicAuthHandler(passman)))
        self.req = urllib2.Request(self.url)

    def get(self):
        """
        获取API信息
        :return:
        """
        try:
            f = urllib2.urlopen(self.req)
            re = f.read()
        except Exception,e:
            return e

        return re

    def post(self, data):
        """
        POST，新增信息
        :param data:
        :return:
        """

        data = urllib.urlencode(data)
        try:
            self.req.get_method = lambda: 'POST'
            f = urllib2.urlopen(self.req, data)
            re = f.read()
        except Exception,e:
            return e
        return re

    def delete(self):
        """
        删除
        :return:
        """
        try:
            self.req.get_method = lambda: 'DELETE'
            f = urllib2.urlopen(self.req)
            re = f.read()
        except Exception,e:
            return e
        return re

    def update(self, data):
        """
        更新信息
        :return:
        """
        data = urllib.urlencode(data)
        try:
            self.req.get_method = lambda: 'PATCH'
            f = urllib2.urlopen(self.req, data)
            data = f.read()
        except Exception,e:
            return e

        return data

    def options(self):
        """
        获取链接参数，只能在主接口进行获取参数信息.
        """
        try:
            self.req.get_method = lambda: 'OPTIONS'
            f = urllib2.urlopen(self.req)
            data = f.read()
        except Exception,e:
            return e

        return data