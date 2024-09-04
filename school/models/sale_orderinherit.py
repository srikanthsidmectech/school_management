from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Adding a custom field
    custom_field = fields.Char(string='Custom Field')
