# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Point of Sale - Accounting Valuation Fix',
    'version': '8.0.0.0.1',
    'category': 'Point of Sale',
    'summary': """Fix the wrong accounting entry when using the Point of Sale system
    """,
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'depends': [
        'point_of_sale',
        'stock_account'
    ],
    'data': [
        'view/pos_config.xml',
    ],
}
