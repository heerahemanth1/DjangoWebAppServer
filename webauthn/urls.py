# -*- coding: utf-8 -*-
from django.urls import path
from . import views

urlpatterns = [
    path('authenticate/', views.AuthenticateUser.as_view(), name='authenticate-user'),
    path('addUser/', views.CreateUser.as_view(), name='add-user'),
]