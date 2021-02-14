import xlsxwriter
import base64
from odoo import fields, models, api
from cStringIO import StringIO
from datetime import datetime
from pytz import timezone
import pytz


class IcrReportStock(models.TransientModel):
    _name = "icr.report.stock"
    _description = "Inventory Consolidated Report .xlsx"

    @api.model
    def get_default_date_model(self):
        return pytz.UTC.localize(datetime.now()).astimezone(timezone(self.env.user.tz or 'UTC'))

    datas = fields.Binary('File', readonly=True)
    datas_fname = fields.Char('Filename', readonnly=True)
    product_ids = fields.Many2many('product.product', 'icr_report_stock_product_rel', 'icr_report_stock_id',
                                   'product_id', 'Product')
    categ_ids = fields.Many2many('product.category', 'icr_report_stock_categ_rel', 'icr_report_stock_id',
                                 'categ_id', 'Categories')
    location_ids = fields.Many2many('stock.location', 'icr_report_stock_location_rel', 'icr_report_stock_id',
                                    'location_id', 'Locations')

    def print_icr_report(self):
        data = self.read[0]
        product_ids = data['product_ids']
        categ_ids = data['categ_ids']
        location_ids = data['location_ids']

        if categ_ids:
            product_ids = self.env['product.product'].search([('categ_id', 'in', categ_ids)])
            product_ids = [prod.id for prod in product_ids]
        where_product_ids = " 1=1 "
        where_product_ids2 = " 1=1 "
        if product_ids:
            where_product_ids = " quant.product_id in %s"%str(tuple(product_ids)).replace(',)', ')')
            where_product_ids2 = " product_id in %s"%str(tuple(product_ids)).replace(',)', ')')
        location_ids2 = self.env['stock.location'].search([('usage', '=', 'internal')])
        ids_location = [loc.id for loc in location_ids2]
        where_location_ids = " quant.location_id in %s"%str(tuple(ids_location)).replace(',)', ')')
        where_location_ids2 = " location_id in %s"%str(tuple(ids_location)).replace(',)', ')')
        if location_ids:
            where_location_ids = " quant.location_id in %s"%str(tuple(location_ids)).replace(',)', ')')
            where_location_ids2 = " location_id in %s"%str(tuple(location_ids)).replace(',)', ')')

        datetime_string = self.get_default_date_model().strftime("%Y-%m-%d %H:%M:%S")
        date_string = self.get_default_date_model().strftime("%Y-%m-%d")
        report_name = 'Inventory Consolidated Report'
        filename = '%s %s.xlsx'%(report_name,date_string)