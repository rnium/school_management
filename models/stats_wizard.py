from email.policy import default

from odoo import models, fields, api
import time

class StudentWeightWizard(models.TransientModel):
    _name = 'student.weight.wizard'
    _description = 'Student Weight Wizard'

    standard = fields.Selection([('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
                                 ('8', '8'), ('9', '9'), ('10', '10')])


    def _compute_total_weight_with_loop(self):
        total_weight = 0.0
        all_students = self.env['school_management.student'].search([('standard', '=', self.standard)])
        for rec in all_students:
            student_record = self.env['school_management.student'].search([('id', '=', rec.id)])
            total_weight += student_record.weight_in_kg
        return total_weight


    def _compute_total_weight_with_read_group(self):
        total_weight = self.env['school_management.student'].read_group(
            [('id', '!=', False), ('standard', '=', self.standard)],
            ['weight_in_kg:sum'],
            []
        )[0].get('weight_in_kg', 0.0)
        return total_weight

    def action_compute_total_weight_in_loop(self):
        total_weight = self._compute_total_weight_with_loop()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Total Weight Calculated',
                'message': f'Total weight calculated using loop is {total_weight}.',
                'sticky': False,
            }
        }

    def action_compute_total_weight_in_read_group(self):
        total_weight = self._compute_total_weight_with_read_group()
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Total Weight Calculated',
                'message': f'Total weight calculated using read group is {total_weight}.',
                'sticky': False,
            }
       }