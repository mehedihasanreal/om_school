from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import random


class SchoolAdmission(models.Model):
    _name = "school.admission"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "School Admission"
    _rec_name = "name"
    _order = 'id desc'

    name = fields.Char(string="Sequence", default="New")
    student_id = fields.Many2one('school.student', string="Student", ondelete="restrict")
    gender = fields.Selection(related='student_id.gender', readonly=False)
    ref = fields.Char(string="Reference")
    email = fields.Char(string="Email", related='student_id.email', readonly=False)
    admission_time = fields.Datetime(string="Admission Time", default=fields.Datetime.now)
    fill_up_date = fields.Date(string="Fill Up Date", default=fields.Date.context_today)
    transcription = fields.Text(string="Transcription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High')], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultant', 'In Consultant'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], default="draft", string="Status", required=True, tracking=True)
    teacher_id = fields.Many2one('res.users', string="Teacher", tracking=True)
    library_line_ids = fields.One2many('admission.library.line', 'admission_id', string="Library Line")
    hide_sales_price = fields.Boolean(string="Hide Sales Price")
    exam_id = fields.Many2one('school.exam', string="Exam")
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    duration = fields.Float(string="Duration")
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')
    amount_total = fields.Monetary(string="Total", compute='_compute_amount_total', currency_field='currency_id')

    @api.onchange("student_id")
    def onchange_student_id(self):
        self.ref = self.student_id.ref

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can delete admission only in 'Draft' state"))
        return super(SchoolAdmission, self).unlink()

    def action_test(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.facebook.com/',
        }

    def action_notification(self):
        action = self.env.ref('om_school.action_school_admission')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('The following replenishment order has been generated'),
                'message': '%s',
                'links': [{
                    'label': self.student_id.name,
                    'url': f'#action={action.id}&id={self.id}&model=school.admission',
                }],
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'school.student',
                    'res_id': self.student_id.id,
                    'views': [(False, 'form')]
                }
            }
        }

    def action_share_whatsapp(self):
        if not self.student_id.phone:
            raise ValidationError(_("Phone number is missing in student record!"))
        message = 'Hi %s, Your admission no. is %s' % (self.student_id.name, self.name)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.student_id.phone, message)
        self.message_post(body=message, subject='Whatsapp Message')
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_send_mail(self):
        template = self.env.ref("om_school.admission_mail_template")
        for rec in self:
            if rec.student_id.email:
                template.send_mail(rec.id, force_send="True")

    def action_in_consultant(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultant'

    def action_done(self):
        for rec in self:
            rec.state = 'done'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Clicked Successfully',
                'type': 'rainbow_man',
            }
        }

    def action_cancel(self):
        action = self.env.ref('om_school.action_cancel_admission').read()[0]
        return action

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultant':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    @api.depends('library_line_ids')
    def _compute_amount_total(self):
        for rec in self:
            amount_total = 0
            for line in rec.library_line_ids:
                amount_total += line.price_subtotal
            rec.amount_total = amount_total

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('school.admission')
        res = super(SchoolAdmission, self).create(vals)

        sl_no = 0
        for line in res.library_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res
    
    def write(self, values):
        res = super(SchoolAdmission, self).write(values)
        sl_no = 0
        for line in self.library_line_ids:
            sl_no += 1
            line.sl_no = sl_no
        return res


class AdmissionLibraryLine(models.Model):
    _name = "admission.library.line"
    _description = "Admission Library Line"

    sl_no = fields.Integer(string="Sl No.")
    product_id = fields.Many2one('product.product', required=True)
    price = fields.Float(related='product_id.list_price', digits='Product Price')
    qty = fields.Integer(string="Quantity", default="1")
    admission_id = fields.Many2one('school.admission', string="Admission")
    currency_id = fields.Many2one('res.currency', related='admission_id.currency_id')
    price_subtotal = fields.Monetary(string="Subtotal", compute='_compute_price_subtotal',
                                     currency_field='currency_id')

    @api.depends('price', 'qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price * rec.qty

