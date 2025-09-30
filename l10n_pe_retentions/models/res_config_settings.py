# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    retention_percentaje = fields.Float("Retension % (Obsoleto)")

    retention_percentage = fields.Char(
        string="Porcentaje de Retención %",
        default="3.00",
        config_parameter='retention_percentage'
    )
    amount_min_retention = fields.Char(
        string="Monto Mínimo Retención",
        default="700.00",
        config_parameter='amount_min_retention'
    )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        retention_percentage = self.env['ir.config_parameter'].sudo().get_param('retention_percentage')
        amount_min_retention = self.env['ir.config_parameter'].sudo().get_param('amount_min_retention')
        res.update(
            retention_percentage=retention_percentage,
            amount_min_retention=amount_min_retention
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param("retention_percentage", self.retention_percentage)
        self.env['ir.config_parameter'].set_param("amount_min_retention", self.amount_min_retention)