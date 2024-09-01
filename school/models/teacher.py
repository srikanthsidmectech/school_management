from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = "school.teacher"
    _description = "School Teacher"

    name = fields.Char("Name", required=True)
    subject = fields.Selection([
        ('telugu', 'Telugu'),
        ('hindi', 'Hindi'),
        ('english', 'English'),
        ('mathematics', 'Mathematics'),
        ('physical_science', 'Physical Science'),
        ('social_studies', 'Social Studies')
    ], string="Subject")
    address = fields.Text("Address")
    date_of_birth = fields.Date("Date of Birth")
    teaching_class = fields.Selection([
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    ], string='Teaching Standard', default='7')