# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from odoo import api, fields, models
from email import _name


class SaleSaleperson(models.TransientModel):
    _name = 'sale.saleperson'
    
    
    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)
    
    
    
    @api.multi
    def sale_saleperson_report(self, data):
        
                
        return self.env['report'].get_action(self, 'sales_report_by_saleperson.sale_saleperson_report', data=data)