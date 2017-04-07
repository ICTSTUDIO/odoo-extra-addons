# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Sale Report - Partner Filters',
    'version': '8.0.0.0.1',
    'category': 'Sales & Invoicing',
    'summary': """Extra Partner Group by filters for Sale Reporting
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
    ],
}
