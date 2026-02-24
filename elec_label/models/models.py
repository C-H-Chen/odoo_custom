from odoo import models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_report_elec_label_xlsx(self):
        return self.env.ref('elec_label.action_report_elec_label_xlsx').report_action(self)


class ElecLabelXlsx(models.AbstractModel):
    _name = 'report.elec_label.report_elec_label_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, orders):
        # 建立分頁
        sheet = workbook.add_worksheet('電鍍標籤')
        
        # 設定欄寬
        # 因為是 5 張卡片並排，需要設定 5 組欄位寬度
        #  [標籤欄(15)] [數值欄(30)] [空格(2)] ... 重複 5 次
        for i in range(5):
            base_col = i * 3
            # 標籤名稱欄 (A, D, G, J, M)
            sheet.set_column(base_col, base_col, 15)
            # 數值內容欄 (B, E, H, K, N)
            sheet.set_column(base_col + 1, base_col + 1, 30)
            # 中間空格欄 (C, F, I, L, O)
            sheet.set_column(base_col + 2, base_col + 2, 2)

        company_format = workbook.add_format({
            'font_size': 15,
            #'bold': True, 
            'align': 'center', 
            'valign': 'vcenter',
            'border': 1,
            #'bg_color': '#EFEFEF' 
        })
        
        label_format = workbook.add_format({
            'font_size': 15,
            #'bold': True,
            'align': 'right',   
            'valign': 'vcenter',
            'top': 1, 'bottom': 1, 'left': 1, 'right': 0
        })
        
        value_format = workbook.add_format({
            'font_size': 15,
            'align': 'left',
            'valign': 'vcenter',
            'top': 1, 'bottom': 1, 'left': 0, 'right': 1,
            'text_wrap': True  
        })
        
        date_format = workbook.add_format({
            'font_size': 15,
            'align': 'left',
            'valign': 'vcenter',
            'top': 1, 'bottom': 1, 'left': 0, 'right': 1, 
            'num_format': 'yyyy-mm-dd'
        })

        # item_index 計算目前是第幾張卡片
        item_index = 0

        for order in orders:
            approve_date = order.date_approve or ''
            
            for line in order.order_line:
                # 準備資料
                categ_name = line.product_id.categ_id.name if line.product_id.categ_id else ''
                product_name = line.product_id.display_name or ''
                # 重量
                qty_part = ""
                if line.product_qty:
                    qty_part = str(line.product_qty) + "　"
                
                # 單位
                uom_part = ""
                if line.product_uom:
                    uom_part = f"({line.product_uom.name})"
                
                # 組合字串
                qty_display_str = qty_part + uom_part
                # ==================================

                # ==========================================
                # 計算座標
                # ==========================================
                # 橫向第幾格 (0, 1, 2, 3, 4)
                col_block = item_index % 5 
                # 縱向第幾層 (0, 1, 2...)
                row_block = item_index // 5

                # 每一組佔用 3 欄 (Label + Value + Gap)
                start_col = col_block * 3 
                # 每一張佔用 6 列 (5內容 + 1Gap)
                start_row = row_block * 6

                # ==========================================
                # 繪製單張卡片
                # ==========================================

                # 1. 公司名稱
                # (Start Row, Start Col) 到 (Start Row, Start Col + 1)
                sheet.merge_range(start_row, start_col, start_row, start_col + 1, 
                                  "琦霖光輝科技有限公司", company_format)
                
                # 日期
                sheet.write(start_row + 1, start_col, "日期 :", label_format)
                sheet.write(start_row + 1, start_col + 1, approve_date, date_format)
                
                # 品名
                sheet.write(start_row + 2, start_col, "品名 :", label_format)
                sheet.write(start_row + 2, start_col + 1, categ_name, value_format)
                
                # 數量
                sheet.write(start_row + 3, start_col, "重量 :", label_format)
                sheet.write(start_row + 3, start_col + 1, qty_display_str, value_format)
                
                # 電鍍規格
                sheet.write(start_row + 4, start_col, "電鍍規格 :", label_format)
                sheet.write(start_row + 4, start_col + 1, product_name, value_format)

                # 處理完一張卡片，計數器 +1
                item_index += 1