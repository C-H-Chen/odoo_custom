# -*- coding: utf-8 -*-
{
    'name': "saleorderline_add",

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
    'depends': ['sale','stock', 'sale_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/saleorderline_add_views.xml',
        'views/purchase_order_view.xml',
        'views/sale_multi_pick_wizard_view.xml',
        'views/stockmove_add_view.xml',
    ],
    "installable": True,
    "application": False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

