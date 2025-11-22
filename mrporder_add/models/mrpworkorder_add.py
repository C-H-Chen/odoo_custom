from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = "stock.move"


    remaining_qty = fields.Float(string="未投料", compute="_compute_remaining_qty")

    @api.depends('product_uom_qty', 'quantity')
    def _compute_remaining_qty(self):
        for move in self:
            move.remaining_qty = (move.product_uom_qty or 0) - (move.quantity or 0)