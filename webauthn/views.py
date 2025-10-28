# -*- coding: utf-8 -*-
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from json import dumps

from .utils import is_authenticated, authenticate

class AuthenticateUser(APIView):
    def post(self, request):
        print(request.method)
        user = authenticate(request=request)
        if user is None:
            return HttpResponse('Authentication Failed', status=401)
        return HttpResponse(user, status=200)

class CreateUser(APIView):
    def post(self, request):
        email = request.data['email']
        username = request.data['username']
        password = request.data['password']
        # validate(username, email, password)
        user = User.objects.create_user(username, email, password)
        if user is None:
            return HttpResponse('User Creation Failed', status=500)
        return HttpResponse('Success', status=200)
