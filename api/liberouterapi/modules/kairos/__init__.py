from liberouterapi import app
from ..module import Module

from flask import Blueprint

# Register a blueprint
#kairos = Blueprint('kairos', __name__)

from .base import *

#kairos.add_url_rule('/health', view_func = health, methods=['GET'])
#kairos.add_url_rule('/status', view_func = status, methods=['GET'])
