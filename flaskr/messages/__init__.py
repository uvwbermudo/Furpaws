from flask import Blueprint

msgs = Blueprint('msgs', __name__)

from . import controller