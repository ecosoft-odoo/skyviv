# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat = fields.Char(copy=False)

    @api.constrains("vat")
    def _check_vat_length(self):
        for record in self:
            if record.vat and len(record.vat) != 13:
                raise ValidationError(
                    _("Identification Number must have exactly 13 digits.")
                )
