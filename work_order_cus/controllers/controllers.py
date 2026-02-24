# -*- coding: utf-8 -*-
# from odoo import http


# class WorkOrderCus(http.Controller):
#     @http.route('/work_order_cus/work_order_cus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/work_order_cus/work_order_cus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('work_order_cus.listing', {
#             'root': '/work_order_cus/work_order_cus',
#             'objects': http.request.env['work_order_cus.work_order_cus'].search([]),
#         })

#     @http.route('/work_order_cus/work_order_cus/objects/<model("work_order_cus.work_order_cus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('work_order_cus.object', {
#             'object': obj
#         })

