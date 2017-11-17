# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    default_revaluation_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Default Revaluation Journal',
        domain=[('type', '=', 'general')])
