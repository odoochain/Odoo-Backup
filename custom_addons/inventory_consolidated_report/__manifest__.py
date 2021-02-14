# -*- coding: utf-8 -*-
# Copyright 2020 Shamsul Arifin, Crystal Technology Bangladesh Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "ICR",
    "version": "1.0.0.1",
    "author": "Shamsul Arifin",
    "category": "Reporting",
    'summary': 'Inventory Consolidated Report.'
               'User can view consolidated report of inventory',
    'company': 'Crystal Technology Bangladesh Ltd.',
    'website': 'www.ctechbd.com',
    "description": """User can view consolidated report of inventory""",
    "depends": ["product", "stock"],
    "data": ["wizard/icr_report_stock_wizard.xml"],

    "installable": True,
    "application": True,
    "auto_install": False,
}
