# -*- coding: utf-8 -*-
# from odoo import http


# class PosInherit(http.Controller):
#     @http.route('/pos_inherit/pos_inherit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_inherit/pos_inherit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_inherit.listing', {
#             'root': '/pos_inherit/pos_inherit',
#             'objects': http.request.env['pos_inherit.pos_inherit'].search([]),
#         })

#     @http.route('/pos_inherit/pos_inherit/objects/<model("pos_inherit.pos_inherit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_inherit.object', {
#             'object': obj
#         })
