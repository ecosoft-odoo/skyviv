# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    approver = fields.Many2one(
        comodel_name='res.partner',
        required=True,
        default=lambda self: self.env['res.partner'].search([
            ('name', 'ilike', 'Vivatvong Vichit-Vadakan')], limit=1 ).id
    )
