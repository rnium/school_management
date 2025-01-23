from odoo import http
from odoo.http import request
import datetime
import jwt


class CustomAuth(http.Controller):
    @http.route('/login', type='json', auth="none", csrf=False, website=False, cors='*', methods=['POST'])
    def signin(self, **kw):
        try:
            user_id = request.session.authenticate(request.params['db'], request.params['login'],
                                                   request.params['password'])

            if not user_id:
                return {'success': False, 'message': 'Authentication failed: Invalid login or password.'}

            payload = {
                'user_id': user_id,
                'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=240)
            }
            secret_key = 'your_secret_key'
            token = jwt.encode(payload, secret_key, algorithm='HS256')

            return {
                'success': True,
                'message': 'Sign in successful!',
                'id': user_id,
                'result': {
                    'token': token
                }
            }

        except Exception as e:
            return {'success': False, 'message': str(e)}