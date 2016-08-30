# -*- encoding: utf-8 -*-
##############################################################################
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

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change(self, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False):
        res = super(SaleOrderLine, self).product_id_change(
                pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
                name=name, partner_id=partner_id, lang=lang,
                update_tax=update_tax, date_order=date_order, packaging=packaging,
                fiscal_position=fiscal_position, flag=flag
        )

        lang = lang or self._context.get('lang', False)

        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        partner = partner_obj.browse(self._cr, self._uid, partner_id)
        lang = partner.lang
        context_partner = self._context.copy()
        context_partner.update({'lang': lang, 'partner_id': partner_id})

        product_obj = product_obj.browse(self._cr, self._uid, product, context=context_partner)

        if not flag:
            res['value']['name'] = product_obj.name

        return res