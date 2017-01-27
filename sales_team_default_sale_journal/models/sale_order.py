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
            string="Sale Warehouse",
            required=False
    )

import logging
from openerp import models, fields, api, _

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def _prepare_invoice(self, order, lines):
        vals = super(SaleOrder, self)._prepare_invoice(order, lines)

        if order.section_id:
            if order.section_id.default_sale_journal:
                vals['journal_id'] = order.section_id.default_sale_journal.id

        return vals