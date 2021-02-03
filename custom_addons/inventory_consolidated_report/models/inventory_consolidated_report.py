from odoo import models, fields


class InventoryConsolidatedRreport(models.Model):
    _name = 'inventory.consolidated'
    _description = 'Inventory Consolidated Report'

    location_id = fields.Many2one('stock.location', 'Location', required=True)
    name = fields.Char('Name', related='location_id.name')
    product_id = fields.Many2one('product.product', 'Product')
    product_uom_id = fields.Many2one(
        'product.uom', string='Unit of Measure', related='product_id.uom_id',
        readonly=True)
    package_id = fields.Many2one(
        'stock.quant.package', string='Package',
        index=True, readonly=True,
        help="The package containing this quant")
    qty = fields.Float(
        'Quantity',
        index=True, readonly=True, required=True,
        help="Quantity of products in this quant, in the default unit of measure of the product")
    # product_qty = fields.Float('Quantity', related='product.product_qty')
