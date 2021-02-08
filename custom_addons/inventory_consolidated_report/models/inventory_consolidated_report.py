from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_round
from odoo.tools.translate import _
from odoo.exceptions import UserError


class InventoryConsolidatedReport(models.Model):
    _name = 'inventory.consolidated'
    _description = 'Inventory Consolidated Report'


