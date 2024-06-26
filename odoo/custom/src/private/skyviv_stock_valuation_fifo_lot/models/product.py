# Copyright 2022 Ecosoft Co., Ltd (https://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models
from odoo.tools import float_is_zero


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _run_fifo(self, quantity, company):
        """Overwrite for fixed bug"""
        self.ensure_one()
        move_id = self._context.get("used_in_move_id")
        if self.tracking == "none" or not move_id:
            vals = super()._run_fifo(quantity, company)
        else:
            move = self.env["stock.move"].browse(move_id)
            move_lines = move._get_out_move_lines()
            tmp_value = 0
            tmp_remaining_qty = 0
            for move_line in move_lines:
                # Find back incoming stock valuation layers
                # (called candidates here) to value `quantity`.
                qty_to_take_on_candidates = move_line.product_uom_id._compute_quantity(
                    move_line.qty_done, move.product_id.uom_id
                )
                candidates = self._get_all_candidates(company).filtered(
                    lambda line: move_line.lot_id in line.lot_ids
                )
                for candidate in candidates:
                    qty_taken_on_candidate = min(
                        qty_to_take_on_candidates, candidate.remaining_qty
                    )

                    candidate_unit_cost = (
                        candidate.remaining_value / candidate.remaining_qty
                    )
                    value_taken_on_candidate = (
                        qty_taken_on_candidate * candidate_unit_cost
                    )
                    value_taken_on_candidate = candidate.currency_id.round(
                        value_taken_on_candidate
                    )
                    new_remaining_value = (
                        candidate.remaining_value - value_taken_on_candidate
                    )

                    candidate_vals = {
                        "remaining_qty": candidate.remaining_qty
                        - qty_taken_on_candidate,
                        "remaining_value": new_remaining_value,
                    }

                    candidate.write(candidate_vals)

                    qty_to_take_on_candidates -= qty_taken_on_candidate
                    tmp_value += value_taken_on_candidate

                    if float_is_zero(
                        qty_to_take_on_candidates,
                        precision_rounding=self.uom_id.rounding,
                    ):
                        break

                if candidates and qty_to_take_on_candidates > 0:
                    tmp_value += abs(candidate.unit_cost * -qty_to_take_on_candidates)
                    tmp_remaining_qty += qty_to_take_on_candidates

            # Calculate standard price (Sorted by lot created date)
            all_candidates = self._get_all_candidates(
                company, sort_by="lot_create_date"
            )
            new_standard_price = False
            if all_candidates:
                new_standard_price = all_candidates[0].unit_cost
            elif candidates:
                new_standard_price = candidate.unit_cost

            # Update standard price
            if new_standard_price and self.cost_method == "fifo":
                self.sudo().with_company(company.id).with_context(
                    disable_auto_svl=True
                ).standard_price = new_standard_price

            # Value
            vals = {
                "remaining_qty": -tmp_remaining_qty,
                "value": -tmp_value,
                "unit_cost": tmp_value / (quantity + tmp_remaining_qty),
            }
        return vals
