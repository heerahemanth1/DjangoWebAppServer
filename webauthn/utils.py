# -*- coding: utf-8 -*-

def generate_auth_code(user):
    code_length = 20
    import random
    import string
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=code_length))
    # ToDo - Verify generated code is not already in db
    # check in a loop if duplicate with iter limit
    # throw error if unable to generate unique code
    return code

