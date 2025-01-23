from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Book(models.Model):
    _name = 'school_management.book'
    _description = 'Book'

    name = fields.Char()
    author = fields.Char()
    edition = fields.Char()
    isbn = fields.Char()
    library_id = fields.Many2one('school_management.library', string='Library')

    @api.constrains('isbn')
    def _check_isbn(self):
        for record in self:
            if self.search_count([('isbn', '=', record.isbn)]) > 1:
                raise ValidationError('ISBN must be unique.')