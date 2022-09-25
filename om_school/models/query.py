from odoo import api, fields, models


class OdooQuery(models.Model):
    _name = "odoo.query"
    _description = "Odoo Query"

    python_1 = fields.Text(string="Code")
    result_1 = fields.Text(string="Result")




