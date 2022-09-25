# -*- coding: utf-8 -*-
# from odoo import http


# class OmOdooInherit(http.Controller):
#     @http.route('/om_odoo_inherit/om_odoo_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_odoo_inherit/om_odoo_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_odoo_inherit.listing', {
#             'root': '/om_odoo_inherit/om_odoo_inherit',
#             'objects': http.request.env['om_odoo_inherit.om_odoo_inherit'].search([]),
#         })

#     @http.route('/om_odoo_inherit/om_odoo_inherit/objects/<model("om_odoo_inherit.om_odoo_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_odoo_inherit.object', {
#             'object': obj
#         })
