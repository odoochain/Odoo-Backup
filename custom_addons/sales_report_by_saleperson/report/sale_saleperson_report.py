# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
from odoo import api, models
from datetime import datetime
from datetime import timedelta

class SaleSalepersonReport(models.AbstractModel):
    _name = 'report.sales_report_by_saleperson.sale_saleperson_report'
    
    
    def get_default_user(self):
        user_pool = self.env['res.users']
        user = user_pool.browse(self.env.user.id)
        if user:
            return user.id 
            print "user.id"
        else:
            return False
    
    def prepare_salepersonwise_line_by_date(self, start_date, end_date):
        if end_date == datetime.now().strftime('%Y-%m-%d'):
            end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql_query = """ SELECT p.login as user_name, r.name as full_name, Count(s.user_id) as patient, sum(s.amount_total) as total
                        FROM sale_order s left join res_users p on p.id = s.user_id left join res_partner r on  r.id = p.partner_id
                        WHERE state= 'sale' AND date_order BETWEEN %s AND %s
                        GROUP BY p.login, r.name """
            print "========================--date-if-==================================="
            print start_date, end_date
            params = (start_date, end_date)
            self.env.cr.execute(sql_query, params)
            res = self.env.cr.dictfetchall()
            print res
            return res
        elif start_date == end_date:
            #date_1 = datetime.datetime.strptime(self.end_date, "%Y-%m-%d")
            #endd_date = date_1 + datetime.timedelta(days=1)
            sql_query = """ SELECT p.login as user_name, r.name as full_name, Count(s.user_id) as patient, sum(s.amount_total) as total
                        FROM sale_order s left join res_users p on p.id = s.user_id left join res_partner r on  r.id = p.partner_id
                        WHERE state= 'sale' AND Date_trunc('day', date_order) BETWEEN %s AND %s
                        GROUP BY p.login, r.name """
            print "========================--date-ifif-==================================="
            print start_date, end_date
            params = (start_date, end_date)
            self.env.cr.execute(sql_query, params)
            res = self.env.cr.dictfetchall()
            print res
            return res
        else: 
            #end_dt = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            
            sql_query = """ SELECT p.login as user_name, r.name as full_name, Count(s.user_id) as patient, sum(s.amount_total) as total
                            FROM sale_order s left join res_users p on p.id = s.user_id left join res_partner r on  r.id = p.partner_id
                            WHERE state= 'sale' AND date_order BETWEEN %s AND %s
                            GROUP BY p.login, r.name """
            print "========================--date-else-==================================="
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
        report = report_obj._get_report_from_name('sales_report_by_saleperson.sale_saleperson_report')
        
        lines = self.prepare_salepersonwise_line_by_date(docs.start_date, docs.end_date)
        user = self.get_default_user()
        print "========================--lines--==================================="
        print lines
        docargs = {
            'doc_ids'               : self._ids,
            'doc_model'             : report.model,
            'docs'                  : self,
            'from_date'             : docs.start_date,
            'to_date'               : docs.end_date,
            'user'                  : user,
            'lines'                 : lines,
        }
        return report_obj.render('sales_report_by_saleperson.sale_saleperson_report', docargs)
    
    
    
    