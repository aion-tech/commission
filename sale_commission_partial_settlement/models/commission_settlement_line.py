from odoo import api, fields, models


class CommissionSettlementLine(models.Model):
    _inherit = "commission.settlement.line"

    agent_line_partial_ids = fields.Many2many(
        comodel_name="account.invoice.line.agent.partial",
        relation="settlement_agent_line_partial_rel",
        column1="settlement_id",
        column2="agent_line_partial_id",
    )
    settled_amount = fields.Monetary(
        compute="_compute_settled_amount",
        related=False,
        readonly=True,
        store=True,
    )

    @api.depends("commission_id.payment_amount_type")
    def _compute_settled_amount(self):
        for rec in self:
            if rec.commission_id.payment_amount_type == "paid":
                rec.settled_amount = rec.agent_line_partial_ids[:1].amount
            else:
                rec.settled_amount = rec.invoice_agent_line_id[:1].amount

    def unlink(self):
        self.mapped("agent_line_partial_ids").unlink()
        return super().unlink()
