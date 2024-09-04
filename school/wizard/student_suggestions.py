from odoo import fields, models, api


class StudentSuggestion(models.TransientModel):
    _name = 'school.student.suggestion'
    _description = 'Student Suggestion'
    _inherit = ["mail.thread"]
    _rec_name = 'student_name'

    """student_id = fields.Many2one('school.student', string='Student', tracking=True)
    student_name = fields.Char(related='student_id.stu_name', string='Student Name', tracking=True)
    stu_guard = fields.Char(related='student_id.stu_guard', string='Father Name', tracking=True)"""

    student_name = fields.Char(string='Student Name', tracking=True, readonly=True)
    stu_guard = fields.Char(string='Father Name', tracking=True, readonly=True)
    suggestion = fields.Text(string='Note', tracking=True)

    def action_save(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window_close'}

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields_list):
        res = super(StudentSuggestion, self).default_get(fields_list)
        context = self.env.context

        default_student_name = context.get('default_student_name')
        default_student_guard= context.get('default_student_guard')

        if default_student_name:
            res.update({
                'student_name': default_student_name,
                'stu_guard': default_student_guard,
            })
        return res
