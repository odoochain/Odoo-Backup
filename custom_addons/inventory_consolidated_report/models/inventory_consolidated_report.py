from odoo import api, fields, models
from odoo.tools.float_utils import float_compare, float_round
from odoo.tools.translate import _
from odoo.exceptions import UserError


class InventoryConsolidatedRreport(models.Model):
    _name = 'inventory.consolidated'
    _description = 'Inventory Consolidated Report'

    name = fields.Char(string='Identifier', compute='_compute_name')
    product_id = fields.Many2one(
        'product.product', 'Product',
        index=True, ondelete="restrict", readonly=True, required=True)
    location_id = fields.Many2one(
        'stock.location', 'Location',
        auto_join=True, index=True, ondelete="restrict", readonly=True, required=True)
    qty = fields.Float(
        'Quantity',
        index=True, readonly=True, required=True,
        help="Quantity of products in this quant, in the default unit of measure of the product")
    product_uom_id = fields.Many2one(
        'product.uom', string='Unit of Measure', related='product_id.uom_id',
        readonly=True)
    package_id = fields.Many2one(
        'inventory.quantpackage', string='Package',
        index=True, readonly=True,
        help="The package containing this quant")
    packaging_type_id = fields.Many2one(
        'product.packaging', string='Type of packaging', related='package_id.packaging_id',
        readonly=True, store=True)
    reservation_id = fields.Many2one(
        'stock.move', 'Reserved for Move',
        index=True, readonly=True,
        help="The move the quant is reserved for")
    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot/Serial Number',
        index=True, ondelete="restrict", readonly=True)
    cost = fields.Float('Unit Cost', group_operator='avg')
    owner_id = fields.Many2one(
        'res.partner', 'Owner',
        index=True, readonly=True,
        help="This is the owner of the quant")
    create_date = fields.Datetime('Creation Date', readonly=True)
    in_date = fields.Datetime('Incoming Date', index=True, readonly=True)
    history_ids = fields.Many2many(
        'stock.move', 'stock_quant_move_rel', 'quant_id', 'move_id',
        string='Moves', copy=False,
        help='Moves that operate(d) on this quant')
    company_id = fields.Many2one(
        'res.company', 'Company',
        index=True, readonly=True, required=True,
        default=lambda self: self.env['res.company']._company_default_get('inventory.consolidated'),
        help="The company to which the quants belong")
    inventory_value = fields.Float('Inventory Value', compute='_compute_inventory_value', readonly=True)
    # Used for negative quants to reconcile after compensated by a new positive one
    propagated_from_id = fields.Many2one(
        'inventory.consolidated', 'Linked Quant',
        index=True, readonly=True,
        help='The negative quant this is coming from')
    negative_move_id = fields.Many2one(
        'stock.move', 'Move Negative Quant',
        readonly=True,
        help='If this is a negative quant, this will be the move that caused this negative quant.')
    negative_dest_location_id = fields.Many2one(
        'stock.location', "Negative Destination Location", related='negative_move_id.location_dest_id',
        readonly=True,
        help="Technical field used to record the destination location of a move that created a negative quant")

    @api.one
    def _compute_name(self):
        """ Forms complete name of location from parent location to child location. """
        self.name = '%s: %s%s' % (self.lot_id.name or self.product_id.code or '', self.qty, self.product_id.uom_id.name)

    @api.multi
    def _compute_inventory_value(self):
        for quant in self:
            if quant.company_id != self.env.user.company_id:
                # if the company of the quant is different than the current user company, force the company in the context
                # then re-do a browse to read the property fields for the good company.
                quant = quant.with_context(force_company=quant.company_id.id)
            quant.inventory_value = quant.product_id.standard_price * quant.qty

    # product_qty = fields.Float('Quantity', related='product.product_qty')

    class QuantPackage(models.Model):
        """ Packages containing quants and/or other packages """
        _name = "inventory.quantpackage"
        _description = "Physical Packages"
        _parent_name = "parent_id"
        _parent_store = True
        _parent_order = 'name'
        _order = 'parent_left'

        name = fields.Char(
            'Package Reference', copy=False, index=True,
            default=lambda self: self.env['ir.sequence'].next_by_code('inventory.quantpackage') or _('Unknown Pack'))
        quant_ids = fields.One2many('inventory.consolidated', 'package_id', 'Bulk Content', readonly=True)
        parent_id = fields.Many2one(
            'inventory.quantpackage', 'Parent Package',
            ondelete='restrict', readonly=True,
            help="The package containing this item")
        ancestor_ids = fields.One2many('inventory.quantpackage', string='Ancestors', compute='_compute_ancestor_ids')
        children_quant_ids = fields.One2many('inventory.consolidated', string='All Bulk Content',
                                             compute='_compute_children_quant_ids')
        children_ids = fields.One2many('inventory.quantpackage', 'parent_id', 'Contained Packages', readonly=True)
        parent_left = fields.Integer('Left Parent', index=True)
        parent_right = fields.Integer('Right Parent', index=True)
        packaging_id = fields.Many2one(
            'product.packaging', 'Package Type', index=True,
            help="This field should be completed only if everything inside the package share the same product, otherwise it doesn't really makes sense.")
        location_id = fields.Many2one(
            'stock.location', 'Location', compute='_compute_package_info', search='_search_location',
            index=True, readonly=True)
        company_id = fields.Many2one(
            'res.company', 'Company', compute='_compute_package_info', search='_search_company',
            index=True, readonly=True)
        owner_id = fields.Many2one(
            'res.partner', 'Owner', compute='_compute_package_info', search='_search_owner',
            index=True, readonly=True)

        @api.one
        @api.depends('parent_id', 'children_ids')
        def _compute_ancestor_ids(self):
            self.ancestor_ids = self.env['inventory.quantpackage'].search([('id', 'parent_of', self.id)]).ids

        @api.multi
        @api.depends('parent_id', 'children_ids', 'quant_ids.package_id')
        def _compute_children_quant_ids(self):
            for package in self:
                if package.id:
                    package.children_quant_ids = self.env['inventory.consolidated'].search(
                        [('package_id', 'child_of', package.id)]).ids

        @api.depends('quant_ids.package_id', 'quant_ids.location_id', 'quant_ids.company_id', 'quant_ids.owner_id',
                     'ancestor_ids')
        def _compute_package_info(self):
            for package in self:
                quants = package.children_quant_ids
                if quants:
                    values = quants[0]
                else:
                    values = {'location_id': False, 'company_id': self.env.user.company_id.id, 'owner_id': False}
                package.location_id = values['location_id']
                package.company_id = values['company_id']
                package.owner_id = values['owner_id']

        @api.multi
        def name_get(self):
            return self._compute_complete_name().items()

        def _compute_complete_name(self):
            """ Forms complete name of location from parent location to child location. """
            res = {}
            for package in self:
                current = package
                name = current.name
                while current.parent_id:
                    name = '%s / %s' % (current.parent_id.name, name)
                    current = current.parent_id
                res[package.id] = name
            return res

        def _search_location(self, operator, value):
            if value:
                packs = self.search([('quant_ids.location_id', operator, value)])
            else:
                packs = self.search([('quant_ids', operator, value)])
            if packs:
                return [('id', 'parent_of', packs.ids)]
            else:
                return [('id', '=', False)]

        def _search_company(self, operator, value):
            if value:
                packs = self.search([('quant_ids.company_id', operator, value)])
            else:
                packs = self.search([('quant_ids', operator, value)])
            if packs:
                return [('id', 'parent_of', packs.ids)]
            else:
                return [('id', '=', False)]

        def _search_owner(self, operator, value):
            if value:
                packs = self.search([('quant_ids.owner_id', operator, value)])
            else:
                packs = self.search([('quant_ids', operator, value)])
            if packs:
                return [('id', 'parent_of', packs.ids)]
            else:
                return [('id', '=', False)]

        def _check_location_constraint(self):
            '''checks that all quants in a package are stored in the same location. This function cannot be used
               as a constraint because it needs to be checked on pack operations (they may not call write on the
               package)
            '''
            for pack in self:
                parent = pack
                while parent.parent_id:
                    parent = parent.parent_id
                locations = parent.get_content().filtered(lambda quant: quant.qty > 0.0).mapped('location_id')
                if len(locations) != 1:
                    raise UserError(_('Everything inside a package should be in the same location'))
            return True

        @api.multi
        def action_view_related_picking(self):
            """ Returns an action that display the picking related to this
            package (source or destination).
            """
            self.ensure_one()
            pickings = self.env['stock.picking'].search(['|', ('pack_operation_ids.package_id', '=', self.id),
                                                         ('pack_operation_ids.result_package_id', '=', self.id)])
            action = self.env.ref('stock.action_picking_tree_all').read()[0]
            action['domain'] = [('id', 'in', pickings.ids)]
            return action

        @api.multi
        def unpack(self):
            for package in self:
                # TDE FIXME: why superuser ?
                package.mapped('quant_ids').sudo().write({'package_id': package.parent_id.id})
                package.mapped('children_ids').write({'parent_id': package.parent_id.id})
            return self.env['ir.actions.act_window'].for_xml_id('stock', 'action_package_view')

        @api.multi
        def view_content_package(self):
            action = self.env['ir.actions.act_window'].for_xml_id('stock', 'quantsact')
            action['domain'] = [('id', 'in', self._get_contained_quants().ids)]
            return action

        get_content_package = view_content_package

        def _get_contained_quants(self):
            return self.env['inventory.consolidated'].search([('package_id', 'child_of', self.ids)])

        get_content = _get_contained_quants

        def _get_all_products_quantities(self):
            '''This function computes the different product quantities for the given package
            '''
            # TDE CLEANME: probably to move somewhere else, like in pack op
            res = {}
            for quant in self._get_contained_quants():
                if quant.product_id not in res:
                    res[quant.product_id] = 0
                res[quant.product_id] += quant.qty
            return res
