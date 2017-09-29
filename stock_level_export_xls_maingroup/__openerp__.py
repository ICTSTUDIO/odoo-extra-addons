# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
{
    'name': 'Product MainGroup - Stock Level Export XLS Extension',
    'version': '8.0.0.0.1',
    'category': 'Stock',
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'license': 'AGPL-3',
    'summary': 'Extension module for Stock Level Export XLS report',
    'depends': [
        'stock', 'report_xls',
        'product_maingroup'
    ],
    'data': [
        'wizard/wiz_export_stock_maingroup_level.xml'
    ],
}