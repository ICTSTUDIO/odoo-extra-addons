# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Sale Auto Invoice',
    'version': '8.0.1.1.1',
    'category': 'Sales & Invoicing',
    'summary': """Automatic creation of invoice on transfer of delivery
    """,
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'depends': [
        'sale_stock',
        'stock_account',
    ],
    'data': [
        'views/sale_order.xml',
    ],
}
