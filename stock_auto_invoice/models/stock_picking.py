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
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import workflow

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.returns('account.journal', lambda r: r.id)
    def _get_journal(self):
        journal_type = self._get_journal_type()
        journal = self.env['account.journal'].search(
            [('type', '=', journal_type)], limit=1)
        if not journal:
            raise except_orm(_('No Journal!'),
                             _("You must define an journal of type '%s'!") % (
                             journal_type,))
        return journal[0]

    def _get_journal_type(self):

        if not self.move_lines:
            return 'sale'
        else:
            src_usage = self.move_lines[0].location_id.usage
            dest_usage = self.move_lines[0].location_dest_id.usage
            type = self.picking_type_id.code
            if type == 'outgoing' and dest_usage == 'supplier':
                journal_type = 'purchase_refund'
            elif type == 'outgoing' and dest_usage == 'customer':
                journal_type = 'sale'
            elif type == 'incoming' and src_usage == 'supplier':
                journal_type = 'purchase'
            elif type == 'incoming' and src_usage == 'customer':
                journal_type = 'sale_refund'
            else:
                journal_type = 'sale'
            return journal_type

    def get_purchase_id(self):
        return self.env['purchase.order'].search([('picking_ids','in',self.id)])


    @api.model
    def create_and_validate_invoice(self, picking_ids, validate=False):
        for picking in self.browse(picking_ids):
            journal = self._get_journal()

            invoices = picking.action_invoice_create(
                    journal.id,
            )
            if validate:
                for invoice in invoices:
                    workflow.trg_validate(
                            self.sudo()._uid,
                            'account.invoice',
                            invoice,
                            'invoice_open',
                            self._cr
                    )


    @api.multi
    def do_transfer(self):
        """
            On transfer create invoice
        """
        return_val = super(StockPicking, self).do_transfer()

        try:
            for rec in self:
                invoice_picking_ids = []
                invoice_valid_picking_ids = []
                if rec.picking_type_id.code == 'outgoing' and rec.sale_id:
                    if rec.sale_id.auto_invoice in ['yes', 'valid'] and rec.sale_id.order_policy == 'picking' and rec.invoice_state == '2binvoiced':
                        if rec.sale_id.auto_invoice == ['valid']:
                            invoice_valid_picking_ids.append(rec.id)
                        else:
                            invoice_picking_ids.append(rec.id)
                elif rec.picking_type_id.code == 'incoming' and rec.get_purchase_id():
                    purchases = rec.get_purchase_id()
                    if purchases:
                        purchase = purchases[0]
                        if rec.purchase.auto_invoice in ['yes', 'valid'] and purchase.invoice_method == 'picking' and rec.invoice_state == '2binvoiced':
                            if rec.purchase.auto_invoice == ['valid']:
                                invoice_valid_picking_ids.append(rec.id)
                            else:
                                invoice_picking_ids.append(rec.id)

                rec.create_and_validate_invoice(invoice_picking_ids)
                rec.create_and_validate_invoice(invoice_valid_picking_ids, validate=True)
        except:
            _logger.error("Unable to automaticly create invoice")

        return return_val
