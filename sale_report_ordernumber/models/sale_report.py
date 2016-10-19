# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp import workflow

_logger = logging.getLogger(__name__)

class SaleReport(models.Model):
    _inherit = "sale.report"

    order_name = fields.Char(string="Ordernumber")

    def _select(self):
        select_str = super(SaleReport, self)._select()
        return select_str + ',s.name as order_name'

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        return group_by_str + ',s.name'