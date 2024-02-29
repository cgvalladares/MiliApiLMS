from flask import Blueprint
finger_bp=Blueprint('finger_bp', __name__, url_prefix='/finger')
from . import fingerServices

