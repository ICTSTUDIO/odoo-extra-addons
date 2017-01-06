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

import urllib
import logging
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    dropship_address = fields.Many2one(
            comodel_name='dropship.address',
            string='Dropship Address',
    )

    @api.model
    def _prepare_procurement_group(self, order):
        res = super(SaleOrder, self)._prepare_procurement_group(order)
        if res and order.dropship_address:
            res['dropship_address'] = order.dropship_address.id
        return res