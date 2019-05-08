from flask import Blueprint, request, make_response

bp = Blueprint("common",__name__,url_prefix='/common')

@bp.route('/')
def index():
    return 'common index'


