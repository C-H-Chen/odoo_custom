from odoo import models

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_print_custom_po(self):
        return self.env.ref(
            'po_report_cus.action_report_custom_po'
        ).report_action(self)
