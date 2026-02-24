from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleMultiPickingWizard(models.TransientModel):
    _name = 'sale.multi.picking.wizard'
    _description = '從多張銷售單選商品建立合併出貨單'

    sale_order_ids = fields.Many2many('sale.order', string='銷售訂單', required=True)
    partner_id = fields.Many2one('res.partner', string='客戶', readonly=True)
    picking_type_id = fields.Many2one('stock.picking.type', string='出貨類型', required=True)
    select_all = fields.Boolean(string='全選商品') 
    line_ids = fields.One2many('sale.multi.picking.wizard.line', 'wizard_id', string='可選商品行')

    # 從 active_ids 自動帶出銷售訂單與商品行
    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get('active_ids') or []
        if not active_ids:
            return res

        orders = self.env['sale.order'].browse(active_ids)
        res['sale_order_ids'] = [(6, 0, orders.ids)]

        first_order = orders[0] if orders else None
        if first_order and first_order.warehouse_id:
            res['picking_type_id'] = (
                first_order.warehouse_id.out_type_id.id
                or first_order.warehouse_id.wh_out_type_id.id
            )

        partners = orders.mapped('partner_id')
        if len(partners) == 1:
            res['partner_id'] = partners[0].id

        lines = []
        for order in orders:
            for so_line in order.order_line:
                if so_line.product_id.type not in ('product', 'consu'):
                    continue
                remaining = so_line.product_uom_qty - so_line.qty_delivered
                if remaining <= 0:
                    continue
                lines.append((0, 0, {
                    'sale_order_id': order.id,
                    'sale_line_id': so_line.id,
                    'product_id': so_line.product_id.id,
                    'uom_id': so_line.product_uom.id,
                    'qty_available': so_line.product_id.qty_available,
                    'qty_to_ship': remaining,
                    'selected': False,
                }))
        if lines:
            res['line_ids'] = lines
        return res

    def action_create_combined_picking(self):
        self.ensure_one()
        lines = self.line_ids.filtered('selected')
        if not lines:
            raise UserError(_('請至少選擇一個商品行以建立出貨。'))

        partners = self.sale_order_ids.mapped('partner_id')
        if len(partners) > 1:
            raise UserError(_('請選擇相同客戶的銷售訂單以合併出貨。'))

        partner = self.partner_id
        if not partner:
            raise UserError(_('找不到客戶'))

        picking_type = self.picking_type_id
        if not picking_type:
            raise UserError(_('請選擇出貨類型 (picking type)。'))

        src_location = picking_type.default_location_src_id.id if picking_type.default_location_src_id else picking_type.warehouse_id.lot_stock_id.id
        dest_location = picking_type.default_location_dest_id.id if picking_type.default_location_dest_id else self.env.ref('stock.stock_location_customers').id

        origin_names = sorted(set(lines.mapped(lambda l: l.sale_order_id.name)))

        picking_vals = {
            'partner_id': partner.id,
            'picking_type_id': picking_type.id,
            'location_id': src_location,
            'location_dest_id': dest_location,
            'origin': ','.join(origin_names),
        }
        picking = self.env['stock.picking'].create(picking_vals)

        for wl in lines:
            qty = float(wl.qty_to_ship or 0.0)
            if qty <= 0:
                continue
            move_vals = {
                'name': wl.product_id.display_name,
                'product_id': wl.product_id.id,
                'product_uom_qty': qty,
                'product_uom': wl.uom_id.id,
                'picking_id': picking.id,
                'location_id': src_location,
                'location_dest_id': dest_location,
                'sale_line_id': wl.sale_line_id.id,
                'origin': picking.origin,
            }
            self.env['stock.move'].create(move_vals)

        picking.action_confirm()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'view_mode': 'form',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'target': 'current',
        }
    # 自動勾選或取消所有商品
    @api.onchange('select_all')
    def _onchange_select_all(self):
        for line in self.line_ids:
            line.selected = self.select_all

class SaleMultiPickingWizardLine(models.TransientModel):
    _name = 'sale.multi.picking.wizard.line'
    _description = 'Wizard - 資料行'

    wizard_id = fields.Many2one('sale.multi.picking.wizard', required=True, ondelete='cascade')
    sale_order_id = fields.Many2one('sale.order', string='銷售訂單')
    sale_line_id = fields.Many2one('sale.order.line', string='訂單行')
    product_id = fields.Many2one('product.product', string='商品')
    uom_id = fields.Many2one('uom.uom', string='單位')
    qty_available = fields.Float(string='庫存', digits='Product Unit of Measure')
    qty_to_ship = fields.Float(string='需求數量', digits='Product Unit of Measure')
    selected = fields.Boolean(string='選擇出貨商品', default=False)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    # 由 server action 開 wizard
    def action_open_multi_picking_wizard(self):
            orders = self
            if not orders:
                raise UserError('請先選擇至少一張銷售訂單')

            partners = orders.mapped('partner_id')
            if len(partners) > 1:
                raise UserError('請選擇相同客戶的銷售訂單以合併出貨')

            partner_id = partners and partners[0].id or False

            first_order = orders[0]
            picking_type_id = False
            if first_order and first_order.warehouse_id:
                picking_type_id = (
                    first_order.warehouse_id.out_type_id.id
                    or first_order.warehouse_id.wh_out_type_id.id
                )
            if not picking_type_id:
                pt = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
                picking_type_id = pt and pt.id or False

            # 建 wizard
            lines = []
            for order in orders:
                for so_line in order.order_line:
                    if so_line.product_id.type not in ('product', 'consu'):
                        continue
                    remaining = float(so_line.product_uom_qty or 0.0) - float(so_line.qty_delivered or 0.0)
                    if remaining <= 0:
                        continue
                    lines.append((0, 0, {
                        'sale_order_id': order.id,
                        'sale_line_id': so_line.id,
                        'product_id': so_line.product_id.id,
                        'uom_id': so_line.product_uom.id,
                        'qty_available': so_line.product_id.qty_available,
                        'qty_to_ship': remaining,
                        'selected': False,
                    }))

            vals = {
                'sale_order_ids': [(6, 0, orders.ids)],
                'partner_id': partner_id,
                'picking_type_id': picking_type_id,
                'line_ids': lines,
            }
            wizard = self.env['sale.multi.picking.wizard'].create(vals)

            action = self.env.ref('saleorder_merage.action_sale_multi_picking_wizard').read()[0]
            action['res_id'] = wizard.id
            action['context'] = dict(self.env.context, active_id=wizard.id)
            return action

    # 取消自動生成交貨單
    @api.model
    def _action_confirm(self):

        # 原生建單
        res = super(SaleOrder, self)._action_confirm()

        # 找出與這些訂單有 origin 關聯的 pickings（尚未完成或取消的）
        order_names = self.mapped('name')
        if order_names:
            try:
                pickings = self.env['stock.picking'].search([('origin', 'in', order_names)])
                # 過濾還沒完成/還存在的 pickings
                pickings = pickings.filtered(lambda p: p.state not in ('done', 'cancel'))
                if pickings:
                    _logger.info("sale.manual_picking: cancelling and unlinking %s pickings for orders %s", len(pickings), order_names)
                    # 取消
                    for p in pickings:
                        try:
                            p.action_cancel()
                        except Exception as e:
                            _logger.warning("Could not action_cancel picking %s: %s", p.id, e)
                    # unlink
                    try:
                        pickings.unlink()
                    except Exception as e:
                        _logger.warning("Could not unlink pickings %s: %s", pickings.ids, e)
            except Exception as e:
                _logger.exception("Error while removing auto-created pickings after sale confirm: %s", e)

        return res