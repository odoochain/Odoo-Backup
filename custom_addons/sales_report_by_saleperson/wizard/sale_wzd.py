# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from odoo import api, fields, models
from datetime import datetime

class SaleSalespersonReport(models.TransientModel):
    _name = 'sale.salesperson.report'

    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)
    user_ids = fields.Many2many('res.users', string="Sales Person")

    @api.multi
    def print_salesperson_vise_report(self):
        #start_dates = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        #(self.start_date, '%Y-%m-%d %H:%M:%S')
        sale_orders = self.env['sale.order'].search([('state', '=', 'sale')])
        groupby_dict = {}
        if self.end_date == datetime.now().strftime('%Y-%m-%d'):
            self.end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print '====================end date================='
            print self.end_date
            for users in self.user_ids:
                filtered_order = list(filter(lambda x: x.user_id == users, sale_orders))
                filtered_by_date = list(filter(lambda x: x.date_order >= self.start_date and x.date_order <= self.end_date, filtered_order))
                groupby_dict[users.name] = filtered_by_date
            print 
            final_dict = {}
        else:
            for users in self.user_ids:
                filtered_order = list(filter(lambda x: x.user_id == users, sale_orders))
                filtered_by_date = list(filter(lambda x: x.date_order >= self.start_date and x.date_order <= self.end_date, filtered_order))
                groupby_dict[users.name] = filtered_by_date
            print 
            final_dict = {}
        
        for userline in groupby_dict.keys():
            temp = []
            for order in groupby_dict[userline]:
                temp_2 = []
                temp_2.append(order.name)
                temp_2.append(order.date_order)
                temp_2.append(order.amount_total)
                temp.append(temp_2)
            final_dict[userline] = temp
        datas = {
            'ids': self.ids,
            'model': 'sale.salesperson.report',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,

        }
        return self.env['report'].get_action(self,'sales_report_by_saleperson.saleperson_report', data=datas)
