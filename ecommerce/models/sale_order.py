from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        order = super().create(vals)
        order._update_partner_products()
        return order

    def write(self, vals):
        res = super().write(vals)
        if 'state' in vals or 'order_line' in vals:
            self._update_partner_products()
        return res

    def _update_partner_products(self):
        for order in self.filtered(lambda o: o.partner_id):
            order.partner_id._update_customer_previous_products()