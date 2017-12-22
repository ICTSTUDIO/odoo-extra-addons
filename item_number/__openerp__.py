# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Item Number',
    'version': '8.0.0.0.2',
    'category': 'Sales Management',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Add Item numbers to Sale Orders, Pickings and Invoices',
    'depends': [
        'sale_stock',
        'account'
    ],
    'data': [
        'views/account_invoice.xml',
        'views/sale_config_settings.xml',
        'views/sale_order.xml',
        'views/stock_move.xml',
        'views/report_sale_order.xml',
        'views/report_stock_picking.xml',
        'views/report_account_invoice.xml',
    ],
}
