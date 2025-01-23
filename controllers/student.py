from odoo import api, http, modules
from odoo.http import request
import jwt
import datetime
import json
from ._utils import requires_auth, check_access


class StudentApi(http.Controller):

    @http.route('/student/all', type='json', auth="public", csrf=False, website=False, cors='*', methods=['GET'])
    def get_all_students(self, **kw):
        students = request.env['school_management.student'].sudo().search([])
        res = {'students': students.read(['name', 'age', 'roll_number'])}
        return res

    @http.route('/student/paginated', type='json', auth="none")
    def get_paginated_students(self, **kw):
        try:
            page = kw.get('page', 1)
            limit = kw.get('limit', 10)
        except ValueError:
            return {'success': False, 'message': 'Invalid page or limit value'}
        offset = (int(page) - 1) * int(limit)
        students = request.env['school_management.student'].sudo().search([], limit=int(limit), offset=offset)
        total_students = request.env['school_management.student'].sudo().search_count([])
        total_pages = total_students // int(limit) + 1
        res = {
            'total_pages': total_pages,
            'current_page': int(page),
            'students': students.read(['name', 'age', 'roll_number']),
        }
        return {'success': True, 'data': res}

    @http.route('/student/<pk>', type='json', auth="none", csrf=False, website=False, cors='*', methods=['GET'])
    def get_student(self, **kw):
        student = request.env['school_management.student'].sudo().search([('id', '=', kw.get('pk'))])
        if not student:
            return {'success': False, 'message': 'Student not found'}
        student_data = student.read(['name', 'age', 'roll_number'])[0]
        return {'success': True, 'student': student_data}


    @http.route('/student/create', type='json', auth="none", csrf=False, website=False, cors='*', methods=['POST'])
    def create_student(self, **kw):
        try:
            student = request.env['school_management.student'].sudo().create({
                'name': kw.get('name'),
                'age': kw.get('age'),
                'roll_number': kw.get('roll_number')
            })
            return {
                'success': True,
                'message': 'Student created successfully!',
                'student': student.read(['name', 'age', 'roll_number'])[0]
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @http.route('/student/update/<id>', type='json', auth="none", csrf=False, website=False, cors='*', methods=['POST'])
    def update_student(self, **kw):
        access_res = check_access('school_management.student', 'write')
        if not access_res.get('success'):
            return access_res
        try:
            student = request.env['school_management.student'].sudo().search([('id', '=', kw.get('id'))])
            if not student:
                return {'success': False, 'message': 'Student not found'}
            data = {}
            for key in kw:
                if key != 'id':
                    data[key] = kw[key]
            student.write(data)
            return {
                'success': True,
                'message': 'Student updated successfully!',
                'student': student.read(['name', 'age', 'roll_number'])[0]
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    @http.route('/student/delete/<id>', type='json', auth="none", csrf=False, website=False, cors='*', methods=['DELETE'])
    @requires_auth
    def delete_student(self, **kw):
        access_res = check_access('school_management.student', 'unlink')
        if not access_res.get('success'):
            return access_res
        try:
            student = request.env['school_management.student'].sudo().search([('id', '=', kw.get('id'))])
            if not student:
                return {'success': False, 'message': 'Student not found'}
            student.unlink()
            return {'success': True, 'message': 'Student deleted successfully!'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
