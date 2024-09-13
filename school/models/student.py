from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "School Student"
    _rec_name = 'stu_name'
    _inherit = ["mail.thread"]

    stu_name = fields.Char("Name", tracking=True)
    stu_standard = fields.Selection([

        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ], string='Standard', default='7', tracking=True)
    user_id = fields.Many2one('res.users', string='login id')
    user_name = fields.Char(related='user_id.name', string='User', tracking=True, readonly=True)
    email_id = fields.Char(string="Email", tracking=True)

    # email=fields.Char(string="E-mail id")
    stu_address = fields.Text(string="Address", tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    stu_guard = fields.Char(string="Guardian", required=True, tracking=True)
    stu_guard_ph_no = fields.Char(string="Guardian Mobile Number", tracking=True)
    date_of_joining = fields.Date(string="Date of Joining", required=True, tracking=True)
    teacher_id = fields.Many2one('school.teacher', string='Class Teacher', tracking=True)
    teaching_staff_ids = fields.Many2many('school.teacher', string='Teaching Staff', tracking=True)
    class_teacher_subject = fields.Char(string="Subject", readonly=True, tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True, readonly=True, tracking=True)
    fee_structure_ids = fields.One2many('school.fee.structure', 'student_id', string='Fee Structure', tracking=True)
    status = fields.Selection([
        ('not_created', 'INCOMPLETE'),
        ('created', 'COMPLETE')
    ], string='Status', default="not_created", tracking=True)

    suggestion_ids = fields.One2many('school.student.suggestion', 'student_id', string='Suggestions')
    suggestion_count = fields.Integer(string='Number of Suggestions', compute='_compute_suggestion_count')

    total_amount = fields.Float(string='Total Amount', compute='_compute_totals', store=True)
    total_tax = fields.Float(string='Total Tax Amount', compute='_compute_totals', store=True)
    untaxed_amount = fields.Float(string='Untaxed Amount', compute='_compute_totals', store=True)


    invoice_count=fields.Integer(string="invoice count",compute="_compute_invoice_count")

    def action_create_student(self):
        for record in self:
            if record.status == 'not_created':
                user_vals = {
                    'name': record.stu_name,
                    'login': record.email_id,
                    'email': f"{record.email_id}",
                    'password': record.stu_name,
                    'groups_id': [(6, 0, [record.env.ref('school.group_school_student').id])]
                }

                # Create the user
                user_record = self.env['res.users'].create(user_vals)

                # Update the record status
                record.status = 'created'

                self.user_id = user_record.id

    @api.depends('fee_structure_ids')
    def _compute_totals(self):
        for student in self:
            total_amount = 0.0
            total_tax = 0.0
            untaxed_amount = 0.0
            for fee in student.fee_structure_ids:
                total_amount += fee.total_amount
                total_tax += fee.total_tax
                untaxed_amount += fee.amount

            student.total_amount = total_amount
            student.total_tax = total_tax
            student.untaxed_amount = untaxed_amount

    @api.onchange('teacher_id')
    def onchange_teacher_id(self):
        for rec in self:
            if rec.teacher_id:
                rec.class_teacher_subject = rec.teacher_id.subject
            else:
                rec.class_teacher_subject = False

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = datetime.today()
        for rec in self:
            if rec.date_of_birth:
                dob = fields.Date.from_string(rec.date_of_birth)
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                rec.age = age
            else:
                rec.age = 0

    @api.model
    def create(self, vals):
        if vals.get('stu_guard'):
            existing_student = self.search([('stu_guard', '=', vals['stu_guard'])])
            if existing_student:
                raise ValidationError('A student with this guardian already exists.')
        return super(SchoolStudent, self).create(vals)

    def action_student_suggestions(self):
        return {
            'name': _('Suggestion'),
            'view_mode': 'form',
            'res_model': 'school.student.suggestion',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_student_name': self.stu_name,
                'default_student_guard': self.stu_guard
            }
        }


    def _compute_invoice_count(self):
        self.invoice_count = self.env['account.move'].search_count(
            domain=[('partner_id', '=', self.user_id.partner_id.id)])

    def action_student_invoices(self):
        for record in self:
            partner_id = record.user_id.partner_id.id

            # Search for invoices related to the student's partner
            student_invoices = self.env['account.move'].search([
                ('partner_id', '=', partner_id),
                ('move_type', '=', 'out_invoice')
            ])

            if student_invoices:
                invoice_lines = [(0, 0, {
                    'invoice_date': inv.invoice_date,
                    'payment_ref': inv.payment_reference,
                    'due_date': inv.invoice_date_due,
                }) for inv in student_invoices]
                count=len(invoice_lines)
                print(count)


                return {
                    'name': _('Invoices'),
                    'view_mode': 'tree,form',
                    'res_model': 'account.move',
                    'domain': [('partner_id','=',partner_id)],
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_student_name': record.stu_name,
                        'default_student_invoices': invoice_lines,
                        'partner_id': partner_id
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('No Invoices Found'),
                        'message': _('No invoices were found for the selected student.'),
                        'type': 'warning',
                    }
                }

    @api.depends('suggestion_ids')
    def _compute_suggestion_count(self):
        self.suggestion_count = self.env['school.student.suggestion'].search_count(
            domain=[('student_name', '=', self.stu_name)])

    def action_view_suggestions(self):
        return {
            'name': _('Suggestion'),
            'view_mode': 'tree',
            'res_model': 'school.student.suggestion',
            'domain': [('student_name', '=', self.stu_name)],
            'type': 'ir.actions.act_window',
            'context': {
                'default_student_name': self.stu_name,
                'default_student_guard': self.stu_guard
            }
        }

    @api.model
    def search(self, domain=[], *args, **kwargs):
        # Add the filter to restrict access to own records
        if self.env.user.has_group('school.group_school_student'):  # Adjust the group as necessary
            domain += [('user_id', '=', self.env.user.id)]
        return super(SchoolStudent, self).search(domain, *args, **kwargs)

    def send_student_invitation(self):
        template = self.env.ref('school.email_template_school_student_invitation')
        for record in self:
            template.send_mail(record.id, force_send=True)

    def update_FeeState(self):
        print("Updates are working")
        today = datetime.today().date()
        print(f"Today's date: {today}")
        # Load the email template
        template = self.env.ref('school.email_template_fee_due_reminder')
        # Query for students with due fees
        students_with_due_fees = self.env['school.student'].search([
            ('fee_structure_ids.date_due', '<=', today)
        ])
        if not students_with_due_fees:
            print("No students with due fees found")
        # Iterate through students with due fees
        for student in students_with_due_fees:
            print(f"Processing student: {student.stu_name}")
            # Filter fees where the due date is today or earlier
            fees_due = []
            for fee in student.fee_structure_ids:
                if fee.date_due:
                    # Compare the fee's due date with today's date
                    if fee.date_due <= today:
                        fees_due.append(fee)
            # If there are due fees, send an email
            if fees_due:
                try:
                    template.send_mail(student.id, force_send=True)
                    print(f"Email sent to {student.stu_name} (ID: {student.email_id})")
                except Exception as e:
                    print(f"Failed to send email to {student.stu_name} (ID: {student.email_id}): {e}")
            else:
                print(f"No due fees for student {student.stu_name} (ID: {student.email_id})")
