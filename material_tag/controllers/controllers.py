# -*- coding: utf-8 -*-
# from odoo import http


# class MaterialTag(http.Controller):
#     @http.route('/material_tag/material_tag', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/material_tag/material_tag/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('material_tag.listing', {
#             'root': '/material_tag/material_tag',
#             'objects': http.request.env['material_tag.material_tag'].search([]),
#         })

#     @http.route('/material_tag/material_tag/objects/<model("material_tag.material_tag"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('material_tag.object', {
#             'object': obj
#         })

