from odoo import models, fields
from odoo.tools.float_utils import float_is_zero

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    show_remaining_qty = fields.Boolean(
        string='顯示未出貨數量',
        help='若上次不建立欠單則啟用，顯示未出貨數量。'
    )

    def _action_done(self):
        self._check_company()

        todo_moves = self.move_ids.filtered(
            lambda m: m.state in ['draft', 'waiting', 'partially_available', 'assigned', 'confirmed']
        )

        for picking in self:
            if picking.owner_id:
                picking.move_ids.write({'restrict_partner_id': picking.owner_id.id})
                picking.move_line_ids.write({'owner_id': picking.owner_id.id})

        todo_moves._action_done(cancel_backorder=self.env.context.get('cancel_backorder'))

        # 不建立欠單：計算未出貨數量
        if self.env.context.get('cancel_backorder', False):
            for move in todo_moves:
                done_qty = sum(ml.quantity for ml in move.move_line_ids)
                move.remaining_qty_to_ship = max(0.0, (move.product_uom_qty or 0.0) - done_qty)
            self.show_remaining_qty = True
        else:
            self.show_remaining_qty = False
            self.move_ids.write({'remaining_qty_to_ship': 0.0})

        self.write({'date_done': fields.Datetime.now(), 'priority': '0'})

        done_incoming_moves = self.filtered(
            lambda p: p.picking_type_id.code in ('incoming', 'internal')
        ).move_ids.filtered(lambda m: m.state == 'done')
        done_incoming_moves._trigger_assign()
        self._send_confirmation_email()
        return True


class StockMove(models.Model):
    _inherit = 'stock.move'

    remaining_qty_to_ship = fields.Float(
        string='未出貨數量',
        digits='Product Unit of Measure'
    )

    show_remaining_qty = fields.Boolean(
        string='顯示未出貨數量',
        related='picking_id.show_remaining_qty',
        store=False,
    )