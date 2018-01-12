# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Purchase Stock Levels',
    'version': '9.0.0.1.4',
    'category': 'Purchase',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Show stock levels on purchases',
    'depends': [
        'base',
        'purchase',
        'stock',
        ],
    'data': [
        'views/purchase_order.xml',
    ],
}
