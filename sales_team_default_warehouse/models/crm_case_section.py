# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)



class CrmCaseSection(models.Model):
    _inherit = 'crm.case.section'


    default_warehouse = fields.Many2one(
            comodel_name="stock.warehouse",
            string="Default Warehouse",
            required=False
    )
