# -*- coding: utf-8 -*-
{
    'name': "out_process_order",

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
    'depends': ["purchase", "web"],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'report/templates.xml',
        'report/outsource_report.xml',
    ],
    "installable": True,
    "application": False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

