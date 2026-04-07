# -*- coding: utf-8 -*-
from django.db import transaction
import hashlib
import random
import string

from .errors import MaxTriesReachedError
from .models import Authorization


# ### private objects

def _verify_unique_auth_code(code):
    with transaction.atomic():
        if Authorization.objects.filter(auth_code=code):
            return False
        return True

def _verify_unique_token(token):
    with transaction.atomic():
        if Authorization.objects.filter(access_token=token):
            return False
        return True

def _any_existing_tokens(userid, clientid):
    return Authorization.objects.filter(user_id=userid, client_id=clientid)

# ### public objects

def generate_auth_code(user):
    code_length = 20
    max_tries = 10
    lcv = 0
    while lcv < max_tries:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=code_length))
        if _verify_unique_auth_code(code):
            return code
        lcv += 1
    raise MaxTriesReachedError(
        "Authorization Code Generation Failed",
        f"Unable to generate unique code, number of tries reached maximum limit of {max_tries}")

def generate_token(user, client, permissions, validity_in_days):
    # ToDo: Check for existing tokens for same user & client
    token = _any_existing_tokens(user.id, client.id)
    if token:
        return token
    scope = ','.join(permissions)
    token = '::'.join((user.id, user.name, scope, str(validity_in_days))).encode('UTF-8')
    token = hashlib.sha256(token).hexdigest()
    return token


def testgt():
    user = { id: '10', name: 'ted' }
    client = { id: '2' }
    permissions = ( 'can_read', 'can_update' )
    validity = 10
    generate_token(user, client, permissions, validity)

if __name__ == '__main__':
    testgt()

