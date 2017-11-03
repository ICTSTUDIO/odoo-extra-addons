# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if operator in ['ilike', 'like']:
            args = args or []

            string_numbers = [s for s in name.split() if s.isdigit()]
            if string_numbers:
                for string_number in string_numbers:
                    args.append(('display_name', 'ilike', string_number))

            recs = self.search(
                [('display_name', '%', name)] + args,
                limit=limit,
                order="similarity(%s.display_name, '%s') DESC" % (self._table, name)
            )
            return recs.name_get()
        return super(ResPartner, self).name_search(name, args=args, operator=operator, limit=limit)


