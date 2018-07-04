# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    'name': 'Sale Report - Product Main Group Extension',
    'version': '10.0.0.0.2',
    'license': 'LGPL-3',
    'author': 'ICTSTUDIO, André Schenkels',
    'category': 'Accounting & Finance',
    'depends': [
        'sale',
        'product_maingroup'
        ],
    'data': [
        'report/account_invoice_report.xml',
        'report/sale_report.xml',
        ],
    'installable': True,
}
