from odoo import models, fields


# school type of transaction bank or cash
class SchoolFeeTransaction(models.Model):
    _name = "school.fee.transaction"
    _description = "Fee transaction"
    _rec_name = 'type_of_transaction'

    type_of_transaction = fields.Char(string='Type of transaction', tracking=True)
