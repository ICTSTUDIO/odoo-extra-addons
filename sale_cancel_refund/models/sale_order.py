# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
from openerp import api, models, fields, _
from openerp.exceptions import Warning as UserError

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_refund_journal(self):

        journal = self.env['account.journal'].search(
                [
                    ('type', '=', 'out_refund'),
                    ('company_id', '=', self.env.user.company_id.id)
                ],
                limit=1
        )
        return journal and journal[0] or False

    @api.multi
    def action_create_refund(self):
        refunds = self.env['account.invoice']
        if len(self.invoice_ids) == 1 and self.invoice_ids.type == 'out_invoice':
            for inv in self.invoice_ids:
                date = fields.Date.today()
                period = inv.period_id and inv.period_id.id or False
                description = inv.internal_number and 'Credit: %s' % inv.internal_number or 'Credit'
                journal = self._get_refund_journal() or inv.journal_id

                refund = inv.refund(date, period, description, journal.id)
                #refund = self.env['account.invoice'].browse(refund_id[0])
                refund.write(
                        {
                            'date_due': date,
                            'check_total': inv.check_total
                        }
                )
                refund.button_compute()
                refunds += refund
            return refunds

    @api.multi
    def action_advanced_cancel(self):

        # Cancel Picking
        if len(self.picking_ids) == 1 and self.picking_ids.state not in ('done'):
            pick = self.picking_ids[0]
            if 'wave_id' in pick._fields and pick.wave_id:
                raise UserError (
                    _("Order is being picked!"),
                    _("First pull picking from Picking Wave: %s") % pick.wave_id.name
                )
            try:
                pick.action_cancel()
            except:
                _logger.debug("Error Cancel Picking")
            try:
                for line in self.order_line:
                    line.procurement_ids.cancel()
            except:
                _logger.debug("Error Cancel Sale Order Procurements")

        elif len(self.picking_ids) == 1:
            raise UserError(
                    _("Order has been picked!"),
                    _("Unable to cancel a picking already done")
            )

        #Create Refund
        res = self.action_create_refund()
        _logger.debug("Create Refund: %s", res)

        line.state = 'cancel'

        return True

    @api.multi
    def action_cancel(self):
        self.ensure_one()
        # ctx = dict(self._context, refund_invoice=True, cancel_pickings=True)

        if self.order_policy == 'manual' and len(self.invoice_ids) == 1:
            self.action_advanced_cancel()

            self.state = 'cancel'
            return True
        else:
            return super(SaleOrder, self).action_cancel()
