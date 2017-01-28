# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Stock Warehouse Transfer',
    'version': '9.0.0.0.1',
    'license': 'AGPL-3',
    'author': 'ICTSTUDIO',
    'website': 'http://www.ictstudio.eu',
    'category': 'Purchase',
    'complexity': 'normal',
    'summary': 'Create a transfer of products between 2 warehouses',
    'depends': [
        'stock',
    ],
    'data': [
        'views/stock_warehouse_transfer.xml',
        'data/ir_sequence.xml',
        'security/ir.model.access.csv'
    ],
}
