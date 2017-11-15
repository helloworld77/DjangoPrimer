#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 21:39:26
# @Author  : Yafei (qiyafei_7@yeah.net)
# @Link    : http://www.cnblogs.com/mar-q/
# @Version : $Id$

import os
import sys
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.conf.urls import url
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django import forms
from PIL import Image, ImageDraw
from io import BytesIO
from django.core.cache import cache
from django.core.urlresolvers import reverse

class ImageForm(forms.Form):
    height = forms.IntegerField(max_value=2000,min_value=1)
    width = forms.IntegerField(max_value=2000,min_value=1)
    def generate(self, image_formate='png'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        text = '{}.{}.{}'.format(width, height, image_formate)
        content = cache.get(text)
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            textwidth,textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft,texttop), text, fill=(255,255,255))
            content = BytesIO()
            image.save(content, image_formate)
            content.seek(0)
            cache.set(text, content, 60*60)
        return content

def placeholder(req, width, height):
    form = ImageForm({'width':width, 'height':height})
    if form.is_valid():
        height = form.cleaned_data['height']
        width = form.cleaned_data['width']
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('图片格式错误')

def index(req):
    example = reverse('placeholder', kwargs={'width':50, 'height':50})
    context = {
        'example': req.build_absolute_uri(example)
    }
    print ('********',context)
    return render_to_response('home.html', context)

urlpatterns=[
    url(u'^$',index, name='homepage'),
    url(u'^image/(?P<width>[0-9]+)*(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
]

DEBUG = os.environ.get('DEBUG','on')=='on'
SECRET_KEY = os.environ.get('SECRET_KEY','&8x8ono))lhdi_6fg!h_9uv3l97w$m$(m6lg&0tttyb2e_lnlv')
ALLOWED_HOSTS=['*']
# BASE_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(__file__)
settings.configure(
    DEBUG=DEBUG,
    SECRET_KEY=SECRET_KEY,
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=ALLOWED_HOSTS,
    MIDDLEWARE=[
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
    ],
    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
        }
    ],
    STATICFILES_DIRS=[
        os.path.join(BASE_DIR, 'static'),
    ],
    STATIC_URL = '/static/'
)

application = get_wsgi_application()

if __name__ == "__main__":
    print("***********",BASE_DIR)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)





