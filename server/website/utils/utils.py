from uuid import uuid4
from slugify import slugify

def get_uuid4():
    return uuid4().hex


def GenerateSlug(name):
    return slugify(name)