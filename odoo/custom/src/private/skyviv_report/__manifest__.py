# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "SKYVIV: Report",
    "summary": "Customize Report template for SKYVIV",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "category": "SKYVIV",
    "author": "Ecosoft",
    "installable": True,
    "depends": [
        "account",
        "purchase",
        "sale",
        "stock",
    ],
    "data": [
        "data/paperformat.xml",
        "views/purchase_views.xml",
        "report/sale_report_templates.xml",
        "report/purchase_order_templates.xml",
        "report/report_payment_receipt_templates.xml",
        "report/report_invoice_template.xml",
        "report/report_stockpicking_operations.xml",
        "report/report.xml",
    ],
}
