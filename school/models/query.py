from odoo import fields, models, exceptions


class NewStudent(models.Model):
    _name = 'school.query'
    _description = "New Admission"
    _rec_name = 'student_name'

    student_name = fields.Char(string="Name")
    student_class = fields.Char(string='Class')
    stu_parent_name = fields.Char(string='Father Name')
    mobile_number = fields.Char(string='Father Mobile No')
    status = fields.Selection([
        ('not_created', 'INCOMPLETE'),
        ('created', 'COMPLETE')
    ], string='Status',default="not_created")

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
                # Notify the user that the student already exists
                raise exceptions.UserError(
                    f"Student with Name: {record.student_name}, Phone Number: {record.mobile_number}, and Class: {record.student_class} already exists.")


            else:
                # Create a new student record
                Student.create({
                    'stu_name': record.student_name,
                    'stu_standard': record.student_class,  # Assuming class maps to standard
                    'stu_guard': record.stu_parent_name,
                    'stu_guard_ph_no': record.mobile_number,
                    'date_of_joining': fields.Date.today(),  # Set today's date or any other default value
                })
                record.write({'status': 'created'})
