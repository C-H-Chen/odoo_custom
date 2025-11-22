from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    ship_price = fields.Float(string='出貨價', compute='_compute_amount', store=True, precompute=True)

    last_customer_discount = fields.Float(string='最後一次折扣')

    '''
    出貨價 = 定價 - 折扣
    未連稅金額 = 數量 * 出貨價
    '''
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'company_id')
    def _compute_amount(self):

        for line in self:
            line.ship_price = line.price_unit - (line.discount or 0.0)

            # 取得原稅基 dict
            base_line = line._convert_to_tax_base_line_dict()
            # 覆寫
            base_line['price_unit'] = line.ship_price
            base_line['discount'] = 0.0

            # 原邏輯
            tax_results = self.env['account.tax'].with_company(line.company_id)._compute_taxes([base_line])

            totals = list(tax_results['totals'].values())[0]
            amount_untaxed = totals['amount_untaxed']
            amount_tax = totals['amount_tax']

            line.update({
                'price_subtotal': amount_untaxed,
                'price_tax': amount_tax,
                'price_total': amount_untaxed + amount_tax,
            })

    # 自動帶出該客戶對此產品的最後一次折扣
    @api.onchange('product_id', 'order_id.partner_id')
    def _onchange_product_set_last_discount(self):
        
        for line in self:
            partner = line.order_id.partner_id
            product = line.product_id

            # 查詢過往報價單中的最後一次折扣
            if partner and product:
                
                last_line = self.env['sale.order.line'].search([
                    ('order_id.partner_id', '=', partner.id),
                    ('product_id', '=', product.id),
                    ('order_id.state', 'in', ['sale', 'done', 'draft']),
                ], order='write_date desc', limit=1)

                if last_line:
                    line.last_customer_discount = last_line.discount
                    line.discount = last_line.discount  # 預填