# -*- coding: utf-8 -*-
# Copyright© 2016-2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

import logging

from openerp import models, fields, api

_logger = logging.getLogger(__name__)


class NeedSyncLine(models.Model):
    _name = "need.sync.line"
    _description = "Need Sync Line Based"

    name = fields.Char(
            string="Sync",
            compute="_get_name"
    )
    need_sync = fields.Many2one(
            comodel_name="need.sync",
            string="Need Sync",
            index=True,
            ondelete="cascade"
    )
    need_sync_connection = fields.Many2one(
            comodel_name="need.sync.connection",
            string="Connection",
            index=True
    )
    need_sync_date = fields.Datetime(
            related="need_sync.need_sync_date"
    )
    model = fields.Selection(
            related="need_sync.model",
            store=True,
            index=True
    )
    res_id = fields.Integer(
            related="need_sync.res_id",
            store=True,
            index=True
    )
    record = fields.Reference(
            related="need_sync.record",
            store=True,
            index=True
    )
    sync_needed = fields.Boolean(
            string="Sync Needed",
            compute="_compute_need_sync",
            store=True,
            index=True,
            help="Synchronization Required"
    )
    last_sync_date = fields.Datetime(
            string="Last Sync Datetime"
    )
    confirmed_date = fields.Datetime(
            string="Last Confirm Datetime"
    )
    published = fields.Boolean(
        string="Published",
        default=True,
        index=True
    )

    _sql_constraints = {
        ('connection_need_sync_uniq', 'unique(need_sync, need_sync_connection)', 'Only one need sync per connection')
    }

    @api.one
    @api.depends('need_sync.res_id',
                 'need_sync.model',
                 'need_sync_connection.name'
                 )
    def _get_name(self):
        object = self.env[self.need_sync.model].browse(self.need_sync.res_id)
        if object and 'name' in object._fields:
            object_name = object.name
        else:
            object_name = "No object name defined"
        if self.need_sync_connection:
            connection_name = self.need_sync_connection.name
        else:
            connection_name = 'No Connection Name'
        self.name = '%s (%s)' % (object_name, connection_name)

    @api.one
    @api.depends('need_sync.need_sync_date',
                 'last_sync_date',
                 'confirmed_date',
                 'published'
                 )
    def _compute_need_sync(self):
        if self.published == True:
            if self.need_sync_date > self.last_sync_date:
                self.sync_needed = True
            elif self.need_sync_date and not self.last_sync_date:
                self.sync_needed = True
            elif self.sync_needed == True:
                self.sync_needed = False
        else:
            self.sync_needed = False

    @api.multi
    def _create_need_sync(self, need_sync, need_sync_connection):
        if need_sync and need_sync_connection:
            self.create(
                    {
                        'need_sync': need_sync.id,
                        'need_sync_connection': need_sync_connection.id
                    }
            )

    @api.multi
    def map_need_sync(self, model, res_ids, need_sync_connection):

        if isinstance(res_ids, (long, int)):
            res_ids = [res_ids]

        need_sync_lines = self.search(
                [
                    ('model', '=', model),
                    ('res_id', 'in', res_ids),
                    ('need_sync_connection', '=', need_sync_connection.id)
                ]
        )

        need_sync_line_res_ids = [x.res_id for x in need_sync_lines]
        create_sync_line_ids = list(set(res_ids) - set(need_sync_line_res_ids))
        if create_sync_line_ids:
            for res_id in create_sync_line_ids:
                need_sync = self.env['need.sync'].search(
                        [
                            ('model', '=', model),
                            ('res_id', '=', res_id),
                        ]
                )
                self._create_need_sync(need_sync, need_sync_connection)
        return True

    @api.multi
    def _check_error_line(self):
        self.ensure_one()
        ctx = dict(self._context, active_test=False)
        check_record = self.env[self.model].with_context(ctx).search([('id', '=', self.res_id)])
        if not check_record:
            # If record no longer exists remove needsync
            self.need_sync.unlink()

    @api.multi
    def check_error_lines(self):
        for rec in self:
            rec._check_error_line()


