from odoo import api, fields, models


class SchoolExam(models.Model):
    _name = "school.exam"
    _description = "School Exam"
    _rec_name = "teacher_id"
    _log_access = False
    _order = 'sequence,id'

    teacher_id = fields.Many2one('res.users', string="Teacher")
    exam_name = fields.Char(string="Exam Name")
    reference_record = fields.Reference(selection=[('school.student', 'Student'),
                                                   ('school.admission', 'Admission')], string="Record")
    sequence = fields.Integer(string="Sequence", default="10")

    @api.model
    def name_create(self, name):
        return self.create({'exam_name': name}).name_get()[0]

