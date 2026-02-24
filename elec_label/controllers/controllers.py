# -*- coding: utf-8 -*-
# from odoo import http


# class ElecLabel(http.Controller):
#     @http.route('/elec_label/elec_label', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/elec_label/elec_label/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('elec_label.listing', {
#             'root': '/elec_label/elec_label',
#             'objects': http.request.env['elec_label.elec_label'].search([]),
#         })

#     @http.route('/elec_label/elec_label/objects/<model("elec_label.elec_label"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('elec_label.object', {
#             'object': obj
#         })

