from odoo import models, api
import requests
import json
import logging

_logger = logging.getLogger(__name__)

class DeliveryReportMail(models.Model):
    _inherit = 'stock.picking'

    def action_print_and_send_mail(self):
        line_token = self.env['ir.config_parameter'].sudo().get_param('line_test.token').strip()
        line_group = "your_line_group_id"

        for picking in self:
            # 發 Email
            try:
                mail_values = {
                    'subject': f"[通知] test",
                    'body_html': f"test",
                    'email_to': "your_mail@gmail.com",
                    'email_from': self.env.user.email_formatted,
                }
                self.env['mail.mail'].sudo().create(mail_values).send()
            except Exception as e:
                _logger.error("Email 發送失敗: %s", e)

            # 發 LINE
            try:
                message_text = f"test"
                payload = {
                    "to": line_group,
                    "messages":[{"type":"text", "text": message_text}]
                }
                r = requests.post("https://api.line.me/v2/bot/message/push",
                                headers={
                                    "Content-Type": "application/json",
                                    "Authorization": f"Bearer {line_token}"
                                },
                                data=json.dumps(payload))
                r.raise_for_status()
                _logger.info("LINE發送成功: %s", r.text)
            except requests.exceptions.RequestException as e:
                _logger.error("LINE發送失敗: %s", e)

        # 回傳 PDF
        return self.env.ref(
            "delivery_report_cus.action_report_custom_delivery_order"

        ).report_action(self)
