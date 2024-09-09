from odoo import fields, models, api


class SchoolFeeStructure(models.Model):
    _name = "school.fee.structure"
    _description = "Fee Structure"
    _inherit = ["mail.thread"]
    _rec_name = 'amount'

    student_id = fields.Many2one('school.student', string='Student', tracking=True)
    # student_name = fields.Char(related='student_id.stu_name', string='Student Name', readonly=True,tracking=True)
    type_of_transaction = fields.Many2one('school.fee.transaction', string='Type of Transaction', tracking=True)

    fee_type = fields.Selection([
        ('tuition', 'Tuition Fee'),
        ('lab', 'Lab Fee'),
        ('sports', 'Sports Fee'),
        ('other', 'Other Fee')
    ], string='Fee Type', tracking=True)
    tax=fields.Many2many('account.tax',string="Tax")
    amount = fields.Float(string='Amount', default=0.0, tracking=True)
    date_due = fields.Date(string='Due Date',tracking=True)
    status = fields.Selection([
        ('not_paid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Status', default='not_paid', tracking=True)

    def action_set_paid(self):
        for record in self:
            if record.status == 'not_paid':
                record.status = 'paid'

    @api.depends('amount', 'tax')
    def _compute_total_amount(self):
        for record in self:

            total_tax = 0.0

            for tax in record.tax:
                total_tax += (record.amount * tax.amount / 100)
            record.total_amount = record.amount + total_tax
            record.total_tax=total_tax


    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    total_tax = fields.Float(string='Total tax amount', compute='_compute_total_amount', store=True)



