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

class sale_order_line(models.Model):
    _inherit = 'sale.order.line'

    nsn = fields.Char(string='NSN')

    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        vals = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id=account_id, context=context)
        vals['nsn'] = line.nsn
        return vals

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0.0,
                              uom=False, qty_uos=0.0, uos=False, name='', partner_id=False,
                              lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):


        vals = super(sale_order_line, self).product_id_change(
            cr, uid, ids, pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos, name=name,
            partner_id=partner_id, lang=lang, update_tax=update_tax, date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag, context=context
        )

        if partner_id and product and not flag:
            lang = self.pool.get('res.partner').browse(cr, uid, partner_id).lang

            if context:
                context_partner = context.copy()
            else:
                context_partner = {}

            context_partner.update({'lang': lang, 'partner_id': partner_id})

            product_obj = self.pool.get('product.product').browse(cr, uid, [product], context=context_partner)[0]
            vals['value']['name'] = product_obj.name
            vals['value']['nsn'] = product_obj.default_code

        return vals

class sale_order(models.Model):
    _inherit = 'sale.order'

    def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
        vals = super(sale_order, self)._prepare_order_line_procurement(cr, uid, order, line, group_id=group_id, context=context)
        vals['nsn'] = line.nsn
        return vals
