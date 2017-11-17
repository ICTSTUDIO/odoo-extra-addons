# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import api, fields, models, _



class StockInventoryRevaluation(models.Model):
    _inherit = 'stock.inventory.revaluation'

    @api.model
    def _default_journal(self):
        if self.env.user.company_id.default_revaluation_journal_id:
            res = self.env.user.company_id.default_revaluation_journal_id
        else:
            res = self.env['account.journal'].search([('type', '=', 'general')])
        return res and res[0] or False

    journal_id = fields.Many2one(default=_default_journal)