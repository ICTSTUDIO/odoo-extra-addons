# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import models, fields, api, _
from openerp.exceptions import except_orm, Warning, RedirectWarning
from openerp import workflow

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = "stock.picking"

    auto_invoiced = fields.Boolean(
            string='Automaticly Invoiced',
            compute='_get_auto_invoice',
            store=True
    )

    @api.one
    @api.depends('state')
    def _get_auto_invoice(self):
        ctx2 = dict(self._context, auto_invoice=self.id)
        if self._context.get('auto_invoice') and self._context.get('auto_invoice') == self.id:
            _logger.debug("Picking: %s Already Invoiced", self.id)
        elif self.invoice_state == '2binvoiced':
            if all([move.state in ['cancel', 'done'] for move in self.move_lines]):

                # Invoice Picking Related to Sale
                if self.picking_type_id.code == 'outgoing' and self.sale_id:
                    ctx = dict(ctx2, inv_type='out_invoice')
                    if self.sale_id.auto_invoice in ['yes', 'valid'] and self.sale_id.order_policy == 'picking':
                        if self.sale_id.auto_invoice == 'valid':
                            self.with_context(ctx).create_and_validate_invoice(validate=True, type='out_invoice')
                        else:
                            self.with_context(ctx).create_and_validate_invoice(type='out_invoice')
                        self.auto_invoiced = True

                # Invoice Picking Related to Purchase
                elif self.picking_type_id.code == 'incoming' and self.get_purchases():
                    ctx = dict(ctx2, inv_type='in_invoice')
                    purchases = self.get_purchases()
                    if purchases:
                        purchase = purchases[0]
                        if purchase.auto_invoice in ['yes', 'valid'] and purchase.invoice_method == 'picking':
                            if purchase.auto_invoice == 'valid':
                                self.with_context(ctx).create_and_validate_invoice(validate=True, type='in_invoice')
                            else:
                                self.with_context(ctx).create_and_validate_invoice(type='in_invoice')
                            self.auto_invoiced = True

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


    def get_purchases(self):
        purchases = self.env['purchase.order']
        for line in self.move_lines:
            if line.purchase_line_id:
                if line.purchase_line_id.order_id not in purchases:
                    purchases += line.purchase_line_id.order_id
        _logger.debug("Purchase Orders: %s, Related to Picking: %s", purchases, self.name)
        return purchases


    @api.multi
    def create_and_validate_invoice(self, validate=False, type='out_invoice'):
        self.ensure_one()
        journal = self._get_journal()

        invoices = self.action_invoice_create(
                journal.id, type=type
        )
        _logger.debug("Invoices: %s", invoices)
        if validate:
            for invoice in invoices:
                _logger.debug('Validating Invoice: %s',(invoice))
                workflow.trg_validate(
                        self.sudo()._uid,
                        'account.invoice',
                        invoice,
                        'invoice_open',
                        self._cr
                )


    # @api.multi
    # def do_transfer(self):
    #     """
    #         On transfer create invoice
    #     """
    #     return_val = super(StockPicking, self).do_transfer()
    #
    #     try:
    #         for rec in self:
    #             if rec.picking_type_id.code == 'outgoing' and rec.sale_id:
    #                 ctx = dict(self._context, inv_type='out_invoice')
    #                 if rec.sale_id.auto_invoice in ['yes', 'valid'] and rec.sale_id.order_policy == 'picking' and rec.invoice_state == '2binvoiced':
    #                     if rec.sale_id.auto_invoice == 'valid':
    #                         rec.with_context(ctx).create_and_validate_invoice(validate=True, type='out_invoice')
    #                     else:
    #                         rec.with_context(ctx).create_and_validate_invoice(type='out_invoice')
    #             elif rec.picking_type_id.code == 'incoming' and rec.get_purchases():
    #                 ctx = dict(self._context, inv_type='in_invoice')
    #                 purchases = rec.get_purchases()
    #                 if purchases:
    #                     purchase = purchases[0]
    #                     if purchase.auto_invoice in ['yes', 'valid'] and purchase.invoice_method == 'picking' and rec.invoice_state == '2binvoiced':
    #                         if purchase.auto_invoice == 'valid':
    #                             rec.with_context(ctx).create_and_validate_invoice(validate=True, type='in_invoice')
    #                         else:
    #                             rec.with_context(ctx).create_and_validate_invoice(type='in_invoice')
    #     except:
    #          _logger.error("Unable to automaticly create invoice")
    #
    #     return return_val
