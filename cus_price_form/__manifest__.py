# -*- coding: utf-8 -*-
{
    'name': "cus_price_form",

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
    'depends': ['web', "sale", 'sale_management', "product", "stock"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/pricelist_views.xml',
    ],
    # "assets": {
    #     "web.assets_backend": [
    #         "cus_price_form/static/src/js/pricelist_packaging_toggle.js",
    #     ],
    # },
    'installable': True,
    'application': False,
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

