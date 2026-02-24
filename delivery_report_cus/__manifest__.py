# -*- coding: utf-8 -*-
{
    'name': "delivery_report_cus",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/delivery_report_template.xml',
        'report/action_delivery_report.xml',
        'views/delivery_report_cus_views.xml',
    ],
    # 'assets': {
    #     'web.report_assets_common': [
    #         'delivery_report_cus/static/src/scss/pdf.scss',
    #     ],
    # },
    'installable': True,
    'application': False,
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}

