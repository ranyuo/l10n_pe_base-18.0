# -*- coding: utf-8 -*-
from collections import defaultdict

from odoo import Command, models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import frozendict
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'


    operation_number = fields.Char(string="N° Operación")

    l10n_pe_prefix_code=fields.Char(string="Serie Comprobante",store=True,readonly=False,
        compute="_compute_l10n_pe_prefix_code")

    l10n_pe_invoice_number=fields.Char(string="Correlativo Comprobante",store=True,readonly=False,
        compute="_compute_l10n_pe_invoice_number")

    sunat_table_01_id = fields.Many2one('l10n.pe.catalogs.sunat',string="Tipo de Medio de Pago SUNAT",
        domain="[('associated_table_id.name','=','TABLA 1'),('active_concept','=',True)]")

    ###################################################################################################################

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super(AccountPaymentRegister,self)._create_payment_vals_from_wizard(batch_result)

        payment_vals_extra = {
            'operation_number':self.operation_number or '',
            'l10n_pe_prefix_code':self.l10n_pe_prefix_code or '',
            'l10n_pe_invoice_number':self.l10n_pe_invoice_number or '',
            'sunat_table_01_id':self.sunat_table_01_id and self.sunat_table_01_id.id or False,
        }

        payment_vals.update(payment_vals_extra)

        return payment_vals


    @api.model
    def _get_batch_l10n_pe_prefix_code(self, batch_result):
        labels = set(line.l10n_pe_prefix_code or line.move_id.l10n_pe_prefix_code or '' for line in batch_result['lines'])
        return ' '.join(sorted(labels))



    @api.model
    def _get_batch_l10n_pe_invoice_number(self, batch_result):
        labels = set(line.l10n_pe_invoice_number or line.move_id.l10n_pe_invoice_number or '' for line in batch_result['lines'])
        return ' '.join(sorted(labels))

    @api.depends('can_edit_wizard')
    def _compute_l10n_pe_prefix_code(self):
        for wizard in self:
            if wizard.can_edit_wizard:
                batches = wizard.batches
                wizard.l10n_pe_prefix_code = wizard._get_batch_l10n_pe_prefix_code(batches[0])
            else:
                wizard.l10n_pe_prefix_code = False

    @api.depends('can_edit_wizard')
    def _compute_l10n_pe_invoice_number(self):
        for wizard in self:
            if wizard.can_edit_wizard:
                batches = wizard.batches
                wizard.l10n_pe_invoice_number = wizard._get_batch_l10n_pe_invoice_number(batches[0])
            else:
                wizard.l10n_pe_invoice_number = False