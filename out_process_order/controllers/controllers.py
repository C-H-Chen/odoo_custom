# -*- coding: utf-8 -*-
# from odoo import http


# class OutProcessOrder(http.Controller):
#     @http.route('/out_process_order/out_process_order', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/out_process_order/out_process_order/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('out_process_order.listing', {
#             'root': '/out_process_order/out_process_order',
#             'objects': http.request.env['out_process_order.out_process_order'].search([]),
#         })

#     @http.route('/out_process_order/out_process_order/objects/<model("out_process_order.out_process_order"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('out_process_order.object', {
#             'object': obj
#         })

