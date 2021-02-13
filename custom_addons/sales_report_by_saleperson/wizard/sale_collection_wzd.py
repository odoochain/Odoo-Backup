# -*- coding: utf-8 -*-
##############################################################################

##############################################################################

from odoo import api, fields, models


class SaleCollection(models.TransientModel):
    _name = 'sale.collection'

    start_date = fields.Date('Start Date', default=fields.Date.today(), required=True)
    end_date = fields.Date(string="End Date", default=fields.Date.today(), required=True)
    user_ids = fields.Many2many('res.users', string="Sales Person")

    @api.multi
    def print_sale_collection_report(self):
        sale_collection = self.env['account.payment'].search([('state', '=', 'posted')])
        groupby_dict = {}
        for user in self.user_ids:
            filtered_order = list(filter(lambda x: x.create_uid == user, sale_collection))
            filtered_by_date = list(
                filter(lambda x: x.payment_date >= self.start_date and x.payment_date <= self.end_date, filtered_order))
            groupby_dict[user.name] = filtered_by_date

        final_dict = {}
        for user in groupby_dict.keys():
            temp = []
            for order in groupby_dict[user]:
                temp_2 = []
                temp_2.append(order.name)
                temp_2.append(order.payment_date)
                temp_2.append(order.payment_type)
                if order.payment_type == 'outbound':
                    order.amounts = -1 * order.amount
                    temp_2.append(order.amounts)
                else:
                    order.amounts = 1 * order.amount
                    temp_2.append(order.amounts)
                temp.append(temp_2)
            final_dict[user] = temp
        datas = {
            'ids': self.ids,
            'model': 'sale.collection',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,

        }
        return self.env['report'].get_action(self,'sales_report_by_saleperson.sale_collection_report', data=datas)
