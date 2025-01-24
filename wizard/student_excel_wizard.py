from odoo import models, fields, api


class StudentExcelWizard(models.TransientModel):
    _name = 'student.excel.wizard'
    _description = 'Student Excel Wizard'

    excel_file = fields.Binary(string='Excel File', required=True)
    file_name = fields.Char(string='File Name', required=True)