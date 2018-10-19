# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)
{
    'name': 'Sale Order Kanban',
    'version': '10.0.1.0.1',
    'category': '',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'LGPL-3',
    'summary': 'Add stages to Sale Order Kanban, define your own stages',
    'depends': [
        'sale',
        'base_kanban_stage',
    ],
    'data': [
        'views/sale_order.xml',
    ],
    'installable': True,
}
