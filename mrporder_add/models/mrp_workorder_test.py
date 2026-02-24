from odoo import models, api

class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.model
    def action_show_info(self):
        return {
            "type": "ir.actions.client",
            "tag": "display_notification", 
            "params": {
                "title": "訊息",
                "message": "這是一個測試訊息！",
                "type": "info", 
                "sticky": False,  
                "next": None
            },
        }