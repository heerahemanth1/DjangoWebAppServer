# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from json import dumps

from .auth import is_authenticated, authenticate, open_auth,  user_logout
from .enums import AuthType

class AuthenticateUser(APIView):
    def post(self, request):
        errors = AuthenticateUser.validate_post_data(request.data)
        if len(errors) > 0:
            errstr = '\n'.join(errors)
            return HttpResponse(f'Invalid Request Data\n{errstr}', status=400)

        user = authenticate(request=request)
        if user is None:
            return HttpResponse('Authentication Failed', status=401)
        return HttpResponse(user, status=200)

    @classmethod
    def validate_post_data(cls, data):
        errors = []
        if not data.get('auth_type'):
            errors.append('Auth Type unspecified')
        return errors

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
        errors = Authorize.validate_post_data(request.data)
        if len(errors) > 0:
            # ToDo: Improve the error response later
            errstr = '\n'.join(errors)
            return HttpResponse(f'Invalid Request Data\n{errstr}', status=400)

        user = open_auth(request)
        if user:
            return HttpResponse(f'code = {user.get("code")}', status=200)
        return HttpResponse('Authorization Failed', status=401)

    @classmethod
    def validate_post_data(cls, data):
        errors = []
        print(str(AuthType.OAUTH))
        if not data.get('auth_type'):
            errors.append('Auth Type unspecified')
        elif AuthType[data.get('auth_type')] != AuthType.OAUTH:
            errors.append('Wrong Auth Type specified')
        if not data.get('response_type'):
            errors.append('Response Type unspecified')
        if not data.get('user_id'):
            errors.append('User Id unspecified')
        if not data.get('client_id'):
            errors.append('Client Id unspecified')
        return errors

@csrf_exempt
def logout(request):
    user_logout(request)
    return HttpResponse('Successfully logged out', status=200)

