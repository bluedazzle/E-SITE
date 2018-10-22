"""esite URL Configuration

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
from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.site_login, name='login'),
    url(r'^sms/$', views.send_code, name='sms'),
    url(r'^question/$', views.question, name='question'),
    url(r'^intro/$', views.intro, name='intro'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^station/$', views.station, name='station'),
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^detail/', views.detail, name='detail'),
    url(r'^mapdata/$', views.map_data, name='mapdata'),
]

# url(r'^crt/$', views.crt, name='crt'),
