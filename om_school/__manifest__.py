# -*- coding: utf-8 -*-

{
    'name': 'School Management System',
    'version': '1.0.0',
    'category': 'School',
    'author': 'Unisoft Software ltd',
    'summary': ' School Management System',
    'description': 'School Management System',
    'sequence': -100,
    'depends': ['mail', 'product', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/student_tag_data.xml',
        'data/student.tag.csv',
        'data/sequence_data.xml',
        'data/mail_template_data.xml',
        'views/menu.xml',
        'wizard/cancel_admission_view.xml',

        'views/student_view.xml',
        'views/female_student_view.xml',
        'views/male_student_view.xml',
        'views/admission_view.xml',
        'views/student_tag_view.xml',
        'views/odoo_playground_view.xml',
        'views/odoo_query_view.xml',
        'views/res_config_settings_views.xml',
        'views/exam_view.xml',

        'reports/student_details_template.xml',
        'reports/report.xml',

    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

}
