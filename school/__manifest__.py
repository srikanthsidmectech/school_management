{
    'name': 'SM SYSTEM',
    'category': 'management',
    'version': '17.0.0.2',
    'author': 'SREEKANTH',
    'depends': ['mail', 'sale', 'report_xlsx', 'base', 'web'],
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
        'views/__invoicing_project__.xml',
        'views/product_brand_view.xml',
        'views/product_inherit.xml',
        'views/home.xml',
        'report/student_card.xml',
        'report/report.xml',
        'report/sales_report_view.xml',
        'report/sales_report.xml',
        'report/invoicing__project__report.xml',
        'report/invoicing__report_data.xml',
        'report/invoicing_report.xml'
    ],
    'license': 'LGPL-3',
    'installable': True,
    'autoinstall': True,

}
