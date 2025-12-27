# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponse
from functools import wraps

from .authtype import AuthType
from .utils import generate_auth_code

# ### private objects

def _get_authenticator(authtype):
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


# ### public objects

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
            typespecauth = _get_authenticator(authtype)
            user = typespecauth(request)
            if user:
                login(request, user)
            return user
        except KeyError:
            print("Invalid AuthType")
    return None

def password_auth(request):
    user = django_authenticate(
        username=request.data['username'],
        password=request.data['password'])
    return user

def open_auth(request):
    response_type = request.data.get('response_type')
    response_type = lower(response_type)
    if response_type == "token":
        pass    # return access token
    elif response_type == "code":
        # ToDo: refactor this to authenticate user
        # and then generate code
        # and then save the code into the database
        if request.data.get('password'):
            if user = password_auth(request):
                user['authorization_code'] = generate_auth_code(user)
                return user
        elif request.data.get('session'):
            if request.session.get_expiry_age() > 60:
                user = request.user
                user['authorization_code'] = generate_auth_code(user)
                return user
    return

def jwt_auth(request):
    pass

def web_auth(request):
    pass

def cert_auth(request):
    pass

def user_logout(request):
    logout(request)

