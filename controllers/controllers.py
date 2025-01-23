from urllib.parse import urlparse
from urllib.parse import urlparse, parse_qs
from odoo.exceptions import AccessError
from odoo import api, http, modules
from odoo.http import request, Response
import jwt
import datetime
from werkzeug.wrappers import Response
import json
from odoo import http
from odoo.http import request


class SchoolManagement(http.Controller):

    @http.route('/school_management/banner', type='json', auth='user')
    def get_banner(self):
        banner_html = """
        <div class="o_kanban_view_banner" style="background-color: #f8d7da; color: #721c24; padding: 10px; border: 1px solid #f5c6cb; border-radius: 5px; text-align: center; width: 100%; box-sizing: border-box;">
            <span style="font-weight: bold;">Important Notification:</span> School Management System Update
        </div>
        """
        return {'html': banner_html}



