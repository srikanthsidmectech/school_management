from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_name = fields.Char(string='Parent Name')
    customer_ph_no = fields.Char(string='parent mobile No')

    student_id=fields.Many2one('school.student',string="student")




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fee_structure_ids = fields.Many2one(
        'school.fee.structure',
        string='Fee Structure'
    )
