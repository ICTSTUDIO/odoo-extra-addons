# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Product Sale Report',
    'version': '8.0.0.0.2',
    'category': 'Sales & Invoicing',
    'summary': """Direct link from product form to Repoorting Invoice Analysis
    """,
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'depends': [
        'sale_stock',
        'account',
    ],
    'data': [
        'views/sale_report.xml',
        'views/product_product.xml',
        'views/product_template.xml',
    ],
}
