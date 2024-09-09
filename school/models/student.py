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
        if not template:
            raise ValueError("Email template not found")
        if template:
            print("template found")
            for record in self:
                if record.user_id:
                    print(record.user_id)
                    template.send_mail(record.id, force_send=True)
