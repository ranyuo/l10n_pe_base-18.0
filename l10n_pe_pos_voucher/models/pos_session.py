# -*- coding: utf-8 -*-
# Copyright (c) 2025-Present Harrison Jonathan Chumpitaz Alverca (hchumpitaz92@gmail.com)

from odoo import models, _


class PosSession(models.Model):
    _inherit = 'pos.session'
    
    def _loader_params_pos_payment_method(self):
        result = super(PosSession, self)._loader_params_pos_payment_method()
        result['search_params']['fields'].append('is_card_payment')
        return result
    
    def _create_split_account_payment(self, payment, amounts):
        res = super(PosSession, self)._create_split_account_payment(payment, amounts)
        # Add the ticket number to the reference and name of the move line and move
        Payment = self.env['account.payment'].sudo().browse(res.move_id.payment_id.id)
        Move = self.env['account.move'].sudo().browse(res.move_id.id)
        if Payment:
            Payment.operation_number = payment.ticket
            Payment.ref = ((Payment.ref or "") + (payment.ticket and _(" N° Voucher: ") + payment.ticket or "")).strip()
        if Move:
            for line in Move.line_ids:
                line.operation_number = payment.ticket
                line.ref = ((line.ref or "") + (payment.ticket and _(" N° Voucher: ") + payment.ticket or "")).strip()
                line.name = ((line.name or "")+ (payment.ticket and _(" N° Voucher: ") + payment.ticket or "")).strip()
        return res
    