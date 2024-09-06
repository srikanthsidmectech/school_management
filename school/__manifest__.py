{
    'name': 'SM SYSTEM',
    'category': 'management',
    'version': '17.0.0.2',
    'author': 'SREEKANTH',
    'depends': ['mail', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/email.xml',
        'security/security.xml',
        'views/student_view.xml',
        'views/teacher_view.xml',
        'views/fee_transction_journal.xml',
        'views/student_suggestionview.xml',
        'views/fee_structureview.xml',
        'views/query_view.xml',  # Ensure this file name is correct
        'views/sale_orderinherit_views.xml',
        'views/sales_invoice_view.xml',
        'views/home.xml'
    ],
    'license': 'LGPL-3',  # Corrected license name
    'installable': True,
    'autoinstall': True
}
