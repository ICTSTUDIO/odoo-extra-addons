# -*- coding: utf-8 -*-
# Copyright© 2017 ICTSTUDIO <http://www.ictstudio.eu>
# License: AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO
import base64
import csv
import time
from sys import exc_info
from traceback import format_exception

from openerp import api, fields, models, _
from openerp.exceptions import Warning as UserError

import logging
_logger = logging.getLogger(__name__)


class ProductPurchasepriceImport(models.TransientModel):
    _name = 'product.purchaseprice.import'
    _description = 'Product Purchaseprice Import'

    supplier = fields.Many2one(
        comodel_name='res.partner',
        string="Supplier",
        domain = [('supplier','=',True)], 
        ondelete='cascade'
    )
    product_purchaseprice_data = fields.Binary(string='File', required=True)
    product_purchaseprice_fname = fields.Char(string='Filename')
    lines = fields.Binary(
        compute='_compute_lines', string='Input Lines', required=True)
    dialect = fields.Binary(
        compute='_compute_dialect', string='Dialect', required=True)
    csv_separator = fields.Selection(
        [(',', ', (comma)'), (';', '; (semicolon)')],
        string='CSV Separator', required=True)
    decimal_separator = fields.Selection(
        [('.', '. (dot)'), (',', ', (comma)')],
        string='Decimal Separator',
        default='.', required=True)
    codepage = fields.Char(
        string='Code Page',
        default=lambda self: self._default_codepage(),
        help="Code Page of the system that has generated the csv file."
             "\nE.g. Windows-1252, utf-8")
    note = fields.Text('Log')

    @api.model
    def _default_codepage(self):
        return 'Windows-1252'

    @api.one
    @api.depends('product_purchaseprice_data')
    def _compute_lines(self):
        if self.product_purchaseprice_data:
            lines = base64.decodestring(self.product_purchaseprice_data)
            # convert windows & mac line endings to unix style
            self.lines = lines.replace('\r\n', '\n').replace('\r', '\n')

    @api.one
    @api.depends('lines', 'csv_separator')
    def _compute_dialect(self):
        if self.lines:
            try:
                self.dialect = csv.Sniffer().sniff(
                    self.lines[:128], delimiters=';,')
            except:
                # csv.Sniffer is not always reliable
                # in the detection of the delimiter
                self.dialect = csv.Sniffer().sniff(
                    '"header 1";"header 2";\r\n')
                if ',' in self.lines[128]:
                    self.dialect.delimiter = ','
                elif ';' in self.lines[128]:
                    self.dialect.delimiter = ';'
        if self.csv_separator:
            self.dialect.delimiter = str(self.csv_separator)

    @api.onchange('product_purchaseprice_data')
    def _onchange_stock_level_data(self):
        if self.lines:
            self.csv_separator = self.dialect.delimiter
            if self.csv_separator == ';':
                self.decimal_separator = ','

    @api.onchange('csv_separator')
    def _onchange_csv_separator(self):
        if self.csv_separator and self.product_purchaseprice_data:
            self.dialect.delimiter = self.csv_separator

    def _remove_leading_lines(self, lines):
        """ remove leading blank or comment lines """
        input = StringIO.StringIO(lines)
        header = False
        while not header:
            ln = input.next()
            if not ln or ln and ln[0] in [self.csv_separator, '#']:
                continue
            else:
                ln_lower = ln.lower()
                ln_set = set(ln_lower.split(self.csv_separator))
                header = ln_lower
        if not header:
            raise UserError(
                _("No header line found in the input file !"))
        output = input.read()
        return output, header

    def _process_header(self, header_fields):
        self._skip_fields = []

        # header fields after blank column are considered as comments
        column_cnt = 0
        for cnt in range(len(header_fields)):
            if header_fields[cnt] == '':
                column_cnt = cnt
                break
            elif cnt == len(header_fields) - 1:
                column_cnt = cnt + 1
                break
        header_fields = header_fields[:column_cnt]

        return header_fields


    @api.multi
    def product_purchaseprice_import(self):
        time_start = time.time()
        self._err_log = ''
        lines, header = self._remove_leading_lines(self.lines)
        header_fields = csv.reader(
            StringIO.StringIO(header), dialect=self.dialect).next()
        self._header_fields = self._process_header(header_fields)
        reader = csv.DictReader(
            StringIO.StringIO(lines), fieldnames=self._header_fields,
            dialect=self.dialect)

        lines = []
        for line in reader:
            # step 1: handle codepage
            for i, hf in enumerate(self._header_fields):
                try:
                    line[hf] = line[hf].decode(self.codepage).strip()
                except:
                    tb = ''.join(format_exception(*exc_info()))
                    raise UserError(
                        _("Wrong Code Page"),
                        _("Error while processing line '%s' :\n%s")
                        % (line, tb))

            header_reversed = reversed(self._header_fields)
            for i, hf in enumerate(header_reversed):
                if i == 0 and line[hf] and line[hf][0] == '#':
                    # lines starting with # are considered as comment lines
                    break
                if line[hf] == '':
                    break

            if line.get('productcode') and line.get('inkoopprijs') and self.supplier:
                supplierinfo = self.env['product.supplierinfo'].search(
                        [
                            ('name', '=', self.supplier.id),
                            ('product_tmpl_id.default_code', '=', line.get('productcode'))
                        ]
                )
                _logger.debug('Supplierinfo: %s', supplierinfo)
                if supplierinfo and len(supplierinfo) == 1:
                    _logger.debug('Write Supplierinfo')
                    supplierinfo.write({'supplier_price': str2float(line.get('inkoopprijs'),self.decimal_separator)})

        return {'type': 'ir.actions.act_window_close'}


def str2float(amount, decimal_separator):
    if not amount:
        return 0.0
    try:
        if decimal_separator == '.':
            return float(amount.replace(',', ''))
        else:
            return float(amount.replace('.', '').replace(',', '.'))
    except:
        return False


def str2int(amount, decimal_separator):
    if not amount:
        return 0
    try:
        if decimal_separator == '.':
            return int(amount.replace(',', ''))
        else:
            return int(amount.replace('.', '').replace(',', '.'))
    except:
        return False
