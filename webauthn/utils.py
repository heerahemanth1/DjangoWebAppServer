# -*- coding: utf-8 -*-
from django.db import transaction
import random
import string

from .models import Authorization


# ### private objects

def _verify_unique_auth_code(code):
    with transaction.atomic():
        if Authorization.objects.filter(auth_code=code):
            return False
        return True

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
    # ToDo - throw error if unable to generate unique code
    return code

