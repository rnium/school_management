from email.policy import default

from odoo import models, fields, api, _


class Playground(models.Model):
    _name = 'school_management.playground'
    _description = 'Playground'

    name = fields.Char()
    location = fields.Char()


class SwimmingPool(models.Model):
    _name = 'school_management.swimming_pool'
    _description = 'Swimming Pool'

    name = fields.Char()
    location = fields.Char()
    length = fields.Float()
    width = fields.Float()
    depth = fields.Float()


class School(models.Model):
    _name = 'school_management.school'
    _description = 'School'

    name = fields.Char()
    address = fields.Text()
    contact = fields.Char()
    email = fields.Char()
    website = fields.Char()
    logo = fields.Binary()
    established_date = fields.Date()
    school_code = fields.Char(
        string='School Code',
        required=True,
        copy=False,
        default=lambda self: _('New'),
    )
    teacher_ids = fields.One2many('school_management.teacher', 'school_id', string='Teachers', ondelete='cascade')
    student_ids = fields.One2many('school_management.student', 'school_id', string='Students', ondelete='cascade')
    active = fields.Boolean(default=True)
    playground_ids = fields.Many2many('school_management.playground', string='Playgrounds')
    swimming_pool_ids = fields.Many2many('school_management.swimming_pool', 'school_id', string='Swimming Pools')

    @api.model
    def create(self, vals):
        if vals.get('school_code', _("New")) == _("New"):
            vals['school_code'] = self.env['ir.sequence'].next_by_code('school.code.sequence') or _("New")
        return super(School, self).create(vals)

    def _get_report_base_filename(self):
        return self.name
    def action_school_report(self):
        res_data = {
            'total_teachers': 5,
            'total_students': 55,
        }
        return self.env.ref('school_management.action_report_school').report_action(self)

    def return_action_to_open_student_list(self):
        action = self.env.ref('school_management.school_management_student_action').read()[0]
        action['domain'] = [('school_id', '=', self.id)]
        action['context'] = {'default_school_id': self.id}
        action['views'] = [(self.env.ref('school_management.school_management_student_view_tree').id, 'tree')]
        return action



