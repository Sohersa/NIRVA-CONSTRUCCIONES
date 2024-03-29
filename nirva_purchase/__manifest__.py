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
    'version': '0.0.7',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'hr', 'account', 'purchase_requisition', 'stock', 'hr_expense'],

    # always loaded
    'data': [
        # SECURITY
        'security/nirva_purchase_security.xml',
        'security/ir.model.access.csv',
        
        # FORM VIEWS
        'views/purchase_order_form.xml',
        'views/purchase_requisition_form.xml',
        'views/stock_location_form.xml',
        'views/stock_picking_form.xml',
        'views/account_move_form.xml',
        'views/res_partner_form.xml',
        'views/res_partner_bank_form.xml',
        'views/partner_property_form.xml',
        'views/hr_expense_form.xml',
        'views/hr_expense_sheet_form.xml',

        # MENUS
        'views/stock_location_menu.xml',

        # TREE VIEWS
        'trees/res_partner_bank_tree.xml',
        'trees/hr_expense_sheet_tree.xml',
        'trees/hr_my_expenses_tree.xml',
        'trees/purchase_requisition_tree.xml',
        'trees/purchase_order_view_tree.xml',
        'trees/purchase_order_kpis_tree.xml',
        'trees/account_invoice_tree.xml',

        # REPORTS
        'reports/account_report_invoice_inherit.xml',
        'reports/stock_report_delivery_inherit.xml',
        'reports/purchase_order_report_inherit.xml',
        'reports/purchase_quotation_report_inherit.xml',
        'reports/purchase_requisition_report_inherit.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}