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


class StockPackOperation(models.Model):
    _inherit = "stock.pack.operation"

    remark = fields.Text(string="Remark")
    product_location = fields.Char(
            string="Location",
            compute="_compute_product_location",
            store=True
    )

    @api.one
    @api.depends('product_id')
    def _compute_product_location(self):
        self.product_location = self.product_id.loc_rack
        if self.product_id.loc_row:
            self.product_location += self.product_id.loc_row
        if self.product_id.loc_case:
            self.product_location += self.product_id.loc_case
