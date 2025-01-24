from odoo import models, fields, api
from . import utils
from odoo.exceptions import UserError
from base64 import encodebytes


class StudentReportWizard(models.TransientModel):
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'
    _rec_name = 'display_name'

    student_id = fields.Many2one('school_management.student', string='Student')
    preview_html = fields.Html('Report', readonly=True)

    def _compute_display_name(self):
        for record in self:
            record.display_name = 'Generate Student Report'

    def generate_report_preview(self):
        self.ensure_one()
        data = self._get_student_data()
        self.preview_html = utils.generate_html_string(data)

    def _get_student_data(self):
        student = self.student_id
        results_data = [
            {
                'course': result.course_id,
                'marks': result.marks,
                'grade': result.grade,
                'result_date': result.result_date
            }
            for result in student.result_ids
        ]
        return {
            'student': student,
            'results': results_data
        }

    def generate_excel_report(self):
        self.ensure_one()
        data = self._get_student_data()
        if not data['results']:
            raise UserError('No results found for this student')
        excel_file_data = utils.generate_excel_file(data)
        wizard_id = self.env['student.excel.wizard'].create(
            {
                'excel_file': encodebytes(excel_file_data),
                'file_name': f'{data["student"].name}_report.xlsx'
            }
        )
        return {
            'name': 'Student Excel Report',
            'type': 'ir.actions.act_window',
            'res_model': 'student.excel.wizard',
            'res_id': wizard_id.id,
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }


