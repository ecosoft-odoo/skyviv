# Copyright 2022 Ecosoft Co., Ltd (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _create_in_svl(self, forced_quantity=None):
        """ 1.Overwrite for skip check stock move - Multiple lot on the stock move is not
        allowed for incoming transfer
            2.Create a `stock.valuation.layer` from `self`.
        :param forced_quantity: under some circunstances, the quantity to value is different than
        the initial demand of the move (Default value = None)
        """
        layers = self.env["stock.valuation.layer"]
        svl_vals_list = []
        for move in self:
            move = move.with_company(move.company_id)
            valued_move_lines = move._get_in_move_lines()
            valued_quantity = 0
            for valued_move_line in valued_move_lines:
                valued_quantity += valued_move_line.product_uom_id._compute_quantity(valued_move_line.qty_done, move.product_id.uom_id)
            unit_cost = abs(move._get_price_unit())  # May be negative (i.e. decrease an out move).
            if move.product_id.cost_method == 'standard':
                unit_cost = move.product_id.standard_price
            svl_vals = move.product_id._prepare_in_svl_vals(forced_quantity or valued_quantity, unit_cost)
            svl_vals.update(move._prepare_common_svl_vals())
            if forced_quantity:
                svl_vals['description'] = 'Correction of %s (modification of past move)' % move.picking_id.name or move.name
            svl_vals_list.append(svl_vals)
            layer = self.env['stock.valuation.layer'].sudo().create(svl_vals_list)
            # Calculate standard price (Sorted by lot created date)
            if (
                move.product_id.cost_method == "fifo"
                and move.product_id.tracking != "none"
            ):
                all_candidates = move.product_id._get_all_candidates(
                    move.company_id, sort_by="lot_create_date"
                )
                if all_candidates:
                    move.product_id.sudo().with_company(
                        move.company_id.id
                    ).with_context(
                        disable_auto_svl=True
                    ).standard_price = all_candidates[
                        0
                    ].unit_cost
            layers |= layer
        return layers

