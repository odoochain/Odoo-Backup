# -*- coding: utf-8 -*-
##############################################################################

##############################################################################
from odoo import api, models


class ReportSalesSalespersonWise(models.AbstractModel):
    _name = 'report.sales_report_by_saleperson.sale_collection_report'

    @api.model
    def render_html(self, docids, data=None):
        docargs =  {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }
        docargs
        return self.env['report'].render('sales_report_by_saleperson.sale_collection_report', docargs)
