# -*- coding: utf-8 -*-
# Copyright© 2018-today  ICTSTUDIO <http://www.ictstudio.eu>
# License: LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)

{
    "name": "Support branding Responsive",
    "category": "Dependecy/Hidden",
    "version": "10.0.0.0.1",
    "license": "LGPL-3",
    "author": "ICTSTUDIO",
    "website": 'http://www.ictstudio.eu',
    "depends": [
        'web_responsive',
    ],
    "qweb": [
        'static/src/xml/base.xml',
    ],
    "data": [
        "data/ir_config_parameter.xml",
        'views/qweb.xml',
    ],
    'installable': True,
}
