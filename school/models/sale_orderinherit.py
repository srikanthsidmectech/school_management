from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string='Custom Field')
    bank_Name = fields.Char(string="Bank Name")
    bank_Account_number = fields.Char(string="Bank Account Number")
    bank_Branch = fields.Char(string="Bank Branch Name")
    bank_Ifsc_code = fields.Char(string="Bank Ifsc Code")
