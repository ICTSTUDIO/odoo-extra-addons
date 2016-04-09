# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


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