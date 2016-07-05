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

_logger = logging.getLogger(__name__)

class product_template(models.Model):
    _inherit = 'product.template'

    @api.one
    def _get_pricelists(self):
        self.pricelists = self.env['product.pricelist'].search(
                [
                    ('show_on_products', '=', True)
                ]
        )

    def _set_pricelists(self):
        for pricelist in self.pricelists:
            if pricelist.product_price:
                _logger.debug("Updating Price: %s", pricelist.product_price)
                pricelist.price_set(self, pricelist.product_price)
    
    pricelists = fields.One2many(
            comodel_name="product.pricelist",
            string="Pricelists",
            compute="_get_pricelists",
            inverse="_set_pricelists"
    )

