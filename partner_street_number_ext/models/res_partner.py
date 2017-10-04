# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import re
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.one
    @api.depends('street_name', 'street_number', 'street_number_ext')
    def _get_street(self):
        self.street = ' '.join(
            filter(None,
                   [
                       self.street_name,
                       self.street_number,
                       self.street_number_ext
                   ]))

    def _write_street(self):
        """
        Simplistically try to parse in case a value should get written
        to the 'street' field (for instance at import time, which provides
        us with a way of easily restoring the data when this module is
        installed on a database that already contains addresses).
        """
        for rec in self:
            street_name = rec.street and rec.street.strip() or False
            street_number = False
            street_number_ext = False
            if rec.street:
                match = re.search(r'(.+)\s+(\d.*)\s(.+)', rec.street.strip())
                if match and len(match.group(2)) < 6:
                    street_name = match.group(1)
                    street_number = match.group(2)
                    street_number_ext = match.group(3)
                else:
                    match = re.search(r'(.+)\s+(\d.*)', rec.street.strip())
                    if match and len(match.group(2)) < 6:
                        street_name = match.group(1)
                        street_number = match.group(2)
                        street_number_ext = False

            rec.street_name = street_name or False
            rec.street_number = street_number or False
            rec.street_number_ext = street_number_ext or False


    @api.model
    def _address_fields(self):
        res = super(ResPartner, self)._address_fields()
        return res + ['street_number_ext']

    street_number_ext = fields.Char('Street number extension')

    street = fields.Char(
        compute='_get_street', store=True, inverse='_write_street')
