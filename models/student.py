from odoo import models, fields, api
from odoo.exceptions import UserError
import time


class Student(models.Model):
    _name = 'school_management.student'
    _description = 'Student'
    _inherit = 'base.person'
    _sql_constraints = [
        ('unique_roll_number', 'unique(roll_number,standard)', 'Roll number must be unique.')
    ]
    _order = 'roll_number desc, standard asc'

    school_id = fields.Many2one('school_management.school', string='School')
    roll_number = fields.Char(copy=False)
    standard = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                                 ('8', '8'), ('9', '9'), ('10', '10')], copy=False)
    section = fields.Selection([('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'),])
    version = fields.Selection([('Bangla', 'Bangla'), ('English', 'English')])
    admission_date = fields.Date(string='Admission Date')
    group = fields.Selection([('Science', 'Science'), ('Commerce', 'Commerce'), ('Arts', 'Arts')])
    weight_in_kg = fields.Float()
    weight_in_pounds = fields.Float()
    parent_id = fields.Many2one('school_management.parent', string='Parent')
    active = fields.Boolean(default=True)
    parent_name = fields.Char(related='parent_id.name', string='Parent Name', store=True)
    result_ids = fields.One2many('school_management.result', 'student_id', string='Results')
    graduated = fields.Boolean(string='Graduated', default=False)
    # total_weight_with_loop = fields.Float(
    #     compute='_compute_total_weight_with_loop', string='Total Weight (Loop)'
    # )
    # total_weight_with_read_group = fields.Float(
    #     compute='_compute_total_weight_with_read_group', string='Total Weight (Read Group)'
    # )

    def send_birthday_email(self):
        self.env.ref(
            'school_management.email_template_model_school_management_student_birthday'
        ).send_mail(self.id, force_send=True)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Email Sent',
                'message': 'Birthday email has been sent to the student.',
                'sticky': False,
            }
        }

    def generate_excel_report(self):
        self.ensure_one()
        report_wizard = self.env['student.report.wizard'].create({'student_id': self.id})
        return report_wizard.generate_excel_report()




    @api.onchange('weight_in_kg')
    def _onchange_weight_in_kg(self):
        if self.weight_in_kg:
            self.weight_in_pounds = self.weight_in_kg * 2.20462

    # This method is invoked by the unlink method while deleting a record of this model
    @api.ondelete(at_uninstall=False)
    def _unlink_if_no_result(self):

        x = self._read_group([('standard', '=', 9)], groupby=['section'], aggregates=['age:sum'],
                            having=[('age:sum', '>', 15)], offset=0, limit=None, order=None)

        y = self.read_group([('standard', '=', 9)], fields=['age:sum'], groupby=['section'], offset=0, limit=None)

        for record in self:

            z = record.search_fetch([('age', '>', 15)], ['name', 'age'])

            if record.school_id:
                raise UserError('Cannot delete a student with school.')

    def mark_as_graduated(self):
        error_list = []
        for student in self:
            if student.graduated:
                error_list.append(student.name)
            else:
                student.update({'graduated': True})
        if error_list:
            raise UserError(f'The following students are already graduated: {", ".join(error_list)}')
        action = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'Students marked as graduated successfully.',
                'sticky': False,
            }
        }
        return action

    @api.model
    def _assign_group(self, *args, **kwargs):
        section_mapping = {
            'A': ('Science', 'English'),
            'B': ('Commerce', 'English'),
            'C': ('Arts', 'English'),
            'D': ('Science', 'Bangla'),
            'E': ('Commerce', 'Bangla'),
            'F': ('Arts', 'Bangla')
        }

        for student in self:
            if student.standard in ['9', '10']:
                if student.section in section_mapping:
                    student.group, student.version = section_mapping[student.section]

    def action_on_click(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Student',
            'res_model': 'school_management.student',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }

    def action_all_results(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Results',
            'res_model': 'school_management.result',
            'view_mode': 'tree,form',
            'domain': [('student_id', '=', self.id)],
            'target': 'current',
        }

    def show_update_popup(self):
        action = self.env.ref('school_management.student_data_update_wizard_action').read()[0]
        return action

    # def write(self, vals):
    #     if results:=vals.get('result_ids'):
    #         num_courses = len(results)
    #         total_marks = sum([result[2]['marks'] for result in results])
    #         marks_per_course = total_marks / num_courses
    #         if marks_per_course > 100:
    #             raise UserError('Total marks per course per student cannot exceed 100.')
    #     super(Student, self).write(vals)



