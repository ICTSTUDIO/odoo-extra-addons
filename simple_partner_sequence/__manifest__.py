# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{
    'name': 'Simple Partner Sequence',
    'version': '10.0.0.0.1',
    'category': 'Partner Management',
    'author': 'ICTSTUDIO, André Schenkels',
    'license': 'AGPL-3',
    'website': 'http://www.ictstudio.eu',
    'summary': """Simple way of adding automated sequences to partners """,
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        'views/res_partner_sequence.xml',
        'data/ir_sequence_res_partner.xml',
        'security/ir.model.access.csv'
    ],
    'installable': False,
}
