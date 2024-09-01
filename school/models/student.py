from odoo import models, fields, api
from datetime import datetime
class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "School Student"
    _rec_name = 'stu_name'

    stu_name = fields.Char("Name", required=True)
    stu_standard = fields.Selection([
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ], string='Standard', default='7')
    stu_address = fields.Text(string="Address")
    date_of_birth = fields.Date(string='Date of Birth')
    stu_guard = fields.Char(string="Guardian")
    stu_guard_ph_no = fields.Char(string="Guardian Mobile Number")
    date_of_joining = fields.Date(string="Date of Joining", required=True)
    teacher_id = fields.Many2one('school.teacher', string='Class Teacher')
    teaching_staff_ids = fields.Many2many('school.teacher', string='Teaching Staff')
    class_teacher_subject = fields.Char(string="Subject", readonly=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True,readonly=True)

    fee_structure_ids = fields.One2many('school.fee.structure', 'student_id', string='Fee Structure')

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


