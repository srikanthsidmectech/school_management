from odoo import models, fields, api
from odoo.exceptions import ValidationError


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

    user_id = fields.Many2one('res.users', string='login id')
    user_name = fields.Char(related='user_id.name', string='User', tracking=True, readonly=True)

    def action_create_teacher(self):
        for record in self:
            if record.status == 'not_created':
                user_vals = {
                    'name': record.name,
                    'login': record.name,
                    'email': f"{record.name}@gmail.com",
                    'password': record.name,
                    'groups_id': [(6, 0, [record.env.ref('school.group_school_teacher').id])]
                }

                # Create the user
                self.env['res.users'].create(user_vals)

                # Update the record status
                record.status = 'created'

    @api.model
    def create(self, vals):
        if vals.get('name'):
            existing_teacher = self.search([('name', '=', vals['name'])])
            if existing_teacher:
                raise ValidationError('A teacher with this guardian already exists.')
        return super(SchoolTeacher, self).create(vals)
