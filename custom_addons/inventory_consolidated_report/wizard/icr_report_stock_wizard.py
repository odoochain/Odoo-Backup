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

        columns = [
            ('No', 5, 'no', 'no'),
            ('Product', 30, 'char', 'char'),
            ('Product Category', 20, 'char', 'char'),
            ('Location', 30, 'char', 'char'),
            ('Incoming Date', 20, 'char', 'char'),
            ('Stock Age', 20, 'number', 'number'),
            ('Total Stock', 20, 'float', 'float'),
            ('Available', 20, 'float', 'float'),
            ('Reserved', 20, 'float', 'float'),
        ]

        datetime_format = '%Y-%m-%d %H:%M:%S'
        utc = datetime.now().strftime(datetime_format)
        utc = datetime.strptime(utc, datetime_format)
        tz = self.get_default_date_model().strftime(datetime_format)
        tz = datetime.strptime(tz, datetime_format)
        duration = tz -utc
        hours = duration.seconds / 60 / 60
        if hours > 1 or hours < 1 :
            hours = str(hours) + ' hours'
        else:
            hours = str(hours) + ' hour'

        query = """
            SELECT 
                prod_tmpl.name as product, 
                categ.name as prod_categ, 
                loc.complete_name as location,
                quant.in_date + interval '%s' as date_in, 
                date_part('days', now() - (quant.in_date + interval '%s')) as aging,
                sum(quant.qty) as total_product, 
                sum(quant2.qty) as stock, 
                sum(quant3.qty) as reserved
            FROM 
                stock_quant quant
            LEFT JOIN 
                (select * from stock_quant where %s and %s
                and reservation_id is null) quant2 on quant2.id = quant.id
            LEFT JOIN 
                (select * from stock_quant where %s and %s
                and reservation_id is not null)quant3 on quant3.id = quant.id
            LEFT JOIN 
                stock_location loc on loc.id=quant.location_id
            LEFT JOIN 
                product_product prod on prod.id=quant.product_id
            LEFT JOIN 
                product_template prod_tmpl on prod_tmpl.id=prod.product_tmpl_id
            LEFT JOIN 
                product_category categ on categ.id=prod_tmpl.categ_id
            WHERE 
                %s and %s
            GROUP BY 
                product, prod_categ, location, date_in
            ORDER BY 
                date_in
        """