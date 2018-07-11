# -*- coding: utf-8 -*-
# Copyright© 2017-today ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

from odoo import models, fields, api


class ProductProductLabel(models.TransientModel):
    _inherit = "product.product.label"

    @api.multi
    def lines_get(self):
        context = self._context or {}
        if context.get('active_model') == 'stock.picking':
            pickings = self.env['stock.picking'].browse(context.get('active_ids', []))
            label_list = []
            for pick in pickings:
                for line in pick.move_lines:
                    if pick.picking_type_code == 'outgoing':
                        if line.product_id.label_outgoing:
                            label_list.append([0,0,{
                                'product_id': line.product_id.id,
                                'quantity': line.product_qty
                            }])
                    elif pick.picking_type_code == 'incoming':
                        if line.product_id.label_incoming:
                            label_list.append([0,0,{
                                'product_id': line.product_id.id,
                                'quantity': line.product_qty
                            }])
        else:
            label_list = super(ProductProductLabel, self).lines_get()
        return label_list