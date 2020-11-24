"""bookmanager URL Configuration

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
from django.contrib import admin
from django.views.generic import RedirectView

from app01 import views

urlpatterns = [
    url(r'^login/', views.login),
    url(r'^publisher_list/', views.publisher_list, name='publist'),

    # FBV写法
    # url(r'^publisher_add/', views.publisher_add),
    # CBV写法
    url(r'^publisher_add/', views.PublishAdd.as_view(), name='pubadd'),

    url(r'^publisher_del/', views.publisher_del, name='pubdel'),
    # url(r'^publisher_edit/', views.publisher_edit),
    # 分组
    # url(r'^publisher_edit/(\d+)/', views.publisher_edit),
    # 命名分组
    url(r'^publisher_edit/(?P<nid>\d+)/', views.publisher_edit, name='pubedit'),

    url(r'^book_list/', views.book_list, name='booklist'),
    url(r'^book_add/', views.book_add, name='bookadd'),
    url(r'^book_del/', views.book_del, name='bookdel'),
    url(r'^book_edit/', views.book_edit, name='bookedit'),

    url(r'^author_list/', views.author_list, name='authorlist'),
    url(r'^author_add/', views.author_add, name='authoradd'),
    url(r'^author_del/', views.author_del, name='authordel'),
    url(r'^author_edit/', views.author_edit, name='authoredit'),

    url(r'^upload/', views.Upload.as_view(), name='upload'),

]
