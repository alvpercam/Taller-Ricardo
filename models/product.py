from odoo import api, fields, models


class ProductCategory(models.Model):
    _inherit = 'product.category'

    categ_id = fields.Selection(
        selection=[
            ('Remolque', 'Remolque'),
            ('Rep in Situ', 'Rep in Situ'),
            ('Suplidos', 'Suplidos'),
            ('Alquiler', 'Alquiler'),
        ],
        string='Acción',
    )


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Compañía a aplicar',
        domain="[('customer_rank', '>', 0)]",
        ondelete='set null',
    )


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Compañía a aplicar',
        domain="[('customer_rank', '>', 0)]",
        ondelete='set null',
    )
    product_categ_id = fields.Many2one(
        comodel_name='product.category',
        string='Acción',
        ondelete='set null',
    )

    @api.onchange('product_tmpl_id', 'product_id')
    def _onchange_product_tmpl_id(self):
        super()._onchange_product_tmpl_id()
        for item in self:
            if item.pricelist_id:
                item.partner_id = item.pricelist_id.partner_id
            if item.product_tmpl_id:
                item.product_categ_id = item.product_tmpl_id.categ_id
