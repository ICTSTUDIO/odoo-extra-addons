# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 ICTSTUDIO (<http://www.ictstudio.eu>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Partner Country Sequence',
    'version': '1.0',
    'category': 'Sales',
    'description': """Use the standard reference field on partner for the unique partner number. Adds
    extra sequence type: Partner and a sequence with code res.partner. As default this sequence will be
    used to assign to partners. You can use the Partner Sequence forms to set different sequence for a country.
    The partner number will be added to the partner just like with the Products in ODOO.""",
    'author': 'ICTSTUDIO, André Schenkels',
    'website': 'http://www.ictstudio.eu',
    'depends': [
        'base',
    ],
    'data': [
        'view/partner_view.xml',
        'data/partner_sequence.xml',
        'security/ir.model.access.csv'
    ],
    }
