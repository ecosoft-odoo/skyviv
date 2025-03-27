# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.payment"

    clearing_advance = fields.Boolean()
    wht_refund = fields.Boolean(string="Withholding Tax Refund")
