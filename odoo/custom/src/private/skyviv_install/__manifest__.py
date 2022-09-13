# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "SKYVIV: Install",
    "summary": "Used to install other modules",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "category": "SKYVIV",
    "author": "Ecosoft",
    "installable": True,
    "depends": [
        # Core Module
        "sale_management",
        "purchase_stock",
        # OCA Module
        "l10n_th_account_tax",
        "l10n_th_account_tax_expense",
        "l10n_th_account_tax_multi",
        "l10n_th_account_tax_report",
        "l10n_th_account_wht_cert_form",
    ],
}
