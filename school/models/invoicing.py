from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_name = fields.Char(string='Parent Name')
    customer_ph_no = fields.Char(string='parent mobile No')
    fee_structure_id = fields.Many2one(
        'school.fee.structure',
        string='Fee Structure'
    )
