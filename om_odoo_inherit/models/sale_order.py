from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed Users")

    def action_confirm(self):
        print('success!!!!!!!!!!!!!')
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['field_name'] = self.confirmed_user_id.id
        return invoice_vals


