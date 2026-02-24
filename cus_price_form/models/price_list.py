from odoo import models, fields, api

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    packaging_unit_price = fields.Boolean(string="包裝單位計價")


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    packaging_unit = fields.Char(
        string="包裝單位",
        compute='_compute_packaging_unit',
        store=True,
    )

    actual_min_quantity = fields.Float(
        string="實際最小數量",
        compute='_compute_actual_min_quantity',
        store=True,
    )


    # 計算並填入 包裝單位（packaging_unit）
    @api.depends('product_id', 'product_tmpl_id')

    def _compute_packaging_unit(self):
        for rec in self:
            product = rec.product_id or (rec.product_tmpl_id.product_variant_ids[:1] if rec.product_tmpl_id else None)
            if product and product.packaging_ids:
                pack = product.packaging_ids.sorted('sequence')[:1]
                rec.packaging_unit = pack.name if pack else ''
            else:
                rec.packaging_unit = ''

    # 如果有勾選包裝單位計價，就用第一個"包裝"的包含數量
    # 否則用原本設定的最小數量
    @api.depends('min_quantity', 'packaging_unit', 'product_id.packaging_ids', 'pricelist_id.packaging_unit_price')
    def _compute_actual_min_quantity(self):
        for rec in self:
            use_packaging = bool(rec.pricelist_id and rec.pricelist_id.packaging_unit_price)
            if use_packaging and rec.product_id and rec.product_id.packaging_ids:
                pack = rec.product_id.packaging_ids.sorted('sequence')[:1]
                rec.actual_min_quantity = pack.qty if pack else rec.min_quantity
            else:
                rec.actual_min_quantity = rec.min_quantity
