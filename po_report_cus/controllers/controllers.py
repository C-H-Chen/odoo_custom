# -*- coding: utf-8 -*-
# from odoo import http


# class PoReportCus(http.Controller):
#     @http.route('/po_report_cus/po_report_cus', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/po_report_cus/po_report_cus/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('po_report_cus.listing', {
#             'root': '/po_report_cus/po_report_cus',
#             'objects': http.request.env['po_report_cus.po_report_cus'].search([]),
#         })

#     @http.route('/po_report_cus/po_report_cus/objects/<model("po_report_cus.po_report_cus"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('po_report_cus.object', {
#             'object': obj
#         })

