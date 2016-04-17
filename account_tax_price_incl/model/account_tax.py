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

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class AccountTax(models.Model):

    @api.model
    def _fix_tax_included_price(self, price, prod_taxes, line_taxes):
        """Subtract tax amount from price when corresponding "price included" taxes do not apply"""

        new_price = super(AccountTax, self)._fix_tax_included_price(price, prod_taxes, line_taxes)

        prod_incl_tax = [tax for tax in prod_taxes if tax.id not in line_taxes and tax.price_include]
        line_incl_tax = [tax for tax in line_taxes if tax.price_include]

        if prod_incl_tax and line_incl_tax:
            #FIXME: If both are included tax the tax could be different
            return price

        return new_price

