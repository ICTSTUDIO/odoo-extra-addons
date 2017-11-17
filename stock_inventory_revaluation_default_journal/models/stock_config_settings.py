# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import fields, models


class StockConfigSettings(models.TransientModel):
    _inherit = 'stock.config.settings'

    default_revaluation_journal_id = fields.Many2one(
        related=['company_id', 'default_revaluation_journal_id'],
        default=lambda self:
        self.env.user.company_id.default_revaluation_journal_id,
    )
