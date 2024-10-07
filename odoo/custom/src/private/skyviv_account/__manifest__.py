# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "SKYVIV: Account",
    "summary": "Used to install related modules",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "category": "SKYVIV",
    "author": "Ecosoft",
    "installable": True,
    "depends": [
        "account",
        "l10n_th_account_tax",
    ],
    "data": [
        "views/account_payment_views.xml",
    ],
}
