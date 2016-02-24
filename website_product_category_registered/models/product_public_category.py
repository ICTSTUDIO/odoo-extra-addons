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

from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)

class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        realtion='partner_public_category_rel',
        column1='public_category_id',
        column2='partner_id'
    )
    partner_count = fields.Integer(
        compute="_compute_partner_count",
        string="Partner Count",
        store=True
    )

    @api.one
    @api.depends('partner_ids')
    def _compute_partner_count(self):
        self.partner_count=len(self.partner_ids)