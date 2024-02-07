from flask import current_app as app
from flask import Blueprint

bp = Blueprint('bp', __name__)

@bp.route('/')
def hello():
    return "Hello, Everyone!"
