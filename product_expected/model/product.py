# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
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

from openerp import models, fields, api, _
from openerp.tools.translate import _
import xmlrpclib
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit="product.product"

    def get_expected_date(self):
        """
        Retreive the max delivery date of picking associated with stock moves of product
        :return: minimum delivery date
        """

        for rec in self:
            min_date = False

            moves = self.env['stock.move'].search(
                [
                    ("product_id", "=", rec.id),
                    ("state", "=", "assigned"),
                    ("picking_type_id.code", "=", "incoming")
                ]
            )
            for move in moves:
                if move.picking_id and move.picking_id.max_date:
                    if min_date and move.picking_id.max_date < min_date:
                        min_date = move.picking_id.max_date
                    else:
                        min_date = move.picking_id.max_date
            rec.expected_date = min_date

    expected_date = fields.Date(
        string="Expected Date",
        compute="get_expected_date"
    )

