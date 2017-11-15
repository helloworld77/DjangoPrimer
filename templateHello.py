#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-11-13 21:39:26
# @Author  : Yafei (qiyafei_7@yeah.net)
# @Link    : http://www.cnblogs.com/mar-q/
# @Version : $Id$

import os
import sys
import hashlib
from io import BytesIO
from PIL import Image, ImageDraw
from django import forms
from django.conf import settings
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,render_to_response
from django.views.decorators.http import etag

#setting
DEBUG = os.environ.get('DEBUG','on')=='on'
SECRET_KEY = os.environ.get('SECRET_KEY', '&8x8ono))lhdi_6fg!h_9uv3l97w$m$(m6lg&0tttyb2e_lnlv')
ALLOWED_HOSTS=['*']
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
            # 'APP_DIRS': True,
        }
    ],
    STATICFILES_DIRS=[
        os.path.join(BASE_DIR, 'static'),
    ],
    STATIC_URL = '/static/'
)

class ImageForm(forms.Form):
    height = forms.IntegerField(min_value=1,max_value=2000)
    width = forms.IntegerField(min_value=1,max_value=2000)
    def generate(self, image_formate='PNG'):
        height = self.cleaned_data['height']
        width = self.cleaned_data['width']
        key = '{}.{}.{}'.format(width, height, image_formate)
        content = cache.get(key) ##增加服务器缓存
        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)
            text = '{}x{}'.format(width, height)
            textwidth,textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttop = (height - textheight) // 2
                textleft = (width - textwidth) // 2
                draw.text((textleft,texttop), text, fill=(255,255,255))
            content = BytesIO()
            image.save(content, image_formate)
            content.seek(0)
            cache.set(key, content, 60*60)
        return content

def generate_etag(req, width, height):
    content = 'Placeholder: {0}x{1}'.format(width, height)
    return hashlib.sha1(content.encode('utf-8')).hexdigest()

@etag(generate_etag)
def placeholder(req, width, height):
    form = ImageForm({'width':width, 'height':height})
    if form.is_valid():
        image = form.generate()
        return HttpResponse(image, content_type='image/png')
    else:
        return HttpResponseBadRequest('图片格式错误')

def index(req):
    example = reverse('placeholder', kwargs={'width':50, 'height':50})##通过url标签和参数获取地址
    context = {
        'example': req.build_absolute_uri(example)##把上面形成的地址传递给页面
    }
    # print ('********',context)
    return render_to_response('home.html', context)

urlpatterns=[
    url(u'^$',index, name='homepage'),
    url(u'^image/(?P<width>[0-9]+)x(?P<height>[0-9]+)/$', placeholder, name='placeholder'),
]

application = get_wsgi_application()

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)





