from odoo import models, fields, api


class SudentDataUpdateWizard(models.TransientModel):
    _name = 'student.data.update.wizard'

    weight_in_kg = fields.Float(string='Weight in KG')
    weight_in_pounds = fields.Float(string='Weight in Pounds')

    def update_weight(self):
        active_ids = self.env.context.get('active_ids', [])
        active_model = self.env.context.get('active_model')
        if active_ids:
            students = self.env[active_model].browse(active_ids)
            students.write({
                'weight_in_kg': self.weight_in_kg,
                'weight_in_pounds': self.weight_in_pounds
            })
