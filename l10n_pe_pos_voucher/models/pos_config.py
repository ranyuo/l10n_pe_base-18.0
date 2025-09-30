# -*- coding: utf-8 -*-
# Copyright (c) 2025-Present Harrison Jonathan Chumpitaz Alverca (hchumpitaz92@gmail.com)

from odoo import models, fields, _
from odoo.exceptions import UserError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    # journal_id = fields.Many2one(
    #     'account.journal',
    #     domain=lambda self: [('type', 'in', ('general', 'sale'))] if self.env.company.country_code != 'PE' else [('type', '=', 'general')])

    def open_ui(self):
        for config in self:
            if not config.company_id.country_id:
                raise UserError(_("You have to set a country in your company setting."))
        return super().open_ui()
    