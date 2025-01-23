from typing import List, Callable
from odoo.http import request, Response
import jwt
from odoo.exceptions import AccessError


def requires_auth(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header:
            return {'success': False, 'message': 'No authorization header provided'}
        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, 'your_secret_key', algorithms=['HS256'])
            request.env.uid = payload['user_id']
        except jwt.ExpiredSignatureError:
            return {'success': False, 'message': 'Token has expired'}
        except jwt.InvalidTokenError:
            return {'success': False, 'message': 'Invalid token'}

        return func(*args, **kwargs)
    return wrapper

def check_access(model_name: str, access_type: str) -> dict:
    model = request.env[model_name]
    try:
        model.check_access_rights(access_type)
    except AccessError:
        return {'success': False, 'message': f'You are not allowed to {access_type} for this model'}
    return {'success': True}