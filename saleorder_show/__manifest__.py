# -*- coding: utf-8 -*-
{
    'name': "saleorder_show",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale', 'web'],

    # always loaded
    'data': [
        'views/order_show_views.xml',
    ],
    # 把前端資產放在 manifest 的 assets 區段（推薦）
    # 'assets': {
    #     'web.assets_backend': [
    #         'saleorder_show/static/src/js/show_expand.js',

    #     ],
    # },
    "installable": True,
    "application": False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

