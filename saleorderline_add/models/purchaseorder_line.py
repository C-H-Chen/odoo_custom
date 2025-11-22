from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    vendor_part_no = fields.Char(string='廠商料號')

    # 自動帶出該供應商對此產品的最後一次廠商料號
    @api.onchange('product_id', 'order_id.partner_id')
    def _onchange_product_set_last_vendor_part_no(self):
        
        for line in self:
            partner = line.order_id.partner_id
            product = line.product_id

            # 查詢過往詢價單中的最後一次料號
            if partner and product:
                
                last_line = self.env['purchase.order.line'].search([
                    ('order_id.partner_id', '=', partner.id),
                    ('product_id', '=', product.id),
                    ('order_id.state', 'in', ['draft', 'sent', 'purchase']),  # 詢價或採購狀態
                ], order='write_date desc', limit=1)

                if last_line and last_line.vendor_part_no:
                    line.vendor_part_no = last_line.vendor_part_no # 預填