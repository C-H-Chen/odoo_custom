from odoo import models, api, fields
from markupsafe import Markup

class DeliveryReportCus(models.AbstractModel):
    _name = 'report.delivery_report_cus.report_delivery_report_template'
    _description = 'Custom Delivery Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        docs_data = []

        def to_text(v):
            if v is None:
                return ''
            return '{:.2f}'.format(v) if isinstance(v, float) else str(v)

        def entify_as_markup(s):
            if s is False or s is None or s == '':
                return Markup('')
            s = str(s)
            out = []
            for ch in s:
                if ord(ch) > 127:
                    out.append('&#%d;' % ord(ch))
                else:
                    if ch == '&': out.append('&amp;')
                    elif ch == '<': out.append('&lt;')
                    elif ch == '>': out.append('&gt;')
                    else: out.append(ch)
            return Markup(''.join(out))
        
        def split_text_to_rows(text, max_chars=40):
            """每 max_chars 字元拆成一行，不考慮單詞完整性"""
            if not text:
                return ['']
            return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

        for doc in docs:
            partner = doc.partner_id or False
            company = doc.company_id or self.env.company

            lines_list = []
            subtotal_sum = 0.0
            tax_sum = 0.0

            for line in doc.move_ids_without_package:
                qty_val = getattr(line, 'quantity', None)
                    # 取得對應的銷售訂單行（用來抓 qty_delivered）
                sol = False
                if doc.sale_id:
                    sol = doc.sale_id.order_line.filtered(lambda l: l.product_id == line.product_id)

                #  qty_delivered -> 從 SOL 取
                # qty_val = sol[0].qty_delivered if sol else 0.0
                # qty_val = qty_val or 0.0
                
                uom_obj = getattr(line, 'product_uom', None) or getattr(line, 'product_uom_id', None)
                uom_name = uom_obj.name if uom_obj else ''

                price_unit = 0.0
                if doc.sale_id:
                    sol = doc.sale_id.order_line.filtered(lambda l: l.product_id == line.product_id)
                    if sol:
                        price_unit = sol[0].price_unit
                if price_unit == 0.0:
                    price_unit = line.product_id.lst_price or 0.0

                line_subtotal = round(price_unit * qty_val, 2)
                subtotal_sum += line_subtotal

                line_tax = 0.0
                if doc.sale_id and sol:
                    for tax in sol[0].tax_id:
                        line_tax += line_subtotal * tax.amount / 100.0
                tax_sum += line_tax

                lines_list.append({
                    'product_code':(
                        '[%s] %s' % (line.product_id.default_code or '', line.product_id.name or '')
                        if line.product_id.default_code else line.product_id.name
                    ),
                        # (sol[0].name if sol else '') 
                    # 'product_name': entify_as_markup(getattr(line.product_id, 'name', '') or ''),
                    'qty': to_text(round(qty_val or 0)),
                    'uom': entify_as_markup(uom_name),
                    'price_unit': to_text(price_unit or ''),
                    'subtotal': to_text(line_subtotal or ''),
                    'client_order_ref': entify_as_markup(doc.sale_id.client_order_ref if doc.sale_id else ''),
                })

            total_sum = subtotal_sum + tax_sum
            
            page_size = 10  # 每頁最大列數
            current_page_lines = 0
            seq = 1
            paginated_lines = []

            for line in lines_list:
                full_text = line['product_code'] or ''
                # 以每 max_chars 字元硬切（中文每字算一個字元）
                text_rows = split_text_to_rows(full_text, max_chars=40)
                needed_lines = len(text_rows)

                # 如果本頁剩餘行數不足容納本筆資料 -> 換頁（並用空列補滿）
                if current_page_lines + needed_lines > page_size:
                    remaining = page_size - current_page_lines
                    if remaining > 0:
                        for _ in range(remaining):
                            paginated_lines.append({
                                'product_code': entify_as_markup(''),
                                'qty': '',
                                'uom': '',
                                'price_unit': '',
                                'subtotal': '',
                                'client_order_ref': '',
                                'seq': ''
                            })
                    current_page_lines = 0  # 換頁

                # 加入資料行（分成多列）
                for i, row_text in enumerate(text_rows):
                    new_line = line.copy()
                    # 產品欄使用 entify_as_markup 以避免 template escape 問題
                    new_line['product_code'] = entify_as_markup(row_text)
                    if i > 0:
                        # 後續拆出列不顯示 qty/uom/price/subtotal，只保留文字
                        new_line['qty'] = ''
                        new_line['uom'] = ''
                        new_line['price_unit'] = ''
                        new_line['subtotal'] = ''
                        new_line['client_order_ref'] = ''
                        new_line['seq'] = ''
                    else:
                        new_line['seq'] = str(seq)
                        seq += 1
                    paginated_lines.append(new_line)

                current_page_lines += needed_lines

            # 把 paginated_lines 放進 docs_data
            docs_data.append({
                'company': {
                    'name': entify_as_markup(company.name or ''),
                    'street_city': entify_as_markup(((company.street or '') + ' ' + (company.city or '')).strip()),
                    'phone': entify_as_markup(getattr(company, 'phone', '') or ''),
                    'website': entify_as_markup(getattr(company, 'website', '') or ''),
                    'email': entify_as_markup(getattr(company, 'email', '') or ''),
                    'logo': company.logo or False,
                },
                'partner': {
                    'name': entify_as_markup(getattr(partner, 'name', '') or ''),
                    'ref': entify_as_markup(getattr(partner, 'ref', '') or ''),
                    'vat': entify_as_markup(getattr(partner, 'vat', '') or ''),
                    'contact': entify_as_markup(partner.child_ids[0].name if partner and partner.child_ids else ''),
                    'phone': entify_as_markup(getattr(partner, 'phone', '') or ''),
                    'website': entify_as_markup(getattr(partner, 'website', '') or ''),
                    'street_city': entify_as_markup(((getattr(partner, 'street', '') or '') + ' ' + (getattr(partner, 'city', '') or '')).strip()),
                },
                'date': entify_as_markup(
                    doc.date_done and fields.Date.to_string(
                        fields.Datetime.context_timestamp(self.env.user, doc.date_done)
                    ) or ''
                ),
                'name': entify_as_markup(doc.name or ''),
                'user_name': entify_as_markup(doc.create_uid.name if doc.create_uid else ''),
                'invoice_ref': entify_as_markup(doc.sale_id.invoice_ids[0].name if doc.sale_id and doc.sale_id.invoice_ids else ''),
                'client_order_ref': entify_as_markup(
                    (doc.sale_id and doc.sale_id.client_order_ref) or ''
                ),
                'carrier_name': entify_as_markup(getattr(doc, 'carrier_id', False) and getattr(doc.carrier_id, 'name', '') or ''),
                'lines': paginated_lines,   
                'amount_untaxed': to_text(subtotal_sum),
                'amount_tax': to_text(tax_sum),
                'amount_total': to_text(total_sum),
            })

        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs_data': docs_data,
        }

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_print_and_download_pdf(self):
        """按鈕 -> 直接下載 PDF"""
        self.ensure_one()
        return self.env.ref(
            'delivery_report_cus.action_report_custom_delivery_order'
        ).report_action(self)