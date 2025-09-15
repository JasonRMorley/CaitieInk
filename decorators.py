from functools import wraps
from flask import session, redirect, url_for


def login_required(role=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if "user" not in session:
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                return "Forbidden", 403
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
