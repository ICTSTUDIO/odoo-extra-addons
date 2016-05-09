# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
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


import logging

from openerp import models, fields
from openerp import tools

_logger = logging.getLogger(__name__)

class StockProductLocation(models.Model):
    _name = "stock.product.location"
    _description = "Product Location Stock"
    _auto = False
    _order = "location_name"

    id = fields.Char(
            string='id',
            size=16,
            readonly=True
    )
    location_name = fields.Char(
            string='Location',
            readonly=True,
            store=True
    )
    location_id = fields.Many2one(
            comodel_name='stock.location',
            string='Location',
            readonly=True
    )
    product_id = fields.Many2one(
            comodel_name='product.product',
            string='Product',
            readonly=True
    )
    product_tmpl_id = fields.Many2one(
            related='product_id.product_tmpl_id',
            comodel_name='product.template',
            string='Product Template'
    )
    categ_id = fields.Many2one(
            related='product_id.categ_id',
            comodel_name="product.category",
            string='Category',
            readonly=True
    )
    uom_id = fields.Many2one (
            related='product_id.uom_id',
            comodel_name="product.uom",
            string="UoM",
            readonly = True
    )
    date = fields.Datetime(
            string='Date Planned',
            readonly=True
    )
    company_id = fields.Many2one(
            comodel_name='res.company',
            string='Company',
            readonly=True
    )
    qty_on_hand = fields.Float(
            string='Quantity',
            digits=(16,2),
            readonly=True
    )
    qty_internal = fields.Float(
            string='Quantity Internal',
            digits=(16,2),
            readonly=True
    )
    qty_outgoing = fields.Float(
            string='Quantity Outgoing',
            digits=(16,2),
            readonly=True
    )
    qty_incoming = fields.Float(
            string='Quantity Incoming',
            digits=(16,2),
            readonly=True
    )
    qty_manual = fields.Float(
            string='Quantity Manual',
            digits=(16,2),
            readonly=True
    )
    qty_backorder = fields.Float(
            string='Quantity Backorder',
            digits=(16,2),
            readonly=True
    )
    min_qty = fields.Float(
            string='Minimum Quantity',
            digits=(16,2),
            readonly=True
    )
    qty_multiple = fields.Float(
            string='Quantity Multiple',
            digits=(16,2),
            readonly=True
    )

    def _select(self):
        select_str = """select min(sml.id) as id , sml.location_id, sml.product_id,
       sum(sml.qty_on_hand) as qty_on_hand,
       sum(sml.qty_internal) as qty_internal,
       sum(sml.qty_outgoing) as qty_outgoing,
       sum(sml.qty_incoming) as qty_incoming,
       sum(sml.qty_manual) as qty_manual,
       CASE WHEN (sum(sml.qty_on_hand)+sum(sml.qty_outgoing)) < 0 THEN sum(sml.qty_on_hand)+sum(sml.qty_outgoing) ELSE 0 END as qty_backorder,
       sml.company_id,
       CASE WHEN swo.product_min_qty is null THEN 0 ELSE swo.product_min_qty END as min_qty,
       CASE WHEN swo.qty_multiple is null THEN 0 ELSE swo.qty_multiple END as qty_multiple,
       sml.location_name as location_name
       """
        return select_str

    def _from(self):
        from_str = """stock_move_location sml
        left join stock_warehouse_orderpoint swo ON swo.location_id = sml.location_id and swo.product_id = sml.product_id and swo.active = true
        """
        return from_str


    def _group_by(self):
        groupby_str = """group by sml.location_name,sml.location_id,sml.product_id,sml.company_id,swo.product_min_qty,swo.qty_multiple"""
        return groupby_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute(
                """CREATE or REPLACE VIEW %s as (
                %s
                FROM %s
                %s
                )""" % (self._table,
                        self._select(),
                        self._from(),
                        self._group_by()
                        )
        )
