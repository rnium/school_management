from odoo import models, fields, api

class Library(models.Model):
    _name = 'school_management.library'
    _description = 'Library'

    name = fields.Char()
    school_id = fields.Many2one('school_management.school', string='School')
    has_delete_permission = fields.Boolean(compute='_compute_delete_permission')

    def _compute_delete_permission(self):
        for record in self:
            record.has_delete_permission = self.env.user.has_group('school_management.group_school_management_admin')
