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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def get_purchase_price(self):
        if self.order_id.pricelist_id:
            frm_cur = self.env.user.company_id.currency_id
            to_cur = self.order_id.pricelist_id.currency_id
            purchase_price = self.product_id.standard_price
            if self.product_uom != self.product_id.uom_id:
                purchase_price = self.env['product.uom']._compute_price(self.product_id.uom_id.id, purchase_price, to_uom_id=self.product_uom.id)
            ctx = self.env.context.copy()
            ctx['date'] = self.order_id.date_order
            price = frm_cur.with_context(ctx).compute(purchase_price, to_cur, round=False)
            return price
        return 0.0

    @api.model
    def create(self, vals):
        return_obj = super(SaleOrderLine, self).create(vals)
        if not return_obj.purchase_price:
            return_obj.purchase_price = return_obj.get_purchase_price()
        return return_obj
