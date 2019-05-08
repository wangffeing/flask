from .views import bp
from flask import session, g, render_template
from ..models import User
import config

@bp.before_request
def before_request():
    if config.USER_ID in session:
        user_id = session.get(config.USER_ID)
        user = User.query.get(user_id)
        if user:
            g.user = user

@bp.errorhandler
def page_not_found():
    return render_template('front/front_404.html')
