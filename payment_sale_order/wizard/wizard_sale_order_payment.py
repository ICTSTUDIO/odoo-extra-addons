# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging
from openerp import api, fields, models, _

_logger = logging.getLogger(__name__)


class WizardSaleOrderPayment(models.TransientModel):
    _name = 'wizard.sale.order.payment'
    _description = 'Create payment for selected orders'

    #TODO: Add filtering on payment gateways providing payment link creation
    acquirer_id = fields.Many2one(
        comodel_name='payment.acquirer',
        string="Payment Acquirer"
    )

    @api.multi
    def create_payment(self):
        active_ids = self.env.context.get('active_ids', [])
        search_args = [
            ('id', 'in', active_ids),
            ('payment_tx_id', '=', False)
        ]

        orders = self.env['sale.order'].search(search_args)

        for order in orders:
            transaction = self._create_payment_transaction(order)
            if not transaction:
                _logger.debug("Unable to create transaction for order: %s", order)
                continue
            _logger.debug("ODOO Transaction created: %s", transaction)
            #transaction._




        return {}

    @api.multi
    def _create_payment_transaction(self, order):
        transaction_obj = self.env['payment.transaction']

        transaction = transaction_obj.s2s_create(
            {
                'acquirer_id': self.acquirer_id.id,
                'type': 'server2server',
                'amount': order.amount_total,
                'currency_id': order.pricelist_id.currency_id.id,
                'partner_id': order.partner_id.id,
                'partner_country_id': order.partner_id.country_id.id,
                'reference': transaction_obj.get_next_reference(order.name),
                'sale_order_id': order.id,
            },
            {}
        )
        if transaction:
            order.write(
                {
                    'payment_acquirer_id': self.acquirer_id.id,
                    'payment_tx_id': transaction
                }
            )

        return transaction or False
