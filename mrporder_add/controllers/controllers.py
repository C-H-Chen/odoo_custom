from odoo import http
from odoo.http import request

class MrpFrontendController(http.Controller):
    @http.route('/mrp_show_info', type='json', auth='user', methods=['POST'])
    def mrp_show_info(self, **kw):
        try:
            action = request.env['mrp.workorder'].sudo().action_show_info()
            return action
        except Exception as e:
            return {
                "type": "ir.actions.client",
                "tag": "display_notification",
                "params": {
                    "title": "伺服器錯誤",
                    "message": f"伺服器發生例外: {str(e)}",
                    "type": "danger",
                    "sticky": True,
                    "next": None
                },
            }
