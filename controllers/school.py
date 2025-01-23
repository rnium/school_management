from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.http import route, request
from odoo.tools import groupby as groupbyelem
from operator import itemgetter
from werkzeug.utils import secure_filename
import base64
from odoo import _

class SchoolPortal(CustomerPortal):

    @route('/my/school', auth='user', website=True)
    def school(self, **kw):
        schools = request.env['school_management.school'].sudo().search([])
        return request.render(
            'school_management.portal_school_list_view_template',
            {
                'schools': schools,
                'page_name': 'schools',
            }
        )

    @route('/my/school/create', auth='user', website=True)
    def create_school(self, **kw):
        success_messages = []
        error_messages = []
        created = False
        if request.httprequest.method == 'POST':
            keys = ['name', 'school_code', 'address', 'email', 'website']
            vals = {key: kw.get(key) for key in keys if kw.get(key)}
            if not vals.get('name'):
                error_messages.append('Please enter school name')
            if not vals.get('address'):
                error_messages.append('Please enter school address')
            if not vals.get('email'):
                error_messages.append('Please enter email')
            if logo:=request.httprequest.files.get('logo'):
                try:
                    vals['logo'] = base64.b64encode(logo.read())
                except Exception as e:
                    error_messages.append('Error while uploading logo. Error: %s' % str(e))
            if len(error_messages) == 0:
                new_school_id = request.env['school_management.school'].create(vals)
                if new_school_id:
                    success_messages.append('School created successfully')
                    created = True
                else:
                    error_messages.append('Error while creating school')
        return request.render(
            'school_management.school_create_template',
            {
                'page_name': 'create_school',
                'success_messages': success_messages,
                'error_messages': error_messages,
                'created': created,
            }
        )

    @route('/my/school/edit/<int:school_id>', auth='user', website=True)
    def edit_school(self, school_id, **kw):
        success_messages = []
        error_messages = []
        school = request.env['school_management.school'].sudo().search([('id', '=', school_id)])
        updated = False
        if request.httprequest.method == 'POST':
            keys = ['name', 'school_code', 'address', 'email', 'website']
            vals = {key: kw.get(key) for key in keys if kw.get(key)}
            if not vals.get('name'):
                error_messages.append('Please enter school name')
            if not vals.get('address'):
                error_messages.append('Please enter school address')
            if not vals.get('email'):
                error_messages.append('Please enter email')
            if logo:=request.httprequest.files.get('logo'):
                try:
                    vals['logo'] = base64.b64encode(logo.read())
                except Exception as e:
                    error_messages.append('Error while uploading logo. Error: %s' % str(e))
            if len(error_messages) == 0:
                school.write(vals)
                success_messages.append('School updated successfully')
                updated = True
        return request.render(
            'school_management.school_edit_template',
            {
                'school': school,
                'page_name': 'edit_school',
                'success_messages': success_messages,
                'error_messages': error_messages,
                'updated': updated,
            }
        )

    @route('/my/school/<int:school_id>', auth='user', website=True)
    def school_detail(self, school_id, **kw):
        school = request.env['school_management.school'].sudo().search([('id', '=', school_id)])
        return request.render(
            'school_management.portal_school_details_view_template',
            {
                'school': school,
                'page_name': 'school_detail',
            }
        )

    @route(['/my/school/<int:school_id>/students', '/my/school/<int:school_id>/students/page/<int:page>'], auth='user', website=True)
    def school_students(self, school_id, page=1, sortby=None, search=None, search_in=None, groupby='standard', **kw):
        limit = 7
        school = request.env['school_management.school'].sudo().search([('id', '=', school_id)])
        searchbar_sortings = {
            'name': {'label': 'Name', 'order': 'name'},
            'age': {'label': 'Age', 'order': 'age'},
            'standard': {'label': 'Standard', 'order': 'standard'},
        }
        groupby_list = {
            'standard': {'input': 'standard', 'label': _('Standard')},
            'version': {'input': 'version', 'label': _('Version')},
        }
        group_by_student = groupby_list.get(groupby, {})
        if not search_in:
            search_in = 'name'
        order = searchbar_sortings[sortby]['order'] if sortby else 'name'
        search_list = {
            'all': {'label': _('All'), 'input': 'all', 'domain': []},
            'name': {'label': _('Name'), 'input': 'name', 'domain': [('name', 'ilike', search)]},
            'standard': {'label': _('Standard'), 'input': 'standard', 'domain': [('standard', '=', search)]},
        }
        if not sortby:
            sortby = 'standard'
        search_domain = [('school_id', '=', school_id)]
        search_domain += search_list[search_in]['domain']
        student_count = request.env['school_management.student'].sudo().search_count(search_domain)
        pager = portal_pager(
            url='/my/school/%s/students' % school_id,
            url_args={'school_id': school_id, 'sortby': sortby, 'search_in': search_in, 'search': search},
            total=student_count,
            page=page,
            step=limit,
        )
        students = request.env['school_management.student'].sudo().search(search_domain, limit=limit, offset=pager['offset'], order=order)
        if groupby_list[groupby]['input']:
            student_group_list = [{group_by_student['input']: i, 'students': list(j)} for i, j in groupbyelem(students, itemgetter(group_by_student['input']))]
        else:
            student_group_list = [{'students': students}]
        return request.render(
            'school_management.portal_school_students_view_template',
            {
                'school': school,
                'students': students,
                'page_name': 'school_students',
                'pager': pager,
                'sortby': sortby,
                'searchbar_sortings': searchbar_sortings,
                'searchbar_inputs': search_list,
                'search_in': search_in,
                'search': search,
                'group_students': student_group_list,
                'default_url': '/my/school/%s/students' % school_id,
                'groupby': groupby,
                'searchbar_groupby': groupby_list,
            }
        )

    @route('/my/student/<int:student_id>', auth='user', website=True)
    def student_detail(self, student_id, **kw):
        student = request.env['school_management.student'].sudo().search([('id', '=', student_id)])
        student_ids = request.env['school_management.student'].sudo().search([('school_id', '=', student.school_id.id)])
        student_index = student_ids.ids.index(student_id)
        student_count = len(student_ids)
        prev_student_id = student_ids[student_index - 1].id if student_index > 0 else False
        next_student_id = student_ids[student_index + 1].id if student_index < student_count - 1 else False
        res = request.render(
            'school_management.student_detailed_view',
            {
                'student': student,
                'school': student.school_id,
                'page_name': 'student_details',
                'prev_record': f"/my/student/{prev_student_id}" if prev_student_id else False,
                'next_record': f"/my/student/{next_student_id}" if next_student_id else False,
            }
        )
        return res

    @route(['/my/school/report/<model(school_management.school):school_id>'], type='http', auth='user', website=True)
    def school_report(self, school_id, **kw):
        return self._show_report(
            model=school_id,
            report_type="pdf",
            report_ref='school_management.report_school_template',
            download=True
        )
