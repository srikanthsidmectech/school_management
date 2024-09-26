from odoo import models, fields


# product brand module
class ProductBrand(models.Model):
    _name = 'product.brand'
    _rec_name = 'brand_name'

    brand_name = fields.Char(string="Product Brand")


# product brand configure module
class ProductTemplateBrand(models.Model):
    _inherit = 'product.template'

    brand_id = fields.Many2one('product.brand', string='Brand')
