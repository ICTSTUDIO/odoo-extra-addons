# -*- coding: utf-8 -*-
# Copyright© 2016 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)


import logging

from openerp import api, models, fields, _
from openerp.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class ResPartner(models.Model):
    _inherit = 'res.partner'


    ref = fields.Char(
        string="Reference",
        required=True,
        default='[Auto]',
        index=True
    )

    @api.one
    @api.constrains('ref')
    def _check_ref(self):
        if self.ref:
            ref_partners = self.search(
                [
                    ('ref', '=', self.ref)
                ]
            )
            if len(ref_partners) >= 1:
                if not self in ref_partners or len(ref_partners) > 1:
                    raise ValidationError(_('Error !'),
                                          _('Partner Reference is already used for other product'))
    
    @api.model
    def create(self, vals):
        # Check if sequence exists for specific country, and get a new number
        if vals.get('ref', '[Auto]') == '[Auto]':
            if 'country_id' in vals:
                partner_sequence = self.env['res.partner.sequence'].search(
                    [
                        ('country_id', '=', vals['country_id'])
                    ]
                )
                if partner_sequence and partner_sequence.sequence_id:
                    while True:
                        vals['ref'] = partner_sequence.sequence_id.next_by_id()
                        if self.search([('ref', '=', vals['ref'])]):
                            _logger.debug("partner get next by code res.partner"
                                          " code already exists in database")
                        else:
                            break

        # If no number was found with the specific country approach the
        # default sequence will be used
        if vals.get('ref', '[Auto]') == '[Auto]':
            while True:
                vals['ref'] = self.env['ir.sequence'].next_by_code(
                    'res.partner'
                )
                if self.search([('ref', '=', vals['ref'])]):
                    _logger.debug("partner get next by code res.partner code "
                                  "already exists in database")
                else:
                    break

        # If no sequence was found
        if vals.get('ref', '[Auto]') == '[Auto]':
            raise ValidationError(
                _('Error !'),
                _('No partner sequence is defined'))

        return super(ResPartner, self).create(vals)
