# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Payment Url - Sale Order',
    'version': '8.0.0.0.2',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Create Payment URL from Sale Order',
    'depends': [
        'payment_transaction_id',
    ],
    'data': [
        'views/sale_order.xml',
        'views/payment_transaction.xml',
        'wizard/wizard_sale_order_payment.xml'
    ],
}