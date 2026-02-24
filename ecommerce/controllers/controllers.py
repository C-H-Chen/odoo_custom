# -*- coding: utf-8 -*-
# from odoo import http


# class Ecommerce(http.Controller):
#     @http.route('/ecommerce/ecommerce', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ecommerce/ecommerce/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ecommerce.listing', {
#             'root': '/ecommerce/ecommerce',
#             'objects': http.request.env['ecommerce.ecommerce'].search([]),
#         })

#     @http.route('/ecommerce/ecommerce/objects/<model("ecommerce.ecommerce"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ecommerce.object', {
#             'object': obj
#         })

