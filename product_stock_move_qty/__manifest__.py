# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Product Stock Move Qty',
    'version': '10.0.1.2.1',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'category': 'Stock Management',
    'summary': 'Show Product Stock Moves Qty for Location/Warehouse',
    'depends': ['stock'],
    'data': [
        'views/stock_move_location.xml',
        'views/product_template.xml',
        'views/product_product.xml',
        'security/ir.model.access.csv'
    ],
    'installable': True,
}

