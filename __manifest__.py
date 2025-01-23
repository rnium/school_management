# -*- coding: utf-8 -*-
{
    'name': "School Management System",

    'summary': "This module help school to manage their students, teachers and parents and their information.",

    'description': """
        Long description of module's purpose
    """,

    'author': "Shamim Hossen",
    'website': "https://www.myschool.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'sale'],
    'assets': {
        'web.report_assets_common': [
            'school_management/static/src/css/fonts.css',
        ]
    },

    # always loaded
    'data': [
        'security/school_management_security.xml',
        'security/ir.model.access.csv',
        'data/school_management.playground.csv',
        'data/school_management.student.csv',
        'data/school_management.teacher.csv',
        'data/course.xml',
        'data/school.xml',
        'data/school_management.result.csv',
        'data/school_management.parent.csv',
        'data/student_weight.xml',
        'views/res_config_settings_views.xml',
        'views/school.xml',
        'views/result.xml',
        'views/student.xml',
        'views/course.xml',
        'views/library.xml',
        'views/stats_wizard.xml',
        'views/parent_view.xml',
        'views/menus.xml',
        'views/portal_templates.xml',
        'views/ir_sequence.xml',
        'report/certificate_layout_pageformats.xml',
        'report/student_report.xml',
        'report/student_testimonial.xml',
        'report/school_report.xml',
        'views/sale_order_line_with_image.xml',
        'views/email_templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/student_data.xml',
    # ],
    'web.assets_backend': [
        'school_management/static/src/js/custom_kanban_renderer.js',
        'school_management/static/src/js/custom_kanban_view.js',
    ],
}
