import xlsxwriter
import base64
from odoo import fields, models, api
from cStringIO import StringIO
from datetime import datetime
from pytz import timezone
import pytz


class IcrReportStock(models.TransientModel):
    _name = "icr.report.stock"
    _description = "Inventory Consolidated Report .xlsx"

    test = fields.Char('test', readonly=True)
