# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Sale Line Delivered Qty',
    'version': '8.0.1.0.1',
    'category': 'MRP',
    'summary': """Quantity Delivered and Invoiced on Sale Line
    """,
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'depends': [
        'stock_move_sale_line',
    ],
    'data': [
        'views/sale_order.xml'
    ],
}