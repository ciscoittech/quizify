# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import Blueprint

bp = Blueprint('home_blueprint' ,__name__,)

from app.home import routes