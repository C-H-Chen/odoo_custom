from odoo import models

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_print_material_label(self):
        self.ensure_one()
        return self.env.ref(
            "material_tag.action_report_material_label"
        ).report_action(self)
