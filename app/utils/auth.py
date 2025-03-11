from functools import wraps

from flask import request

from app.config import Config


def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return {"error": "Token is missing"}, 401

            token = auth_header.split(" ")[1]
            user = Config.ACCESS_TOKENS.get(token)

            if not user:
                return {"error": "Invalid token"}, 403

            if role and user["role"] != role:
                return {"error": "Unauthorized"}, 403

            if args and hasattr(args[0], "__class__"):
                return f(args[0], user, *args[1:], **kwargs)

        return decorated_function

    return decorator
