# -*- coding: utf-8 -*-
from django.contrib.auth.models import User, Permission
from django.db import models


clienttypes = {
    "PUBLIC": "Public",
    "CONFIDENTIAL": "Confidential",
}

class AuthClient(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=100)
    client_type = models.CharField(choices=clienttypes)
    description = models.CharField(max_length=200)
    redirect_uri = models.CharField(max_length=200)
    password = models.CharField(max_length=128)

class Authorization(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(AuthClient, on_delete=models.CASCADE, null=True)
    auth_code = models.CharField(max_length=100, unique=True, null=True)
    access_token = models.CharField(max_length=100, unique=True, null=True)
    refresh_token = models.CharField(max_length=100, unique=True, null=True)
    permissions = models.ManyToManyField(Permission)
    code_issued_time = models.DateTimeField(null=True)
    token_issued_time = models.DateTimeField(null=True)

