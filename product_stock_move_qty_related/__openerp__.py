# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Product Stock Move Qty Related Picking',
    'version': '8.0.1.0.1',
    'category': 'Stock Management',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Intermediate Module between Product Stock Move Qty and Related Picking',
    'depends': [
        'product_stock_move_qty',
        'stock_picking_related_picking'
    ],
    'data': [
        'views/stock_move_location.xml',
    ],
}

