from odoo import fields, models


class SchoolFeeStructure(models.Model):
    _name = "school.fee.structure"
    _description = "Fee Structure"


    student_id = fields.Many2one('school.student', string='Student', required=True)
    student_name = fields.Char(related='student_id.stu_name', string='Student Name', readonly=True)
    fee_type = fields.Selection([
        ('tuition', 'Tuition Fee'),
        ('lab', 'Lab Fee'),
        ('sports', 'Sports Fee'),
        ('other', 'Other Fee')
    ], string='Fee Type', required=True)
    amount = fields.Float(string='Amount', required=True, default=0.0)
    date_due = fields.Date(string='Due Date', required=True)
    status = fields.Selection([
        ('not_paid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Status', default='not_paid')

    def action_set_paid(self):
        for record in self:
            if record.status == 'not_paid':
                record.status = 'paid'