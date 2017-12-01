# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Payment Url - Invoices',
    'version': '8.0.0.0.1',
    'category': 'Payment Management',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Create Payment URL from Invoice',
    'depends': [
        'payment',
        'account'
    ],
    'data': [
        'views/account_invoice.xml',
    ],
}