# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models, api, _


class MatrixRoleCompany(models.Model):
    _name = 'matrix.role.company'
    _rec_name = 'role_name'

    role_name = fields.Char()
    role = fields.Many2one(
        comodel_name='res.users.role',
        string='Linked to Role'
    )
    company = fields.Many2one(
        comodel_name='res.company',
        string='Label'
    )

