from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class SchoolStudent(models.Model):
    _name = "school.student"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Student"

    name = fields.Char(string='Name', tracking=True)
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(string='Age', compute="_compute_age", inverse="_inverse_compute_age",
                         search="_search_age", tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True)
    ref = fields.Char(string="Reference", tracking=True)
    active = fields.Boolean(string='Active', default='True')
    admission_id = fields.Many2one('school.admission', string="Admission ID")
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('student.tag', string="Tags")
    admission_count = fields.Integer(string="Admission Count", compute="_compute_admission_count", store=True)
    admission_ids = fields.One2many('school.admission', 'student_id', string="Admissions")
    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status")
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Birthday?", compute="_compute_is_birthday")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    website = fields.Char(string="Website")

    # admission count by "search_count"
    # @api.depends('admission_ids')
    # def _compute_admission_count(self):
    #     for rec in self:
    #         rec.admission_count = self.env['school.admission'].search_count([('student_id', '=', rec.id)])

    # admission count by "read_group" method
    @api.depends('admission_ids')
    def _compute_admission_count(self):
        admission_group = self.env['school.admission'].read_group(domain=[('state', '=', 'done')],
                                                                  fields=['student_id'], groupby=['student_id'])
        for admission in admission_group:
            student_id = admission.get('student_id')[0]
            student_rec = self.browse(student_id)
            student_rec.admission_count = admission['student_id_count']
            self -= student_rec
        self.admission_count = 0

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Date of Birth is not acceptable"))

    @api.ondelete(at_uninstall=False)
    def _check_admissions(self):
        for rec in self:
            if rec.admission_ids:
                raise ValidationError(_("You can not delete patient with admissions"))

    # overriding create method
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('school.student')
        return super(SchoolStudent, self).create(vals)
    
    def write(self, vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('school.student')
        return super(SchoolStudent, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        for rec in self:
            today = date.today()
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 0

    @api.depends('age')
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    def name_get(self):
        student_list = []
        for record in self:
            name = '[' + record.ref + ']' + ' ' + record.name
            student_list.append((record.id, name))

        return student_list

    def action_test(self):
        print("clicked!!!!!!!")
        return

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def actions_view_admissions(self):
        return {
            'name': _('Admissions'),
            'res_model': 'school.admission',
            'view_mode': 'list,form',
            'target': 'current',
            'context': {'default_student_id': self.id},
            'domain': [('student_id', '=', self.id)],
            'type': 'ir.actions.act_window',
        }