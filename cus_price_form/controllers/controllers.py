# -*- coding: utf-8 -*-
# from odoo import http


# class CusPriceForm(http.Controller):
#     @http.route('/cus_price_form/cus_price_form', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cus_price_form/cus_price_form/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('cus_price_form.listing', {
#             'root': '/cus_price_form/cus_price_form',
#             'objects': http.request.env['cus_price_form.cus_price_form'].search([]),
#         })

#     @http.route('/cus_price_form/cus_price_form/objects/<model("cus_price_form.cus_price_form"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cus_price_form.object', {
#             'object': obj
#         })

