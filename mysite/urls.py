"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from blog.views import *
# from DjangoUeditor.forms import UEditorField
from django.conf import settings
from blog.views import *

urlpatterns = [
	url(r'ckeditor/', include('ckeditor_uploader.urls')),
	url(r'^admin/', admin.site.urls),
	url(r'^$', index, name='index'),
	url(r'^index/$', index, name='index'),
	url(r'^myarticle/$', myarticle, name='myarticle'),
	url(r'^addarticle/$', addarticle, name='addarticle'),
	url(r'^addarticlesave/$', addarticlesave, name='addarticlesave'),
	url(r'^article/detail/(\d.*)/$', articledetail, name='articledetail'),
	url(r'^article/comment/(?P<article_id>[0-9]+)/$', Articlecomment, name='articlecomment'),
	url(r'^regist/$', regist, name='regist'),
	url(r'^userlogin/$', userlogin, name='userlogin'),
	url(r'^userlogout/$', uesrlogout, name='userlogout'),
	url(r'^updateuserpassword/$', updateuserpassword, name='updateuserpassword'),
	url(r'^feeds/$', feeds, name='feeds'),
]

if settings.DEBUG:
	from django.conf.urls.static import static
	
	urlpatterns += static(
		settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
