# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth import login, logout
from django.db import transaction
from django.http import HttpResponse
from functools import wraps

from appserver.settings import DEFAULT_TOKEN_VALIDITY_IN_DAYS
from .enums import AuthType
from .errors import AuthenticationError, AuthorizationCodeGenerationError, MaxTriesReachedError
from .models import Authorization
from .utils import generate_auth_code, generate_token


# ### private objects

# ### public objects

def get_authenticator(authtype):
    authtypemapping = {
        AuthType.PASSWORD: PasswordAuthenticator,
        AuthType.OAUTH: OpenAuthenticator,
        AuthType.JWT: JwtAuthenticator,
        AuthType.PASSKEY: PasskeyAuthenticator,
        AuthType.CERTIFICATE: CertificateAuthenticator,
    }

    if authtype in AuthType.__members__:
        return authtypemapping[AuthType[authtype]]
    else:
        atypestr = '\n'.join(at.name for at in AuthType)
        raise AuthenticationError(
            "Invalid Authentication Type",
            f"Provided Auth Type not in the supported types:\n{atypestr}")


def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return HttpResponse('Invalid User. Please authenticate.', status=401)
        func(*args, **kwargs)
    return wrapper

def user_logout(request):
    logout(request)


class Authenticator:
    def __init__(self, request):
        self.request = request

    def authenticate(self):
        if self.request and self.request.data:
            try:
                authtype = AuthType[self.request.data['auth_type']]
                typespecauth = get_authenticator(authtype)
                user = typespecauth(self.request).authenticate()
                if user:
                    login(self.request, user)
                return user
            except KeyError as err:
                raise AuthenticationError(
                    "Authentication Failed.",
                    "Invalid authentication type specified.") from err
        return None


class PasswordAuthenticator(Authenticator):
    def authenticate(self):
        user = django_authenticate(
            username=self.request.data['username'],
            password=self.request.data['password'])
        return user


class OpenAuthenticator(Authenticator):
    def _create_authorization_entry(self, code, user):
        with transaction.atomic():
            new_oauth = Authorization(
                    user=user,
                    # ToDo: support client later
                    auth_code=code,
                    # ToDo: support permissions later
                    code_issued_time=datetime.utcnow(),
                    )
            new_oauth.save()

    def _update_authorization_entry_with_token(self, token, user):
        with transaction.atomic():
            auth = Authorization.objects.get(user=user)
            if not auth:
                auth = Authorization(
                    user=user,
                    # ToDo: client and permissions
                    token_issued_time=datetime.utcnow(),
                    )
            auth.token = token
            auth.save()

    def _resource_owner_authentication(self):
        user = None
        if self.request.data.get('password'):
            user = PasswordAuthenticator(request).authenticate()
        elif self.request.data.get('session'):
            if self.request.session.get_expiry_age() > 60:
                user = self.request.user
        return user

    def _handle_oauth_code_response(self, user):
        try:
            code = generate_auth_code(user)
            self._create_authorization_entry(code, user)
            return code
        except MaxTriesReachedError as err:
            raise AuthorizationCodeGenerationError(
                "Authorization Code Generation Failed", "") from err

    def _handle_oauth_token_response(self, user):
        permissions = self.request.data.get('permissions')
        client = self.request.data.get('client')
        token = generate_token(user, client, permissions, DEFAULT_TOKEN_VALIDITY_IN_DAYS)
        self._update_authorization_entry_with_token(token, user)
        return token

    def authenticate(self):
        user = self._resource_owner_authentication()
        if not user:
            raise AuthenticationError(
                "Authentication Failed", "Provided credentials were invalid.")
        response_type = self.request.data.get('response_type').lower()
        oauth_result = None
        if response_type == "code":
            oauth_result = self._handle_oauth_code_response(user)
        elif response_type == "token":
            oauth_result = self._handle_oauth_token_response(user)
        return oauth_result


class JwtAuthenticator(Authenticator):
    def authenticate(self):
        pass


class PasskeyAuthenticator(Authenticator):
    def authenticate(self):
        pass


class CertificateAuthenticator(Authenticator):
    def authenticate(self):
        pass

