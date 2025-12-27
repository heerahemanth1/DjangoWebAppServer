# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class AuthClient(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    redirect_uri = models.CharField(max_length=200)
    password = models.CharField(max_length=128)

class Authorization(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    client_id = models.ForeignKey(AuthClient, on_delete=models.CASCADE)
    auth_code = models.CharField(max_length=100, unique=True)
    access_token = models.CharField(max_length=100, unique=True)
    refresh_token = models.CharField(max_length=100, unique=True)
    # ToDo: Link permissions
    code_issued_time = models.DateTimeField()
    token_issued_time = models.DateTimeField()

