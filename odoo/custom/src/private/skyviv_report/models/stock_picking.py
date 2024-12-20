# Copyright 2021 Ecosoft Co., Ltd. <http://ecosoft.co.th>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    description = fields.Text(
        string="Description",
        translate=True,
    )
