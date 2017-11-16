#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 21:39:26
# @Author  : Yafei (qiyafei_7@yeah.net)
# @Link    : http://www.cnblogs.com/mar-q/
# @Version : $Id$

import os
import sys
from django.http import HttpResponse
def index(req):
	return HttpResponse('HelloWorld')

from django.conf.urls import url
urlpatterns=[
	url(u'^$',index),
]

DEBUG = os.environ.get('DEBUG','on')=='on'
SECRET_KEY = os.environ.get('SECRET_KEY','^3nrp_4-6)oh0&xl+t(!9k-n%$qis2if0s8pnm41n&nf#xss_)')
ALLOWED_HOSTS=['*']
from django.conf import settings
settings.configure(
	DEBUG=DEBUG,
	SECRET_KEY=SECRET_KEY,
	ROOT_URLCONF=__name__,
	ALLOWED_HOSTS=ALLOWED_HOSTS,
	MIDDLEWARE=[
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		]
	)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

if __name__ == "__main__":
	from django.core.management import execute_from_command_line
	execute_from_command_line(sys.argv)
