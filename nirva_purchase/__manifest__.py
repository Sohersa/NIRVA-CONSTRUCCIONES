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
    'category': 'stock',
    'version': '0.0.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'hr', 'account', 'purchase_requisition', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/security.xml',
        
        # FORM VIEWS
        'views/purchase_order_form.xml',
        'views/purchase_requisition_form.xml',
        'views/stock_picking_form.xml',
        'views/account_move_form.xml',
        # 'views/templates.xml',

        # REPORTS
        'reports/account_report_invoice_inherit.xml',
        'reports/stock_report_delivery_inherit.xml',
        'reports/purchase_quotation_report_inherit.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}