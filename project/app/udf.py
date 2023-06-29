
from .models import *
import math
import random
import base64
import secrets
import uuid

import json
from django.contrib.auth.hashers import make_password

def check_user_exist(email):
    user_ = user_info.objects.filter(email=email)
    if user_.exists():
        return True, "professional"

    else:        
        return False, "None"
    
# print(check_user_exist("karan22@gmail.com"))
def user_session_create(user_id, session_while):
    global user_token
    if session_while == "added":
        user_token = f"{secrets.token_hex()}{make_password(session_while)}{uuid.uuid4()}"
        UserSessionToken.objects.create(user_id=user_id, token=user_token)

    return user_token


def authenticate_user(user_id, user_token):
    try:
        user_info = UserSessionToken.objects.get(user_id=user_id)
        return True if int(user_info.user_id) == int(
            user_id) and user_info.token == user_token else False
    except:
        return False