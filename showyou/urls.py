#main 서브앱의 urls
#서브앱의 urls는 같은 위치의 view.py의 함수로 연결을 담당 (path)
#같은 위치의 views.py를 식별 못하면 import 

from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('generic/',views.generic, name = 'generic'),
    path('elements/',views.elements, name = 'elements'),
    path('twitterSelect/',views.twitterSelect, name = 'twitterSelect'),
    path('instaSelect/',views.instaSelect, name='instaSelect'),
    path('blogSelect/',views.blogSelect, name='blogSelect'),
    path('user/',views.user, name='user'),
]