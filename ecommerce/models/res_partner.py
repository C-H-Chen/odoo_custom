from odoo import models, fields, api

class CustomerPreviousProduct(models.Model):
    _name = 'customer.previous.product'
    _description = '客戶曾訂購過的商品'
    _rec_name = 'product_id'

    partner_id = fields.Many2one('res.partner', string='客戶', ondelete='cascade')
    product_id = fields.Many2one('product.product', string='商品', required=True)
    description = fields.Char(string='說明')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_previous_products = fields.One2many(
        'customer.previous.product',
        'partner_id',
        string='曾訂購過的商品'
    )

    def _update_customer_previous_products(self):
        ProductModel = self.env['customer.previous.product']
        for partner in self:
            # 刪掉舊紀錄
            ProductModel.search([('partner_id', '=', partner.id)]).unlink()
            # 查出所有已訂購商品
            order_lines = self.env['sale.order.line'].search([
                ('order_id.partner_id', '=', partner.id)
            ])
            # 以商品分組
            product_map = {}
            for line in order_lines:
                if line.product_id.id not in product_map:
                    product_map[line.product_id.id] = {
                        'partner_id': partner.id,
                        'product_id': line.product_id.id,
                        'description': line.name or '',
                    }
            # 建立新紀錄
            for val in product_map.values():
                ProductModel.create(val)