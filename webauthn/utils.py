# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from functools import wraps

from .authtype import AuthType

def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return HttpResponse('Invalid User. Please authenticate.', status=401)
        func(*args, **kwargs)
    return wrapper

def authenticate(request):
    if request and request.data:
        try:
            authtype = AuthType[request.data['authtype']]
            typespecauth = get_authenticator(authtype)
            return typespecauth(request)
        except KeyError:
            print("Invalid AuthType")
    return None

def password_auth(request):
    user = django_authenticate(
        username=request.data['username'],
        password=request.data['password'])
    if user:
        login(request, user)
    return user

def open_auth(request):
    pass

def jwt_auth(request):
    pass

def web_auth(request):
    pass

def cert_auth(request):
    pass

def get_authenticator(authtype):
    authtypemapping = {
        AuthType.PASSWORD: password_auth,
        AuthType.OAUTH: open_auth,
        AuthType.JWT: jwt_auth,
        AuthType.WEBAUTHN: web_auth,
        AuthType.CERTIFICATE: cert_auth,
    }

    if authtype in authtypemapping:
        return authtypemapping[authtype]
    else:
        pass    # throw error