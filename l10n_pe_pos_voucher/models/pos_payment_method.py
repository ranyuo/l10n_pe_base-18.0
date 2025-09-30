# -*- coding: utf-8 -*-
# Copyright (c) 2025-Present Harrison Jonathan Chumpitaz Alverca (hchumpitaz92@gmail.com)

from odoo import models, fields, api


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    is_card_payment = fields.Boolean(string='Card Payment', default=False, compute='_compute_is_card_payment')

    @api.depends('journal_id')
    def _compute_is_card_payment(self):
        for pm in self:
            pm.is_card_payment = True if pm.journal_id.type == 'bank' else False
    