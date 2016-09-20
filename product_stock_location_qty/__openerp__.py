# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Product Stock Location Qty',
    'version': '8.0.1.1.2',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'category': 'Stock Management',
    'summary': 'Show Product Qty On Stock for Location',
    'depends': ['product_stock_move_qty'],
    'data': [
        'views/stock_product_location.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'security/ir.model.access.csv',
    ],
}
