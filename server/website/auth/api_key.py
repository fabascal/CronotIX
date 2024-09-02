from flask import request, jsonify, current_app
from functools import wraps
from website.auth.models import User
from website.home.models import Assistants, AssistantsApiKey

API_KEYS = {
    "user1": "key1",
    "user2": "key2"
}

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('USER-ID') or not request.headers.get('API-KEY'):
            return jsonify({"message": "Missing headers"}), 403
        API_KEYS = {}
        user_id = request.headers.get('USER-ID')
        api_key = request.headers.get('API-KEY')
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({"message": "Invalid user ID"}), 403
        for assistant in user.assistants:
            API_KEYS[assistant.name] = assistant.apikey.apikey
        if api_key and api_key in API_KEYS.values():
            return f(*args, **kwargs)
        else:
            return jsonify({"message": "Invalid or missing API key"}), 403
    return decorated_function
