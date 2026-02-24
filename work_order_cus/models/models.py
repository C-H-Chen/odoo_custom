from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    date_late = fields.Datetime(
        string="最晚開工日"
    )

    def action_print_work_order_card(self):
        return self.env.ref(
            "work_order_cus.action_report_work_order_card"
        ).report_action(self)