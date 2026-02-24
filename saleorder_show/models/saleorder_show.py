from odoo import models, fields, api
from markupsafe import Markup  # 用來安全處理 HTML 特殊字元，避免亂碼或 XSS

class SaleOrder(models.Model):
    _inherit = "sale.order"

    # 控制"+"
    show_detail = fields.Boolean(string="顯示明細", default=False)

    # 訂單明細表格欄位，會自動生成 HTML table，前端顯示用
    line_table = fields.Html(string="訂單明細", compute="_compute_line_table", sanitize=True, store=True)

    # 計算 line_table 的內容，依據訂單明細生成表格
    @api.depends(
        'order_line', 'order_line.product_id', 'order_line.name',
        'order_line.product_uom_qty','order_line.product_packaging_qty','order_line.product_packaging_id', 
        'order_line.price_unit','order_line.price_subtotal', 'order_line.tax_id', 'show_detail'
    )


    # 生成 HTML 表格，顯示每筆訂單明細
    def _compute_line_table(self):
        for order in self:
            if not order.show_detail or not order.order_line:
                # 如果不顯示或沒有明細，表格為空
                order.line_table = ""
                continue

            rows = []

            # 表格標題列
            header = (
                "<thead><tr>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:left;'>商品</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:left;'>說明</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:right;'>數量</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:right;'>包裝數量</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:left;'>包裝</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:right;'>單價</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:right;'>未連稅</th>"
                "<th style='padding:2px 6px;border-bottom:1px solid #ddd;text-align:left;'>稅項</th>"
                "</tr></thead>"
            )

            # 每筆訂單明細生成一列
            for line in order.order_line:
                prod_name = line.product_id.display_name if line.product_id else ''
                desc = line.name or ''
                qty = getattr(line, 'product_uom_qty', '') or ''
                package_qty = getattr(line, 'product_packaging_qty', '') or ''
                package_name = line.product_packaging_id.name if line.product_packaging_id else ''
                price_unit = getattr(line, 'price_unit', '') or ''
                subtotal = getattr(line, 'price_subtotal', '') or ''

                # 處理稅項名稱
                tax_names = ''
                if line.tax_id:
                    tax_names = ', '.join(t.name for t in line.tax_id)

                # 生成 HTML table row
                row = (
                    "<tr>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;vertical-align:top;'>{Markup.escape(prod_name)}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;vertical-align:top;'>{Markup.escape(desc)}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;text-align:right;vertical-align:top;'>{qty}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;text-align:right;vertical-align:top;'>{package_qty}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;vertical-align:top;'>{Markup.escape(package_name)}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;text-align:right;vertical-align:top;'>{price_unit}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;text-align:right;vertical-align:top;'>{subtotal}</td>"
                    f"<td style='padding:2px 6px;border-top:1px solid #f4f4f4;vertical-align:top;'>{Markup.escape(tax_names)}</td>"
                    "</tr>"
                )
                rows.append(row)

            # 將 header 和 body 合併成完整 table
            table_html = (
                "<div style='max-width:800px;overflow:auto;' title=''>"
                "<table style='border-collapse:collapse;width:100%;font-size:12px;'>"
                + header +
                "<tbody>" + "".join(rows) + "</tbody>"
                "</table>"
                "</div>"
            )

            # 將生成好的 HTML 存入欄位
            order.line_table = Markup(table_html)
    
    
    # 切換 "+" 狀態
    def action_toggle_detail(self):
        
        for rec in self:
            rec.show_detail = not rec.show_detail
        return True