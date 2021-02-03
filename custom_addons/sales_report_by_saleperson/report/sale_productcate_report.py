# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
from odoo import api, models
from datetime import datetime

class SaleProductcateReport(models.AbstractModel):
    _name = 'report.sales_report_by_saleperson.sale_productcate_report'
    
    
    def get_default_user(self):
        user_pool = self.env['res.users']
        user = user_pool.browse(self.env.user.id)
        if user:
            return user.id 
            print "user.id"
        else:
            return False
    
    def prepare_productcate_line_by_date(self, start_date, end_date, categ_id):
        if end_date == datetime.now().strftime('%Y-%m-%d'):
            end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    
            if categ_id:
                sql_query = """ SELECT c.name as category_name, s.name as product_name, s.qty_Invoiced as quantity, s.price_subtotal as total, s.create_date as date, s.invoice_status
                            FROM sale_order_line s left join product_template p on p.id = s.product_id left join product_category c on  c.id = p.categ_id
                            where invoice_status = 'invoiced' and c.name = %s and s.create_date BETWEEN %s AND %s
                            ORDER BY category_name ASC """
                print start_date, end_date
                params = (categ_id.name, start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
            else:
                sql_query = """ SELECT c.name as category_name, s.name as product_name, s.qty_Invoiced as quantity, s.price_subtotal as total, s.create_date as date, s.invoice_status
                                FROM sale_order_line s left join product_template p on p.id = s.product_id left join product_category c on  c.id = p.categ_id
                                where invoice_status = 'invoiced' and s.create_date BETWEEN %s AND %s
                                ORDER BY category_name ASC """ 
                print start_date, end_date
                params = (start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
        else:
            if categ_id:
                sql_query = """ SELECT c.name as category_name, s.name as product_name, s.qty_Invoiced as quantity, s.price_subtotal as total, s.create_date as date, s.invoice_status
                            FROM sale_order_line s left join product_template p on p.id = s.product_id left join product_category c on  c.id = p.categ_id
                            where invoice_status = 'invoiced' and c.name = %s and s.create_date BETWEEN %s AND %s
                            ORDER BY category_name ASC """
                print start_date, end_date
                params = (categ_id.name, start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
            else:
                sql_query = """ SELECT c.name as category_name, s.name as product_name, s.qty_Invoiced as quantity, s.price_subtotal as total, s.create_date as date, s.invoice_status
                                FROM sale_order_line s left join product_template p on p.id = s.product_id left join product_category c on  c.id = p.categ_id
                                where invoice_status = 'invoiced' and s.create_date BETWEEN %s AND %s
                                ORDER BY category_name ASC """ 
                print start_date, end_date
                params = (start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
                   
    @api.multi
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('sales_report_by_saleperson.sale_productcate_report')
        
        lines = self.prepare_productcate_line_by_date(docs.start_date, docs.end_date, docs.categ_id)
        user = self.get_default_user()
        print "========================--lines--==================================="
        print lines
        docargs = {
            'doc_ids'               : self._ids,
            'doc_model'             : report.model,
            'docs'                  : self,
            'from_date'             : docs.start_date,
            'to_date'               : docs.end_date,
            'categ'                 : docs.categ_id.name,
            'user'                  : user,
            'lines'                 : lines,
        }
        return report_obj.render('sales_report_by_saleperson.sale_productcate_report', docargs)
    
    
    
    