# -*- encoding: utf-8 -*-
##############################################################################
#
#    Nato Stock Number
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class purchase_order_line(models.Model):
    _inherit = 'purchase.order.line'

    nsn = fields.Char(string='NSN')
    part_number = fields.Char(string='Part number')

    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
                            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
                            name=False, price_unit=False, state='draft', context=None
                            ):

        vals = super(purchase_order_line, self).onchange_product_id(
            cr, uid, ids, pricelist_id, product_id, qty, uom_id, partner_id, date_order=date_order,
            fiscal_position_id=fiscal_position_id, date_planned=date_planned,name=name, price_unit=price_unit,
            state=state, context=context
        )

        if not product_id:
            return vals

        product_product = self.pool.get('product.product')
        res_partner = self.pool.get('res.partner')

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        if product:
            name = product.name
            if product.description_purchase:
                name += '\n' + product.description_purchase
            vals['value'].update({'name': name})
            vals['value']['nsn'] = product.default_code or False

        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                vals['value']['part_number'] = supplier.product_code or False

        return vals

class purchase_order(models.Model):
    _inherit = 'purchase.order'

    def _prepare_order_line_move(
            self, cr, uid, order, order_line, picking_id, group_id, context=None
    ):
        vals = super(purchase_order, self)._prepare_order_line_move(
            cr, uid, order, order_line, picking_id, group_id, context=context
        )

        for val in vals:
            val['nsn'] = order_line.nsn

        return vals



    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        vals = super(purchase_order, self)._prepare_inv_line(
            cr, uid, account_id, order_line, context=context
        )
        vals['nsn'] = order_line.nsn
        return vals