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

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    auto_invoice = fields.Selection(
            selection=[
                ('no', 'No Automatic Invoice'),
                ('yes', 'Automatic Invoice'),
                ('valid', 'Automatic Invoice & Validation'),

            ],
            string='Auto Invoice on Delivery',
            default='no'
    )
    auto_invoiced = fields.Boolean(
        string='Automaticly Invoiced',
        compute='_get_auto_invoice',
        store=True
    )

    @api.depends('order_line.move_ids.state')
    def _get_auto_invoice(self):
        for rec in self:

            if rec.auto_invoice in ['yes', 'valid'] and rec.invoice_method == 'manual':
                if all([move.state in ['cancel', 'done'] for move in rec.order_line.move_ids]):
                    invoice = self.env['purchase.order'].sudo().action_invoice_create()
                    if invoice:
                        _logger.debug(
                            'Automaticly Created Invoice: %s',(
                                invoice
                            )
                        )
                        rec.auto_invoiced = True

                        if rec.auto_invoice == ['valid']:
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
