# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Stock Picking Moves Seperate',
    'version': '8.0.0.1.2',
    'category': 'Stock',
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Work with the Moves of the Picking in a seperate window',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_picking.xml',
        'views/stock_move.xml',
        'wizard/stock_move_done.xml',
        'wizard/stock_move_cancel.xml'
    ],
}