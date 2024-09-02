# -*- encoding: utf-8 -*-
"""
Copyright (c) 2024 - present 
"""

from flask import Blueprint

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)