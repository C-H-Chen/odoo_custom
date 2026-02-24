# -*- coding: utf-8 -*-
# from odoo import http


# class DeliveryReportCus(http.Controller):
#     @http.route('/delivery_report_cus/delivery_report_cus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_report_cus/delivery_report_cus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_report_cus.listing', {
#             'root': '/delivery_report_cus/delivery_report_cus',
#             'objects': http.request.env['delivery_report_cus.delivery_report_cus'].search([]),
#         })

#     @http.route('/delivery_report_cus/delivery_report_cus/objects/<model("delivery_report_cus.delivery_report_cus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_report_cus.object', {
#             'object': obj
#         })

