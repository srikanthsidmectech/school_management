from odoo import models, fields, api
from odoo.exceptions import ValidationError


# teacher model
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
    #action for creating student
    image = fields.Binary("Image", attachment=True)
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
                user_record = self.env['res.users'].create(user_vals)

                # Update the record status
                record.status = 'created'

                self.user_id = user_record.id
    #fetch teachers details and if it existed it can't be created.
    @api.model
    def create(self, vals):
        if vals.get('name'):
            existing_teacher = self.search([('name', '=', vals['name'])])
            if existing_teacher:
                raise ValidationError('A teacher with this guardian already exists.')
        return super(SchoolTeacher, self).create(vals)

    def get_user_company_logo_(self):
        user_company = self.env.user.company_id
        return user_company.logo

    # update current user company logo to student image fields
    def default_get(self, fields):
        res = super(SchoolTeacher, self).default_get(fields)
        res['image'] = self.get_user_company_logo_()
        return res