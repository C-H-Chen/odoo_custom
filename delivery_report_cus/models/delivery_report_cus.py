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
            if s is None:
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

        for doc in docs:
            partner = doc.partner_id or False
            company = doc.company_id or self.env.company

            lines_list = []
            subtotal_sum = 0.0
            tax_sum = 0.0

            for line in doc.move_ids_without_package:
                qty_val = getattr(line, 'quantity', None) or getattr(line, 'product_uom_qty', None) or getattr(line, 'product_qty', 1)
                uom_obj = getattr(line, 'product_uom', None) or getattr(line, 'product_uom_id', None)
                uom_name = uom_obj.name if uom_obj else 'PCS'

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
                    'product_code': entify_as_markup(getattr(line.product_id, 'default_code', '') or '預設編號'),
                    'product_name': entify_as_markup(getattr(line.product_id, 'name', '') or '預設品名'),
                    'qty': to_text(qty_val or 1),
                    'uom': entify_as_markup(uom_name),
                    'price_unit': to_text(price_unit or 0.0),
                    'subtotal': to_text(line_subtotal or 0.0),
                    'note': entify_as_markup(getattr(line, 'note', '') or ''),
                })

            total_sum = subtotal_sum + tax_sum

            docs_data.append({
                'company': {
                    'name': entify_as_markup(company.name or ''),
                    'street_city': entify_as_markup(((company.street or '') + ' ' + (company.city or '')).strip()),
                    'phone': entify_as_markup(getattr(company, 'phone', '') or ''),
                    'fax': entify_as_markup(getattr(company, 'fax', '') or ''),
                    'email': entify_as_markup(getattr(company, 'email', '') or ''),
                    'logo': company.logo or False,
                },
                'partner': {
                    'name': entify_as_markup(getattr(partner, 'name', '') or ''),
                    'ref': entify_as_markup(getattr(partner, 'ref', '') or ''),
                    'vat': entify_as_markup(getattr(partner, 'vat', '') or ''),
                    'contact': entify_as_markup(partner.child_ids[0].name if partner and partner.child_ids else '預設聯絡人'),
                    'phone': entify_as_markup(getattr(partner, 'phone', '') or '0000-000000'),
                    'fax': entify_as_markup(getattr(partner, 'fax', '') or ''),
                    'street_city': entify_as_markup(((getattr(partner, 'street', '') or '') + ' ' + (getattr(partner, 'city', '') or '')).strip()),
                },
                'date': entify_as_markup(doc.scheduled_date and fields.Datetime.to_string(doc.scheduled_date) or ''),
                'name': entify_as_markup(doc.name or 'DEL-0001'),
                'user_name': entify_as_markup(doc.create_uid.name if doc.create_uid else '系統'),
                'invoice_ref': entify_as_markup(doc.sale_id.invoice_ids[0].name if doc.sale_id and doc.sale_id.invoice_ids else ''),
                'note': entify_as_markup(doc.note or ''),
                'carrier_name': entify_as_markup(doc.carrier_id.name if doc.carrier_id else ''),
                'lines': lines_list,
                'amount_untaxed': to_text(subtotal_sum),
                'amount_tax': to_text(tax_sum),
                'amount_total': to_text(total_sum),
            })

        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs_data': docs_data,
        }
