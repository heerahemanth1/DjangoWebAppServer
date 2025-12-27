# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from json import dumps

from .utils import is_authenticated, authenticate, user_logout

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

class Authorize(APIView):
    # ToDo: Implement GET method later with UI
    def post(self, request):
        rtype = request.data.get('response_type')
        if not rtype:
            return HttpResponse('Response Type unspecified.', status=400)

@csrf_exempt
def logout(request):
    user_logout(request)
    return HttpResponse('Successfully logged out', status=200)

