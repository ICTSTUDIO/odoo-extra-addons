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

class StockMoveLocation(models.Model):
    _name = "stock_move_location"
    _description = "Location Moves"
    _auto = False

    id = fields.Char(
            string='id',
            size=16,
            readonly=True
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
    qty_processing = fields.Float(
            string='Quantity Processing',
            digits=(16,2),
            readonly=True
    )
    qty_in_transit = fields.Float(
            string='Quantity Transit',
            digits=(16,2),
            readonly=True
    )
    qty_in_transit_processing = fields.Float(
            string='Quantity Transit Processing',
            digits=(16,2),
            readonly=True
    )
    qty_backorder = fields.Float(
            string='Quantity Backorder',
            digits=(16,2),
            readonly=True
    )


    def _select(self):
        select_str = """select min(id) as id ,location_id,product_id,
       sum(qty_on_hand) as qty_on_hand,
       sum(qty_processing) as qty_processing,
       sum(qty_in_transit) as qty_in_transit,
       sum(qty_in_transit_processing) as qty_in_transit_processing,
       sum(qty_backorder) as qty_backorder,
       company_id"""
        return select_str

    def _from(self):
        from_str = """stock_move_location"""
        return from_str


    def _group_by(self):
        groupby_str = """group by location_id,product_id,company_id"""
        return groupby_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute(
                """CREATE or REPLACE VIEW %s as (
                %s
                FROM ( %s )
                %s
                )""" % (self._table,
                        self._select(),
                        self._from(),
                        self._group_by()
                        )
        )
