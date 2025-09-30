# -*- coding: utf-8 -*-
# Copyright (c) 2025-Present Harrison Jonathan Chumpitaz Alverca (hchumpitaz92@gmail.com)

from odoo import models, _


class PosPayment(models.Model):
    _inherit = 'pos.payment'
    
    def _create_payment_moves(self, is_reverse=False):
        results = super(PosPayment, self)._create_payment_moves(is_reverse)
        # Add the ticket number to the reference and name of the move line and move
        for result in results:
            tickets = ",".join(result.pos_payment_ids.mapped('ticket'))
            result.ref = ((result.ref or "") + (tickets and _(" N° Voucher: ") + tickets or "")).strip()
            for line in result.line_ids:
                line.operation_number = tickets
                line.ref = ((line.ref or "") + (tickets and _(" N° Voucher: ") + tickets or "")).strip()
                line.name = ((line.name or "") + (tickets and _(" N° Voucher: ") + tickets or "")).strip()
        return results
    