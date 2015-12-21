# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) 2015 ERP|OPEN (www.erpopen.nl).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp import models, fields, api, _
from openerp import workflow

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = "sale.order"

    auto_invoice = fields.Boolean(
        string='Auto Invoice on Delivery',
        default=True
    )
    auto_invoiced = fields.Boolean(
        string='Automaticly Invoiced',
        compute='_get_auto_invoice',
        store=True
    )

    @api.depends('order_line.procurement_ids.state')
    def _get_auto_invoice(self):
        for rec in self:
            group = rec.procurement_group_id
            if group and rec.auto_invoice and rec.order_policy == 'manual':
                if all([proc.state in ['cancel', 'done'] for proc in group.procurement_ids]):

                    invoice = self.env['sale.order'].sudo().action_invoice_create()
                    if invoice:
                        _logger.debug(
                            'Automaticly Created Invoice: %s',(
                                invoice
                            )
                        )
                        rec.auto_invoiced = True
                        _logger.debug('Validating Invoice: %s',(invoice))
                        workflow.trg_validate(
                            self.sudo()._uid,
                            'account.invoice',
                            invoice,
                            'invoice_open',
                            self._cr
                        )
                    else:
                        _logger.debug(
                            'Error automatic Invoice creation for order: %s',(
                                rec.id
                            )
                        )
                        rec.auto_invoiced = False
                else:
                    rec.auto_invoiced = False
