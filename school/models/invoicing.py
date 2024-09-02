from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'


    customer_name= fields.Char(string='Custom Field')

