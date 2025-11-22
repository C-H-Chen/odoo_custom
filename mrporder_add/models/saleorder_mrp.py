from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    auto_mo_ids = fields.Many2many('mrp.production', string="Auto Generated MO")

    def action_confirm(self):
        res = super().action_confirm()

        for order in self:
            for line in order.order_line:
                product = line.product_id
                qty_needed = float(line.product_uom_qty)

                # 找對應物料清單(product_id 或 product_tmpl_id)
                bom = self.env['mrp.bom'].search([
                    '|',
                    ('product_tmpl_id', '=', product.product_tmpl_id.id),
                    ('product_id', '=', product.id),
                    ('type', '=', 'normal')
                ], limit=1)
                if not bom:
                    print(f"No BOM found for {product.name}")
                    continue

                # 檢查物料清單的每個料件庫存是否充足
                can_produce = True
                for bom_line in bom.bom_line_ids:
                    component = bom_line.product_id
                    required_qty = bom_line.product_qty * qty_needed / bom.product_qty
                    if component.qty_available < required_qty:
                        can_produce = False
                        break

                if not can_produce:
                    continue

                # 建立製造訂單
                vals = {
                    'product_id': product.id,
                    'product_qty': qty_needed,
                    'product_uom_id': product.uom_id.id,
                    'origin': order.name,
                    'bom_id': bom.id,
                    'company_id': order.company_id.id,
                }

                production = self.env['mrp.production'].sudo().create(vals)
                production.action_confirm()
                production.action_assign()

                order.auto_mo_ids = [(4, production.id)]

        return res
    
    # 查看製造訂單button
    def action_view_auto_mo(self):
        if not self.auto_mo_ids:
            return

        return {
            'name': "製造訂單",
            'type': 'ir.actions.act_window',
            'res_model': 'mrp.production',
            'view_mode': 'form,tree',
            'res_id': self.auto_mo_ids.id if len(self.auto_mo_ids) == 1 else False,
            'domain': [('id', 'in', self.auto_mo_ids.ids)] if len(self.auto_mo_ids) > 1 else [],
            'target': 'current',
        }