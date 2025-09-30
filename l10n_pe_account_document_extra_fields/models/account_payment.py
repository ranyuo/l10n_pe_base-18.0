from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError,RedirectWarning
import re
import logging
_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = "account.payment"

    force_destination_account_id = fields.Many2one('account.account',string="Cuenta Contrapartida",
        domain="[('deprecated', '=', False), ('company_ids', '=', company_id)]")

    operation_number = fields.Char(string="N° Operación")

    l10n_pe_prefix_code=fields.Char(string="Serie Comprobante")

    l10n_pe_invoice_number=fields.Char(string="Correlativo Comprobante")
    
    aplication_aml_id = fields.Many2one('account.move.line',string="Movimiento Contable Aplicado",readonly=True)

    ###############################################################################################################


    @api.depends(
        'journal_id',
        'partner_id',
        'paired_internal_transfer_payment_id',
        'payment_type',
        'partner_type',
        'force_destination_account_id')
    def _compute_destination_account_id(self):
        super(AccountPayment,self)._compute_destination_account_id()
        for payment in self:
            if payment.force_destination_account_id:
                payment.destination_account_id = payment.force_destination_account_id



    def action_post(self):
        super(AccountPayment,self).action_post()

        aplication_aml_id = self.aplication_aml_id

        if aplication_aml_id:
            if aplication_aml_id.account_id and aplication_aml_id.account_id.reconcile and \
                not (aplication_aml_id.reconciled):

                payment_aml_id = self.move_id.line_ids.filtered(lambda y:y.account_id == aplication_aml_id.account_id)[0]
                
                if payment_aml_id:
                    (payment_aml_id + aplication_aml_id).reconcile()


        if self.move_id and self.operation_number:
            self.move_id.line_ids.write({'operation_number':self.operation_number or ''})

        if self.move_id and self.l10n_pe_prefix_code:
            self.move_id.line_ids.write({'l10n_pe_prefix_code':self.l10n_pe_prefix_code or ''})

        if self.move_id and self.l10n_pe_invoice_number:
            self.move_id.line_ids.write({'l10n_pe_invoice_number':self.l10n_pe_invoice_number or ''})
