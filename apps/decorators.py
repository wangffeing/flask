from flask import session, redirect, url_for, g
from functools import wraps
import config

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if config.USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('front.signin'))
    return inner

def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('front'))
        return inner
    return outter