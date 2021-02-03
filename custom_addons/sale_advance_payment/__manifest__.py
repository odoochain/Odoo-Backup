# -*- coding: utf-8 -*-
# Copyright 2020 Shafiqul Dhaka, Crystal Technology Bangladesh Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Advance Sale",
    "version": "1.0.0.0",
    "author": "Shafiqul Islam",
    "category": "Sales",
    'summary': 'Allow to add advance payments on sales',
    'company': 'Crystal Technology Bangladesh Ltd.',
    'website': 'www.ctechbd.com',
    "description": """Allow to add advance payments on sales and then use its
 on invoices""",
    "depends": ["base", "sale", "account"],
    "data": ["wizard/sale_advance_payment_wzd_view.xml",
             "views/sale_view.xml",
             "security/ir.model.access.csv"],
    
    "installable": True,
    "images": ['static/description/icon.png'],
    "application": True,
    "auto_install": False,
}
