from flask_login import current_user, login_required
from flask import flash, abort
from functools import wraps

def role_required(*roles):
    """Custom decorator to restrict routes to specific roles."""
    def decorator(f):
        @wraps(f)
        @login_required
        def wrapper(*args, **kwargs):
            if not hasattr(current_user, 'role') or current_user.role not in roles:
                flash("Access restricted to authorized users.", "danger")
                return abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Usage example for admin-only routes
admin_required = role_required('admin')