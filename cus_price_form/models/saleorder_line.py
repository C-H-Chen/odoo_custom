from odoo import models, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends(
        'product_id', 'product_uom_qty', 'order_id.pricelist_id',
        'product_uom', 'order_id.fiscal_position_id', 'currency_id',
    )
    def _compute_price_unit(self):

        for line in self:

            # 若缺必要欄位直接設定為 0
            if not line.order_id or not line.product_id or not line.product_uom:
                line.price_unit = 0.0
                continue

            # 價格表
            pricelist = line.order_id.pricelist_id

            # 沒價格表，原邏輯
            if not pricelist:
                line.price_unit = line._get_display_price()
                continue

            # 若該行已開立發票或折扣，則不重算價格。
            if (
                line.qty_invoiced > 0
                or (line.product_id.expense_policy == 'cost' and getattr(line, 'is_expense', False))
                or line._is_discount_line()
            ):
                continue

            line = line.with_company(line.company_id)
            quantity = float(line.product_uom_qty or 0.0)

            # price: 用於暫存計算中的未稅價格（以價目表幣別計算）
            # 是否有套用包裝價邏輯
            price = None
            applied_packaging = False

            # 若價目表啟用「包裝單位定價」且產品有包裝設定，則優先以包裝數量為基準決定價格。
            if pricelist.packaging_unit_price and line.product_id.packaging_ids:
                # 取第一個包裝規則（依 sequence 排序）
                packaging = line.product_id.packaging_ids.sorted('sequence')[:1]
                if packaging:
                    pack_qty = float(packaging.qty or 0.0)

                    # 若訂單數量 >= 包裝數量，嘗試使用價目表的價格規則
                    if pack_qty and quantity >= pack_qty:
                        try:
                            # 原價格規則計算方法
                            price_pack, rule_id = pricelist._get_product_price_rule(
                                line.product_id, quantity, line.product_uom
                            )
                        except Exception:
                            price_pack = None

                        if price_pack is not None:
                            # 成功取得價格表價格
                            price = price_pack
                            applied_packaging = True
                        else:
                            # 若無價目表規則，則原邏輯售價
                            price = line.product_id.list_price
                            applied_packaging = True
                    else:
                        # 若數量未達包裝數量門檻，則使用產品的基本售價
                        price = line.product_id.list_price
                        applied_packaging = False

            # 若未套用包裝邏輯或無法計算價格，則原邏輯計價。
            if price is None:
                price = line._get_display_price()

            # 稅金與幣別換算 
            product_taxes = line.product_id.taxes_id._filter_taxes_by_company(line.company_id)
            final_price_unit = line.product_id._get_tax_included_unit_price_from_price(
                price,
                line.currency_id or line.order_id.currency_id,
                product_taxes=product_taxes,
                fiscal_position=line.order_id.fiscal_position_id,
            )

            # 最終單價
            line.price_unit = final_price_unit