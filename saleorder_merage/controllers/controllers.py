# -*- coding: utf-8 -*-
# from odoo import http


# class SaleorderMerage(http.Controller):
#     @http.route('/saleorder_merage/saleorder_merage', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/saleorder_merage/saleorder_merage/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('saleorder_merage.listing', {
#             'root': '/saleorder_merage/saleorder_merage',
#             'objects': http.request.env['saleorder_merage.saleorder_merage'].search([]),
#         })

#     @http.route('/saleorder_merage/saleorder_merage/objects/<model("saleorder_merage.saleorder_merage"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('saleorder_merage.object', {
#             'object': obj
#         })

