# -*- coding: utf-8 -*-
from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"

    default_claim_user_id = fields.Many2one(
        "res.users", string="Responsable de Reclamos y Quejas")
    default_claim_attention_period = fields.Integer(string="Plazo de atención de reclamo", default=15)

class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    claim_user_id = fields.Many2one(
        "res.users", related="company_id.default_claim_user_id", readonly=False, domain=[('share', '=', False)])

    claim_attention_period = fields.Integer(related="company_id.default_claim_attention_period", readonly=False)
