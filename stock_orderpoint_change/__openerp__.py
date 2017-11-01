# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Stock Warehouse Orderpoint - Change',
    'version': '8.0.0.0.2',
    'license': 'AGPL-3',
    'author': 'ICTSTUDIO',
    'website': 'http://www.ictstudio.eu',
    'category': 'Purchase',
    'complexity': 'normal',
    'summary': 'When changing the parameters in the orderpoint the procurements needs to be cancelled and all chained.',
    'depends': [
        'procurement_order_chain',
    ],
    'data': [
        'views/stock_warehouse_orderpoint.xml',
        'views/procurement_rule.xml',
    ],
}
