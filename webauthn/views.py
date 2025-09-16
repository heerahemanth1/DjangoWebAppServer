# -*- coding: utf-8 -*-
from django.http import HttpResponse
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render

from .utils import is_authenticated

class AuthenticateUser(APIView):
    def post(self, request):
        print(request.method)
        user = authenticate(
            username=request.data['username'],
            password=request.data['password'])
        if user is None:
            return HttpResponse('Authentication Failed', status=401)
        login(request, user)
        return HttpResponse('Success', status=200)
    
    def get(self, request):
        form = AuthenticationForm()
        return render(request)

@login_required
def create_user(self, request):
    if request.method == 'POST':
        email = request.data['email']
        username = request.data['username']
        password = request.data['password']
        # validate(username, email, password)
        user = User.objects.create_user(username, email, password)
        return HttpResponse('Success', status=200)
    elif request.method == 'GET':
        pass
