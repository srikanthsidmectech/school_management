from odoo import fields, models, api, exceptions


class NewStudent(models.Model):
    _name = 'school.query'
    _description = "New Admission"
    _rec_name = 'student_name'
    _inherit = ["mail.thread"]

    custom_integer_id = fields.Integer(string="student ID", copy=False, readonly=True, index=True,
                                       default=lambda self: self._get_next_custom_integer_id())
    student_name = fields.Char(string="Name", tracking=True, required=True)
    student_class = fields.Integer(string='Class', tracking=True, required=True)
    stu_parent_name = fields.Char(string='Father Name', tracking=True, required=True)
    mobile_number = fields.Char(string='Father Mobile No', tracking=True, required=True)
    status = fields.Selection([
        ('not_created', 'INCOMPLETE'),
        ('created', 'COMPLETE')
    ], string='Status', default="not_created")

    _sql_constraints = [
        ('custom_integer_id_unique', 'unique(custom_integer_id)', 'Custom Integer ID must be unique.')
    ]

    def _get_next_custom_integer_id(self):
        # Get the next integer ID based on the maximum existing ID
        last_id = self.search([], limit=1, order='custom_integer_id desc').custom_integer_id
        return (last_id or 0) + 1

    @api.model
    def create(self, vals):
        if not vals.get('custom_integer_id'):
            vals['custom_integer_id'] = self._get_next_custom_integer_id()
        return super(NewStudent, self).create(vals)

    def action_create_student(self):
        Student = self.env['school.student']
        for record in self:
            existing_student = Student.search([
                ('stu_name', '=', record.student_name),
                ('stu_guard_ph_no', '=', record.mobile_number),
                ('stu_standard', '=', record.student_class)
            ])

            if existing_student:
                record.write({'status': 'created'})

                raise exceptions.UserError(
                    f"Student with Name: {record.student_name}, Phone Number: {record.mobile_number}, and Class: {record.student_class} already exists."
                )
            else:

                Student.create({
                    'stu_name': record.student_name,
                    'stu_standard': record.student_class,
                    'stu_guard': record.stu_parent_name,
                    'stu_guard_ph_no': record.mobile_number,
                    'date_of_joining': fields.Date.today(),  # Set today's date or any other default value
                })
                record.write({'status': 'created'})
