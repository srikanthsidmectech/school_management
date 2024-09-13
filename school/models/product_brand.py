from odoo import models, fields
from odoo.fields import Many2one


class ProductBrand(models.Model):
    _name = 'product.brand'
    _rec_name = 'brand_name'

    brand_name=fields.Char(string="Product Brand")


class ProductTemplateBrand(models.Model):
    _inherit = 'product.template'


    brand_id=fields.Many2one('product.brand',string='Brand')