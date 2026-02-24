import io
import base64
import zipfile
import xlsxwriter 
from odoo import models, fields, _

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_print_outsource_report(self):
        return self.env.ref('out_process_order.action_report_outsource').report_action(self)

    def action_report_elec_label_xlsx(self):
        return self.env.ref('elec_label.action_report_elec_label_xlsx').report_action(self)

    # ==========================================
    # 一鍵下載 (PDF + Excel -> ZIP)
    # ==========================================
    def action_download_outsource_pack(self):
        self.ensure_one()
        
        # 產生 PDF 資料 (Binary)
        report_action_id = 'out_process_order.action_report_outsource'
        pdf_content, _ = self.env['ir.actions.report']._render_qweb_pdf(report_action_id, self.ids)

        # 產生 Excel 資料 (Binary)
        # 使用 io.BytesIO 在記憶體中建立 Excel
        excel_buffer = io.BytesIO()

        # 引入 xlsxwriter
        workbook = xlsxwriter.Workbook(excel_buffer)
        
        # 呼叫共用的繪製邏輯 (傳入 workbook 和 當前訂單)
        self._generate_elec_label_content(workbook, self)
        
        workbook.close()
        excel_data = excel_buffer.getvalue()
        excel_buffer.close()

        # 建立 ZIP 檔案
        zip_buffer = io.BytesIO()
        zip_filename = f"{self.name}_外包加工資料包.zip"
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 加入 PDF
            zf.writestr(f"{self.name}_外包加工單.pdf", pdf_content)
            # 加入 Excel
            zf.writestr(f"{self.name}_電鍍標籤.xlsx", excel_data)

        # 建立附件並下載
        zip_content = base64.b64encode(zip_buffer.getvalue())
        zip_buffer.close()

        attachment = self.env['ir.attachment'].create({
            'name': zip_filename,
            'type': 'binary',
            'datas': zip_content,
            'res_model': 'purchase.order',
            'res_id': self.id,
            'mimetype': 'application/zip',
        })

        # 回傳下載動作
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }

    # ==========================================
    # 繪製 Excel 內容
    # (被 Report 模組 和 ZIP 方法同時呼叫)
    # ==========================================
    def _generate_elec_label_content(self, workbook, orders):
        # 建立分頁
        sheet = workbook.add_worksheet('電鍍標籤')
        
        # 設定欄寬 (5 張卡片並排)
        for i in range(5):
            base_col = i * 3
            # 標籤名稱欄 (A, D, G, J, M)
            sheet.set_column(base_col, base_col, 15)
            # 數值內容欄 (B, E, H, K, N)
            sheet.set_column(base_col + 1, base_col + 1, 30)
            # 中間空格欄 (C, F, I, L, O)
            sheet.set_column(base_col + 2, base_col + 2, 2)

        # 樣式定義
        company_format = workbook.add_format({
            'font_size': 15,
            'align': 'center', 'valign': 'vcenter', 'border': 1
        })
        label_format = workbook.add_format({
            'font_size': 15,
            'align': 'right', 'valign': 'vcenter',
            'top': 1, 'bottom': 1, 'left': 1, 'right': 0
        })
        value_format = workbook.add_format({
            'font_size': 15,
            'align': 'left', 'valign': 'vcenter', 
            'text_wrap': True,
            'top': 1, 'bottom': 1, 'left': 0, 'right': 1
        })
        date_format = workbook.add_format({
            'font_size': 15,
            'align': 'left', 'valign': 'vcenter',
            'num_format': 'yyyy-mm-dd',
            'top': 1, 'bottom': 1, 'left': 0, 'right': 1
        })

        item_index = 0

        for order in orders:
            approve_date = order.date_approve or ''
            
            # 過濾掉 display_type 為 'line_note' 或 'line_section' 的行，只保留產品行
            for line in order.order_line.filtered(lambda l: not l.display_type):
                # 準備資料
                categ_name = line.product_id.categ_id.name if line.product_id.categ_id else ''
                product_name = line.product_id.display_name or ''
                
                # 重量 / 單位字串組合
                qty_part = str(line.product_qty) + "　" if line.product_qty else ""
                uom_part = f"({line.product_uom.name})" if line.product_uom else ""
                qty_display_str = qty_part + uom_part

                # 計算座標 (5張一列)
                col_block = item_index % 5 
                row_block = item_index // 5
                start_col = col_block * 3 
                start_row = row_block * 6 

                # 繪製單張卡片
                # 1. 公司名稱
                sheet.merge_range(start_row, start_col, start_row, start_col + 1, 
                                  "xxxxxx有限公司", company_format)
                
                # 2. 日期
                sheet.write(start_row + 1, start_col, "日期 :", label_format)
                sheet.write(start_row + 1, start_col + 1, approve_date, date_format)
                
                # 3. 品名
                sheet.write(start_row + 2, start_col, "品名 :", label_format)
                sheet.write(start_row + 2, start_col + 1, categ_name, value_format)
                
                # 4. 重量
                sheet.write(start_row + 3, start_col, "重量 :", label_format)
                sheet.write(start_row + 3, start_col + 1, qty_display_str, value_format)
                
                # 5. 電鍍規格
                sheet.write(start_row + 4, start_col, "電鍍規格 :", label_format)
                sheet.write(start_row + 4, start_col + 1, product_name, value_format)

                item_index += 1


# ==========================================
# Excel 報表模型 (修改後)
# ==========================================
class ElecLabelXlsx(models.AbstractModel):
    _name = 'report.elec_label.report_elec_label_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, orders):
        # 直接呼叫 PurchaseOrder 裡的共用邏輯，避免代碼重複
        # 使用 orders[0] 來獲取模型方法 (如果 orders 不為空)
        if orders:
            orders[0]._generate_elec_label_content(workbook, orders)
