from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Result(models.Model):
    _name = 'school_management.result'
    _description = 'Result'
    _inherits = {'school_management.student': 'student_id'}

    student_id = fields.Many2one('school_management.student', string='Student', required=True, ondelete='cascade',
                                 context={'active_test': False}
                                 )
    course_id = fields.Many2one('school_management.course', string='Course', required=True)
    grade = fields.Selection([('a+', 'A+'), ('a', 'A'), ('a-', 'A-'), ('b+', 'B+'), ('b', 'B'), ('b-', 'B-'),])
    marks = fields.Float()
    result_date = fields.Date(string='Result Date', default=fields.Date.today)

    @api.constrains('student_id', 'course_id')
    def _check_unique_result_per_student_per_course(self):
        for record in self:
            if self.search_count([('student_id', '=', record.student_id.id), ('course_id', '=', record.course_id.id)]) > 1:
                raise ValidationError('Result must be unique per student per course.')

    @staticmethod
    def _check_marks_per_course(num_courses, total_marks):
        max_marks_per_course = 100
        if num_courses <= 1:
            return
        marks_per_course = total_marks / num_courses
        if marks_per_course > max_marks_per_course:
            raise ValidationError('Total marks per course per student cannot exceed %d.\nCurrent total marks: %s for %d courses!' % (max_marks_per_course, total_marks, num_courses))

    @api.onchange('marks')
    def _check_student_total_marks(self):
        for record in self:
            if record.marks < 0 or record.marks > 150:
                raise ValidationError('Marks must be between 0 and 150.')
            results = record.student_id.result_ids
            existing_records = results.filtered(lambda res: res.id.origin)
            virtual_records = results.filtered(lambda res: hasattr(res.id, 'ref') and isinstance(res.id.ref, str))
            in_memory_records = results.filtered(lambda res: hasattr(res.id, 'ref') and res.id.ref is None)
            num_results = len(existing_records) + len(virtual_records)
            total_marks = sum(existing_records.mapped('marks'))
            for v_rec in virtual_records:
                in_memory_records_for_v_rec = in_memory_records.filtered(lambda rec: rec.course_id.id == v_rec.course_id.id)
                if len(in_memory_records_for_v_rec) > 0:
                    total_marks += in_memory_records_for_v_rec[0].marks
                else:
                    total_marks += v_rec.marks
            self._check_marks_per_course(num_results, total_marks)




