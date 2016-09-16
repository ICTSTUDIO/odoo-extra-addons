# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Purchase Auto Invoice',
    'version': '8.0.1.1.1',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'category': 'Purchase Management',
    'summary': """Automaticly create invoice on receiving goods
    """,
    'depends': [
        'purchase',
    ],
    'data': [
        'views/purchase_order.xml',
    ],
}
