# -*- coding: utf-8 -*-
{
    'name': "mrporder_add",

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
    'depends': ['mrp_workorder', 'mrp', 'purchase', 'stock', 'sale', 'product', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrpworkorder_views.xml',
        'views/saleorder_mrp_view.xml',
        #'views/shop_floor_view.xml',
        #'views/template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mrporder_add/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

