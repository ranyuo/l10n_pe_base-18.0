# -*- coding: utf-8 -*-
# Copyright (c) 2025-Present Harrison Jonathan Chumpitaz Alverca (hchumpitaz92@gmail.com)

from odoo import models, fields, api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    voucher_number = fields.Char("Voucher number", help="Voucher number for the order", readonly=True)
    
    def _export_for_ui(self, order):
        fields = super()._export_for_ui(order)
        if self.env.company.country_code == 'PE':
            fields['voucher_number'] = order.voucher_number
        return fields
    
    def _order_fields(self, ui_order):
        fields = super()._order_fields(ui_order)
        if self.env.company.country_code == 'PE':
            fields['voucher_number'] = ui_order['voucherNumber'] if 'voucherNumber' in ui_order else False
        return fields
    
    # def _prepare_invoice_vals(self):
    #     vals = super()._prepare_invoice_vals()
    #     if self.env.company.country_code == 'PE':
    #         vals['payment_reference'] = self.voucher_number
    #     return vals
     