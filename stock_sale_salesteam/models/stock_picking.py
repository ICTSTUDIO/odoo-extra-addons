# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    section_id = fields.Many2one(
            compute='_get_section_id',
            comodel_name='crm.case.section',
            string='Sales Team',
            store=True,
            index=True
    )

    @api.one
    @api.depends('sale_id')
    def _get_section_id(self):
        if self.sale_id and self.sale_id.section_id:
            self.section_id = self.sale_id.section_id