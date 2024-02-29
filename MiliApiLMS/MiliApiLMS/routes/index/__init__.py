from flask import Blueprint

index_bp = Blueprint('index_pb', __name__, template_folder='templates', url_prefix='/')

from . import index
