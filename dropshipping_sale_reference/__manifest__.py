# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Dropshipping Client Order Reference',
    'version': '11.0.0.0.1',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'LGPL-3',
    'summary': 'Provide Sale Order Reference on Purchase Order Dropshipment',
    'depends': [
        'stock_dropshipping'
    ],
    'data': [
        'views/purchase_order.xml',
    ],
    'installable': False,
}