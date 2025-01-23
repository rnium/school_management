from odoo import models, fields, api

class ResConfigSettingSchool(models.TransientModel):
    _inherit = 'res.config.settings'

    max_number_of_students = fields.Integer(string='Max Number of Students', config_parameter='school_management.number_of_students')
    max_student_age = fields.Integer(string='Maximum Student Age', config_parameter='school_management.max_student_age')