{
    'name': 'SM SYSTEM',
    'category': 'management',
    'version': '17.0.0.2',
    'author': 'SREEKANTH',
    'depends': ['mail', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/email.xml',
        'data/fee_due_date_activity.xml',
        'data/email_template_fee_due_reminder.xml',
        'security/security.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/fee_transction_journal.xml',
        'views/student_suggestionview.xml',
        'views/fee_structureview.xml',
        'views/query_view.xml',
        'views/sale_orderinherit_views.xml',
        'views/sales_invoice_view.xml',
        'views/home.xml',
        'report/student_card.xml',
        'report/report.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'autoinstall': True

}
