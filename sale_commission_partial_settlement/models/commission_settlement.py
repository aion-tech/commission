from odoo import models


class CommissionSettlement(models.Model):
    _inherit = "commission.settlement"

    def unlink(self):
        self.mapped("line_ids.agent_line_partial_ids").unlink()
        return super().unlink()
