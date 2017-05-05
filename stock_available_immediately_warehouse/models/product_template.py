# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    @api.depends('virtual_available', 'incoming_qty')
    def _immediately_usable_qty(self):
        """Ignore the incoming goods in the quantity available to promise

        This is the same implementation as for variants."""
        super(ProductTemplate, self)._immediately_usable_qty()
        for tmpl in self:
            check_context = ('location','location_id','warehouse','warehouse_id')
            if not self.env.context or not (any([i in check_context for i in self.env.context])):
                imm_usable_qty = 0
                for warehouse in self.env['stock.warehouse'].search(
                        [
                            ('use_for_available_immediately', '=', True)
                        ]
                ):
                    ctx = dict(self._context, warehouse=warehouse.id)
                    imm_usable_qty += tmpl.with_context(ctx).virtual_available - tmpl.with_context(ctx).incoming_qty
                tmpl.immediately_usable_qty = imm_usable_qty
