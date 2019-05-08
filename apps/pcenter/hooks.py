from .views import bp
import config
from flask import session, g, render_template
from ..models import User, Permission

@bp.before_request
def before_request():
    if config.USER_ID in session:
        user_id = session.get(config.USER_ID)
        user = User.query.get(user_id)
        if user:
            g.user = user

@bp.context_processor
def context_processor():
    return {'Permission': Permission}