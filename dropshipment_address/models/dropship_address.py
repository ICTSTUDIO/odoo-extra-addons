# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from odoo import models, fields, api

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
