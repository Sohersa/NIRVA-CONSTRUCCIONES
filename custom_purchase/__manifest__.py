# -*- coding: utf-8 -*-
{
    'name': "Purchase customizations",

    'summary': """'Purchase' customizations according to the Nirva logic.""",

    'description': """The module's purpose is to create a custom implementation for the existing purchase app.""",

    'author': "Oupp",
    'website': "https://www.sohersabim.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}