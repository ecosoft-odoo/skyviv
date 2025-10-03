# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    clearing_advance = fields.Boolean()
    wht_refund = fields.Boolean(string="Withholding Tax Refund")
    bypass_check_syncronize = fields.Boolean(
        string="Skip check receivable/payable account",
        copy=False,
    )

    def _synchronize_from_moves(self, changed_fields):
        return super(
            AccountPayment,
            self.filtered(lambda move: not move.bypass_check_syncronize),
        )._synchronize_from_moves(changed_fields)
