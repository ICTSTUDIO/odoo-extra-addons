# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Simple Product Sequence',
    'version': '9.0.0.0.1',
    'category': 'Product Management',
    'description': """Adding Product Sequence to the default_code field""",
    'author': 'ICTSTUDIO | André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'product',
               ],
    'data': ['data/ir_sequence_product_product.xml',
        ],
    
    'installable': True,
    }
