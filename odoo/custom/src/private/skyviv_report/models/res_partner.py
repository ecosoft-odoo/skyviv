# Copyright 2022 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import  fields, models



class ResPartner(models.Model):
    _inherit = "res.partner"

    purchase_approver = fields.Boolean()
