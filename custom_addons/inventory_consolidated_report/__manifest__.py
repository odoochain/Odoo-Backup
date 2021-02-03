# -*- coding: utf-8 -*-
# Copyright 2020 Shafiqul Dhaka, Crystal Technology Bangladesh Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Inventory Consolidated Report",
    "version": "1.0.0.0",
    "author": "Shamsul Arifin",
    "category": "Stock",
    'summary': 'Allow to add advance payments on sales',
    'company': 'Crystal Technology Bangladesh Ltd.',
    'website': 'www.ctechbd.com',
    "description": """Allow to add advance payments on sales and then use its
 on invoices""",
    "depends": ["base", "sale", "account"],
    "data": ["views/menu.xml"],

    "installable": True,
    "application": True,
    "auto_install": False,
}
