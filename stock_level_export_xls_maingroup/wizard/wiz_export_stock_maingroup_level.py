# -*- coding: utf-8 -*-
# Copyright 2009-2017 Noviat.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError


class WizExportStockMaingroupLevel(models.TransientModel):
    _name = 'wiz.export.stock.maingroup.level'
    _description = 'Generate a stock level report for a given date'

    stock_level_date = fields.Datetime(
        string='Stock Level Date',
        help="Specify the Date & Time for the Stock Levels."
             "\nThe current stock level will be given if not specified.")
    categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
        domain=[('parent_id', '=', False)],
        help="Limit the export to the selected Top Level Product Category.")
    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        help="Limit the export to the selected Warehouse.")
    category_select = fields.Selection([
        ('all', 'All Categories'),
        ('select', 'Selected Categories'),
        ], string='Categories',
        default=lambda self: self._default_category_select())
    # import_compatible = fields.Boolean(
    #     string='Import Compatible Export',
    #     help="Generate a file for use with the 'stock_level_import' module.")
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env['res.company']._company_default_get(
            'stock.inventory'))

    def _default_category_select(self):
        if self._context.get('active_model') == 'product.category':
            return 'select'
        else:
            return 'all'

    def _xls_export_domain(self):
        ctx = self._context
        domain = [
            ('parent_id', '=', False),
        ]
        if self.categ_id:
            domain.append(('main_category', '=', self.categ_id.id))
        if self.category_select == 'select':
            if ctx.get('active_model') == 'product.category':
                domain.append(('id', 'in', ctx.get('active_ids')))
        return domain

    def _update_datas(self, datas):
        """
        Update datas when adding extra options to the wizard
        in inherited modules.
        """
        pass

    @api.multi
    def xls_export(self):
        self.ensure_one()
        warehouses = self.warehouse_id
        if not warehouses:
            warehouses = self.env['stock.warehouse'].search(
                [('company_id', '=', self.company_id.id)])
        warehouse_ids = warehouses._ids
        domain = self._xls_export_domain()
        categories = self.env['product.category'].search(domain)

        if not categories:
            raise UserError(
                _("No Data Available."),
                _("'\nNo records found for your selection !"))


        datas = {
            'model': self._name,
            'stock_level_date':self.stock_level_date,
            'category_ids': categories._ids,
            'category_id': self.categ_id.id,
            'warehouse_ids': warehouse_ids,
            'category_select': self.category_select,
            'company_id': self.company_id.id,
        }
        self._update_datas(datas)
        return {'type': 'ir.actions.report.xml',
                'report_name': 'stock.maingroup.level.xls',
                'datas': datas}
