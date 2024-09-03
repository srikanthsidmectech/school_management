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
    stu_address = fields.Text(string="Address", tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', required=True, tracking=True)
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

    def action_create_student(self):
        for record in self:
            if record.status == 'not_created':
                record.status = 'created'

    @api.onchange('teacher_id')
    def onchange_teacher_id(self):
        if self.teacher_id:
            self.class_teacher_subject = self.teacher_id.subject

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
                'default_student_id': self.stu_name
            }
        }
