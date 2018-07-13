# -*- coding:utf-8 -*-
import re

from django.db.models import F
from django.shortcuts import render
from django.utils.deprecation import MiddlewareMixin

from mainapp.models import User, Blog


class Counter(MiddlewareMixin):
    def process_request(self,req):
        path = req.path
        url = re.compile(r'^/(show/(\d+)$)')
        #
        # print(path)
        # if not (path=='/'):
        #     token = req.COOKIES.get('token')
        #     if not token:
        #         return render(req,'index.html')
        #     elif not User.objects.filter(token='token').exists():
        #         return render(req,'index.html')
        if url.findall(path):
            id = path.split('/')[-1]
            Blog.objects.filter(id=id).update(cnt=F('cnt')+1)


