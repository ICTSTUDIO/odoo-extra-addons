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
            # search="_new_search_product_quantity",
            digits=dp.get_precision('Product Unit of Measure')
    )
    virtual_available = fields.Float(
            compute="_new_product_available",
            # search="_new_search_product_quantity",
            digits=dp.get_precision('Product Unit of Measure')
    )
    incoming_qty = fields.Float(
            compute="_new_product_available",
            # search="_new_search_product_quantity",
            digits=dp.get_precision('Product Unit of Measure')
    )
    outgoing_qty = fields.Float(
            compute="_new_product_available",
            # search="_new_search_product_quantity",
            digits=dp.get_precision('Product Unit of Measure')
    )


    warehouses = fields.One2many(
            comodel_name="stock.warehouse",
            string="Warehouse Stock",
            related="product_variant_ids.warehouses"
    )

    @api.one
    def _new_product_available(self):
        qty_available = 0.0
        incoming_qty = 0.0
        outgoing_qty = 0.0
        virtual_available = 0.0

        for product in self.product_variant_ids:
            qty_available += product.qty_available
            outgoing_qty += product.outgoing_qty
            incoming_qty += product.incoming_qty
            virtual_available += product.virtual_available

        self.qty_available = qty_available
        self.outgoing_qty = outgoing_qty
        self.incoming_qty = incoming_qty
        self.virtual_available = virtual_available
