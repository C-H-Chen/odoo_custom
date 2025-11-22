# -*- coding: utf-8 -*-
# from odoo import http


# class SaleorderlineAdd(http.Controller):
#     @http.route('/saleorderline_add/saleorderline_add', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/saleorderline_add/saleorderline_add/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('saleorderline_add.listing', {
#             'root': '/saleorderline_add/saleorderline_add',
#             'objects': http.request.env['saleorderline_add.saleorderline_add'].search([]),
#         })

#     @http.route('/saleorderline_add/saleorderline_add/objects/<model("saleorderline_add.saleorderline_add"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('saleorderline_add.object', {
#             'object': obj
#         })

