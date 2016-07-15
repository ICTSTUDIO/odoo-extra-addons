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


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def name_get(self):
        _logger.debug("NG Context: %s", self.env.context)
        if self.env.context.get('return_line'):
            res = []
            for rec in self:

                if rec.product_id:
                    name = rec.product_id.name
                if rec.product_id.code:
                    name = "[" + str(rec.product_id.code) + "] " + name
                if rec.product_qty:
                    name = name + " (" + str(rec.product_qty) + ")"
                res.append((rec.id, name))
        else:
            res = super(StockMove, self).name_get()
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        _logger.debug("NS Context: %s", self.env.context)
        if self.env.context.get('return_line'):
            args = args or []
            if name:
                product_args = ['|',
                                   ('name', operator, name),
                                   ('default_code', operator, name)
                               ]

                products = self.env['product.product'].search(product_args)
                args = [('product_id', 'in', products.ids)]
                args = [('picking_id', '=', self.env.context.get('return_line'))] + args
            moves = self.search(args, limit=limit)
            return moves.with_context(return_line=self.env.context.get('return_line')).name_get()
        else:
            return super(StockMove, self).name_search(
                    name,
                    args=args,
                    operator=operator,
                    limit=limit
            )