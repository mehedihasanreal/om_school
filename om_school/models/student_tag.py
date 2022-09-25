from odoo import api, fields, models, _


class StudentTag(models.Model):
    _name = "student.tag"
    _description = "Student Tag"

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True, copy=False)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
            default['sequence'] = 10
        project = super(StudentTag, self).copy(default)
        return project

    _sql_constraints = [
        ('unique_tag_name', 'unique (name, active)', 'your name must be unique'),
        ('check_sequence', 'check (sequence > 0)', 'Sequence should not be zero')
    ]


