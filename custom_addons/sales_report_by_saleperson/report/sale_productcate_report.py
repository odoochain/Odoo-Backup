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
                sql_query = """ SELECT c.name as category_name, p.name as product_name, round(s.qty_invoiced,2) as quantity, round(s.price_total,2) as total, s.date as date
                                FROM sale_report s inner join product_template p on s.product_tmpl_id = p.id inner join product_category c on s.categ_id = c.id
                                where s.qty_invoiced > '0' and c.name = %s and s.date BETWEEN %s AND %s
                                ORDER BY category_name ASC """
                print start_date, end_date
                params = (categ_id.name, start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
            else:
                sql_query = """ SELECT c.name as category_name, p.name as product_name, round(s.qty_invoiced,2) as quantity, round(s.price_total,2) as total, s.date as date
                                FROM sale_report s inner join product_template p on s.product_tmpl_id = p.id inner join product_category c on s.categ_id = c.id
                                where s.qty_invoiced > '0' and s.date BETWEEN %s AND %s
                                ORDER BY category_name ASC """ 
                print start_date, end_date
                params = (start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
        elif start_date == end_date:
            if categ_id:
                sql_query = """ SELECT c.name as category_name, p.name as product_name, round(s.qty_invoiced,2) as quantity, round(s.price_total,2) as total, s.date as date
                                FROM sale_report s inner join product_template p on s.product_tmpl_id = p.id inner join product_category c on s.categ_id = c.id
                                where s.qty_invoiced > '0' and c.name = %s and Date_trunc('day', s.date) BETWEEN %s AND %s
                                ORDER BY category_name ASC """
                print start_date, end_date
                params = (categ_id.name, start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
            else:
                sql_query = """ SELECT c.name as category_name, p.name as product_name, round(s.qty_invoiced,2) as quantity, round(s.price_total,2) as total, s.date as date
                                FROM sale_report s inner join product_template p on s.product_tmpl_id = p.id inner join product_category c on s.categ_id = c.id
                                where s.qty_invoiced > '0' and Date_trunc('day', s.date) BETWEEN %s AND %s
                                ORDER BY category_name ASC """ 
                print start_date, end_date
                params = (start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
        else:
            if categ_id:
                sql_query = """ SELECT c.name as category_name, p.name as product_name, round(s.qty_invoiced,2) as quantity, round(s.price_total,2) as total, s.date as date
                                FROM sale_report s inner join product_template p on s.product_tmpl_id = p.id inner join product_category c on s.categ_id = c.id
                                where s.qty_invoiced > '0' and c.name = %s and s.date BETWEEN %s AND %s
                                ORDER BY category_name ASC """
                print start_date, end_date
                params = (categ_id.name, start_date, end_date)
                self.env.cr.execute(sql_query, params)
                res = self.env.cr.dictfetchall()
                print res
                return res
            else:
                sql_query = """ SELECT c.name as category_name, p.name as product_name, round(s.qty_invoiced,2) as quantity, round(s.price_total,2) as total, s.date as date
                                FROM sale_report s inner join product_template p on s.product_tmpl_id = p.id inner join product_category c on s.categ_id = c.id
                                where s.qty_invoiced > '0' and s.date BETWEEN %s AND %s
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
    
    
    
    