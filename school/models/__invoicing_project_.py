from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_name = fields.Char(string='Parent Name')
    customer_ph_no = fields.Char(string='parent mobile No')

    student_id=fields.Many2one('school.student',string="student")

    bank_Name = fields.Char(string="Bank Name")
    bank_Account_number = fields.Char(string="Bank Account Number")
    bank_Branch = fields.Char(string="Bank Branch Name")
    bank_Ifsc_code = fields.Char(string="Bank Ifsc Code")




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    fee_structure_ids = fields.Many2one(
        'school.fee.structure',
        string='Fee Structure'
    )

