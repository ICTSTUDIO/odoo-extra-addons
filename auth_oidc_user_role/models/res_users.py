# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _auth_oauth_get_roles(self, validation=False):
        if not validation and self.oauth_provider_id and self.oauth_access_token:
            validation = self._auth_oauth_validate(self.oauth_provider_id.id, self.oauth_access_token)
        if validation:
            if validation.get('role'):
                return validation.get('role')
            if validation.get('members'):
                return validation.get('members')
        return []

    @api.model
    def _auth_oauth_signin(self, provider, validation, params):
        login = super(ResUsers, self)._auth_oauth_signin(provider, validation, params)
        if login:
            user = self.search([('login', '=', login)])
            user._auth_set_name(validation)
            user._auth_set_roles(validation=validation)
        return login

    @api.model
    def _signup_create_user(self, values):
        if values.get('name'):
            values.update({'firstname': '',
                           'lastname': values.get('name')})
        return super(ResUsers, self)._signup_create_user(values)

    @api.model
    def _auth_set_name(self, values):
        self.ensure_one()
        if values.get('name'):
            if self.name != values.get('name'):
                self.write({'lastname': values.get('name'),
                            'firstname': ''})

    @api.model
    def _auth_set_roles(self, validation=False, specific_company_id=False):
        self.ensure_one()
        current_auth_list = self._auth_oauth_get_roles(validation=validation)
        ctx = self._context.copy()
        company_id = False
        roles = self.env['res.users.role']
        ctx.update({'no_auth_role_changes': 1})
        if current_auth_list and not self._context.get('no_auth_role_changes'):
            match_matrix = self.env['matrix.role.company'].sudo().search(
                [
                    ('role_name', 'in', current_auth_list)
                ]
            )

            companies = match_matrix.mapped('company')

            if len(companies) == 0:
                company_id = 1
            else:
                company_id = companies[0].id

            if specific_company_id:
                company_id = specific_company_id

            matrix_filtered = match_matrix.filtered(lambda r: not r.company or r.company and r.company.id == company_id)
            roles = matrix_filtered.mapped('role')

        if roles:
            rem_role_lines = self.env['res.users.role.line'].search([('user_id', '=', self.id), ('role_id', 'not in', roles.ids)])
            rem_role_lines.unlink()

            active_role_lines = self.env['res.users.role.line'].search([('user_id', '=', self.id), ('role_id', 'in', roles.ids)])
            active_roles = active_role_lines.mapped("role_id")

            add_roles = roles - active_roles
            add_role_lines = []
            for add_role in add_roles:
                add_role_lines.append((0, 0, {'role_id': add_role.id}))

            write_values = {
                'company_id': company_id,
                'company_ids': [(6, 0, companies.ids)],
                'role_line_ids': add_role_lines
            }

        else:
            write_values = {
                'company_id': False,
                'company_ids': [(5)],
                'role_line_ids': [(5)]
            }
        if specific_company_id or self._context.get('no_auth_role_changes'):
            del write_values['company_id']
            del write_values['company_ids']
        return self.with_context(ctx).write(write_values)

    @api.multi
    def write(self, vals):
        ret = super(ResUsers, self).write(vals)
        if vals.get('company_id') and len(self) == 1:
            if self.env.uid == self.id:
                self.sudo()._auth_set_roles(specific_company_id=vals.get('company_id'))
        return ret