import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from dateutil import relativedelta
from datetime import date


class CancelAdmissionWizard(models.TransientModel):
    _name = "cancel.admission.wizard"
    _description = "Cancel Admission Wizard"
    
    @api.model
    def default_get(self, fields):
        res = super(CancelAdmissionWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        if self.env.context.get('active_id'):
            res['admission_id'] = self.env.context.get('active_id')
        return res

    admission_id = fields.Many2one('school.admission', string="Admission", domain=[('state', '=', 'draft')])
    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_school.cancel_days')
        allowed_date = self.admission_id.fill_up_date - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            raise ValidationError(_("Sorry, cannot cancel appointment in before one day"))
        self.admission_id.state = 'cancel'
        return {'type': 'ir.actions.client', 'tag': 'reload'}
