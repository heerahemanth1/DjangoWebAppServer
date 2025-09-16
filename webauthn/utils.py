# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps

def is_authenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            return HttpResponse('Invalid User. Please authenticate.', status=401)
        func(*args, **kwargs)
    return wrapper