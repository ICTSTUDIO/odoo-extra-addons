# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
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
from openerp.tools.safe_eval import safe_eval as eval
import openerp.addons.decimal_precision as dp
from openerp.tools.float_utils import float_round
from openerp.exceptions import except_orm

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    qty_available = fields.Float(
            compute="_new_product_available",
            search="_search_template_qty_available",
            digits=dp.get_precision('Product Unit of Measure')
    )
    virtual_available = fields.Float(
            compute="_new_product_available",
            search="_search_template_virtual_available",
            digits=dp.get_precision('Product Unit of Measure')
    )
    incoming_qty = fields.Float(
            compute="_new_product_available",
            search="_search_template_incoming_qty",
            digits=dp.get_precision('Product Unit of Measure')
    )
    outgoing_qty = fields.Float(
            compute="_new_product_available",
            search="_search_template_outgoing_qty",
            digits=dp.get_precision('Product Unit of Measure')
    )


    warehouses = fields.One2many(
            comodel_name="stock.warehouse",
            string="Warehouse Stock",
            related="product_variant_ids.warehouses"
    )

    @api.multi
    def _new_product_available(self):
        for template in self:
            qty_available = 0.0
            incoming_qty = 0.0
            outgoing_qty = 0.0
            virtual_available = 0.0

            for product in template.product_variant_ids:
                qty_available += product.qty_available
                outgoing_qty += product.outgoing_qty
                incoming_qty += product.incoming_qty
                virtual_available += product.virtual_available

            template.qty_available = qty_available
            template.outgoing_qty = outgoing_qty
            template.incoming_qty = incoming_qty
            template.virtual_available = virtual_available

    def _search_template_qty_available(self, operator, value):
        res = self._search_template_filter_quantity(operator, value, 'qty_available')
        return res

    def _search_template_virtual_available(self, operator, value):
        res = self._search_template_filter_quantity(operator, value, 'virtual_available')
        return res

    def _search_template_incoming_qty(self, operator, value):
        res = self._search_template_filter_quantity(operator, value, 'incoming_qty')
        return res


    def _search_template_outgoing_qty(self, operator, value):
        res = self._search_template_filter_quantity(operator, value, 'outgoing_qty')
        return res

    def _get_qty_filter_fields(self):
        return  ['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty']

    def _search_template_filter_quantity(self, operator, value, filter_field):
        prod_search = self.env['product.product']._search_product_filter_quantity(operator, value, filter_field)
        product_variants = self.env['product.product'].search(prod_search)
        return [('product_variant_ids', 'in', product_variants.ids)]