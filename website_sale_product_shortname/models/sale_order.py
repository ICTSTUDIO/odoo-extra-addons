# -*- coding: utf-8 -*-
import random
import openerp

from openerp import SUPERUSER_ID, tools
import openerp.addons.decimal_precision as dp
from openerp.osv import osv, orm, fields
from openerp.addons.web.http import request
from openerp.tools.translate import _
from openerp.exceptions import UserError


class sale_order(osv.Model):
    _inherit = "sale.order"

    def _website_product_id_change(self, cr, uid, ids, order_id, product_id, qty=0, context=None):
        context = dict(context or {})
        values = super(sale_order, self)._website_product_id_change(
                cr, uid, ids, order_id, product_id, qty=qty, context=context
        )

        order = self.pool['sale.order'].browse(cr, SUPERUSER_ID, order_id, context=context)
        product_context = context.copy()
        product_context.update({
            'lang': order.partner_id.lang,
            'partner': order.partner_id.id,
            'quantity': qty,
            'date': order.date_order,
            'pricelist': order.pricelist_id.id,
        })
        product = self.pool['product.product'].browse(cr, uid, product_id, context=product_context)

        values['name'] = product.display_name
        return values