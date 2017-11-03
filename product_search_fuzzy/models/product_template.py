# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if name and operator in ['ilike', 'like']:
            args = args or []

            string_numbers = [s for s in name.split() if s.isdigit()]
            if string_numbers:
                for string_number in string_numbers:
                    args.append(('name', 'ilike', string_number))

            recs = self.search(
                [('name', '%', name)] + args,
                limit=limit,
                order="similarity(%s.name, '%s') DESC" % (self._table, name)
            )

            if recs:
                return recs.name_get()
        return super(ProductTemplate, self).name_search(name, args=args, operator=operator, limit=limit)

