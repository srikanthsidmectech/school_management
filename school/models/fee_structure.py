from odoo import fields, models, api


class SchoolFeeStructure(models.Model):
    _name = "school.fee.structure"
    _description = "Fee Structure"
    _inherit = ["mail.thread"]
    _rec_name = 'fee_type'

    student_id = fields.Many2one('school.student', string='Student', tracking=True)
    # student_name = fields.Char(related='student_id.stu_name', string='Student Name', readonly=True,tracking=True)
    type_of_transaction = fields.Many2one('school.fee.transaction', string='Type of Transaction', tracking=True)

    product_ids = fields.Many2one("product.template", string="product")

    fee_type = fields.Selection([
        ('tuition', 'Tuition Fee'),
        ('lab', 'Lab Fee'),
        ('sports', 'Sports Fee'),
        ('other', 'Other Fee')
    ], string='Fee Type', tracking=True)
    tax = fields.Many2many('account.tax', string="Tax")
    amount = fields.Float(string='Amount', default=0.0, tracking=True)
    date_due = fields.Date(string='Due Date', tracking=True)
    status = fields.Selection([
        ('not_paid', 'Unpaid'),
        ('paid', 'Paid')
    ], string='Status', tracking=True, default="not_paid", compute='_compute_state_payment')

    invoice_id = fields.Many2one('account.move', string="invoice")

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
            record.total_tax = total_tax

    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    total_tax = fields.Float(string='Total tax amount', compute='_compute_total_amount', store=True)

    def action_button_method(self):
        print("Button action triggered")
        for record in self:
            # Verify the student record
            # if record.status == 'not_paid':
            #     record.status = 'paid'
            # if record.status == 'paid':
            #     record.status = 'not_paid'
            # if not record.student_id:
            #     print(f"No student found for fee structure {record.id}")
            #     continue
            #
            # if not record.student_id.user_id:
            #     print(f"No user found for student {record.student_id.id}")
            #     continue
            #
            # if not record.student_id.user_id.partner_id:
            #     print(f"No partner found for user {record.student_id.user_id.id}")
            #     raise ValueError("No partner found for student")

            partner_id = record.student_id.user_id.partner_id.id
            print(f"Partner ID: {partner_id}")

            if self.invoice_id:
                return {
                    'view_mode': 'form',
                    'type': 'ir.actions.act_window',
                    'tag': 'reload',
                    'res_model': 'account.move',
                    "res_id": self.invoice_id.id,
                    'target': 'current'

                }

            else:
                # Create the invoice
                invoice = self.env['account.move'].create({
                    'partner_id': partner_id,  # Set the partner ID here
                    'invoice_date': fields.Date.today(),  # Set invoice date as today
                    'move_type': 'out_invoice',  # or 'in_invoice' depending on the context
                    'invoice_line_ids': [(0, 0, {
                        'product_id': record.product_ids.id,
                        'fee_structure_ids': record.id,
                        'name': record.fee_type,
                        'account_id': partner_id,  # Example account, typically should be a valid account ID
                        'quantity': 1,
                        'price_unit': record.amount,
                        'tax_ids': [(6, 0, record.tax.ids)],
                    })],
                })
            self.invoice_id = invoice.id
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'account.move',
                "res_id": invoice.id,
                'target': 'current',
                'view_mode': 'form',
            }

    # @api.depends('student_id')
    def _compute_state_payment(self):
        for record in self:
            if record.invoice_id:
                payment_state = record.invoice_id.payment_state
                if payment_state == "paid":
                    record.status = "paid"
                else:
                    record.status = "not_paid"
            else:
                record.status = "not_paid"
