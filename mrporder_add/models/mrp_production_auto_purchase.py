from odoo import models, fields, api
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_confirm(self):
        # 執行製造訂單原確認邏輯
        res = super(MrpProduction, self).action_confirm()
        self._check_materials_and_create_purchase()
        return res

    def _check_materials_and_create_purchase(self):
        PurchaseOrder = self.env['purchase.order']
        ProductSupplierInfo = self.env['product.supplierinfo']

        for mo in self:
            supplier_lines_map = {} # 暫存供應商採購
            # 每個原料未完成需求
            for line in mo.move_raw_ids.filtered(lambda m: m.state != 'done'):
                product = line.product_id
                # 實際已分配數量
                done_qty = sum(line.move_line_ids.mapped('quantity')) or 0.0
                required_qty = (line.product_uom_qty or 0.0) - done_qty

                if required_qty > 0:
                    supplier_info = ProductSupplierInfo.search([
                        ('product_tmpl_id', '=', product.product_tmpl_id.id)
                    ], limit=1)
                    
                    # 確認供應商
                    if not supplier_info:
                        raise UserError(f"產品 {product.display_name} 沒有設定供應商，無法自動建立採購單。")

                    supplier = supplier_info.partner_id
                    if supplier not in supplier_lines_map:
                        supplier_lines_map[supplier] = []

                    supplier_lines_map[supplier].append({
                        'product_id': product.id,
                        'name': product.name,
                        'product_qty': required_qty,
                        'product_uom': product.uom_id.id,
                        'price_unit': supplier_info.price or 0.0,
                        'date_planned': mo.date_start,
                    })

            # 依供應商建立採購單並確認
            for supplier, lines in supplier_lines_map.items():
                po = PurchaseOrder.create({
                    'partner_id': supplier.id,
                    'order_line': [(0, 0, l) for l in lines],
                    'origin': mo.name,
                })
                po.button_confirm()  # 直接變成正式採購單


    # 採購單列表跳轉button

    def action_open_purchase_orders(self, record_ids=None):

        action = {
            'type': 'ir.actions.act_window',
            'name': '採購單列表',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('state', '=', 'purchase')],  # 只顯示已確認的採購單
        }