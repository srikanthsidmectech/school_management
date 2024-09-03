from odoo import fields, models, api


class StudentSuggestion(models.TransientModel):
    _name = 'school.student.suggestion'
    _description = 'Student Suggestion'
    _inherit = ["mail.thread"]

    student_id = fields.Many2one('school.student', string='Student', tracking=True)
    student_name = fields.Char(related='student_id.stu_name', string='Student Name', tracking=True)
    stu_guard = fields.Char(related='student_id.stu_guard', string='Father Name', tracking=True)
    suggestion = fields.Text(string='Note', tracking=True)

    def action_save(self):
        self.ensure_one()
        self.env['school.student.suggestion'].create({
            'student_id': self.student_id.id,
            'student_name': self.student_name,
            'stu_guard': self.stu_guard,
            'suggestion': self.suggestion
        })
        return {'type': 'ir.actions.act_window_close'}


    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}