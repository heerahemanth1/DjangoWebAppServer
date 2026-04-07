# -*- coding: utf-8 -*-
from enum import Enum

class AuthType(Enum):
    PASSWORD = 2736472
    OAUTH = 9237462
    JWT = 3430424
    PASSKEY = 5632349
    CERTIFICATE = 3746423


class GrantTypes(Enum):
    AUTHORIZATION_CODE = 0
    IMPLICIT = 1
    RES_OWNER_CRED = 2
    CLIENT_CRED = 3

