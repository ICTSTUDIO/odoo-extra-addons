# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ICTSTUDIO (www.ictstudio.eu).
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

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class DropshipAddress(models.Model):
    _name = "dropship.address"
    _description = "Sropshipment Addresses"

    def _select_type(self):
        return [
            ('shipping', 'Shipping Address'),
        ]

    def _get_default_type(self):
        return 'shipping'

    type = fields.Selection(
        selection=_select_type,
        default=_get_default_type,
    )
    company = fields.Char()
    name = fields.Char()
    street = fields.Char()
    housenumber = fields.Char()
    housenumberaddition = fields.Char()
    zipcode = fields.Char()
    city = fields.Char()
    countrycode = fields.Char()
    email = fields.Char()
    telephone = fields.Char()

    @api.model
    def create_address(self, values):
        #TODO: Check and map values if needed
        return self.create(values)
