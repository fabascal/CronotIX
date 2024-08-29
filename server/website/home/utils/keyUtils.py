import secrets
from uuid import uuid4

def get_uuid4():
    return uuid4().hex

def GenerateUUIDStyled(data:str):
    return data + "_" + get_uuid4()


def generate_api_key():
    return secrets.token_urlsafe(32)