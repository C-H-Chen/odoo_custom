# -*- coding: utf-8 -*-
# from odoo import http


# class Btn(http.Controller):
#     @http.route('/btn_/btn_', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/btn_/btn_/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('btn_.listing', {
#             'root': '/btn_/btn_',
#             'objects': http.request.env['btn_.btn_'].search([]),
#         })

#     @http.route('/btn_/btn_/objects/<model("btn_.btn_"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('btn_.object', {
#             'object': obj
#         })

