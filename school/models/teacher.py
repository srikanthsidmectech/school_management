from odoo import models, fields


class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Teacher"
    _inherit = ["mail.thread"]

    name = fields.Char("Name", required=True, tracking=True)
    subject = fields.Selection([
        ('telugu', 'Telugu'),
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('mathematics', 'Mathematics'),
        ('physical_science', 'Physical Science'),
        ('social_studies', 'Social Studies')
    ], string="Subject", tracking=True)
    address = fields.Text("Address", tracking=True)
    date_of_birth = fields.Date("Date of Birth", tracking=True)
    teaching_class = fields.Selection([
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ], string='Teaching Standard', default='7', tracking=True)
    status = fields.Selection([
        ('not_created', 'Draft'),
        ('created', 'Done')
    ], string='Status', default="not_created", tracking=True)

    def action_create_teacher(self):
        for record in self:
            if record.status == 'not_created':
                record.status = 'created'
