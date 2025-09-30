from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError,RedirectWarning
from datetime import datetime, timedelta



class AccountMove(models.Model):
    _inherit = "account.move"


    id_mov = fields.Char(string="ID Mov",readonly=True,index=True)

    l10n_pe_prefix_code=fields.Char(string="Serie Comprobante")

    l10n_pe_invoice_number=fields.Char(string="Correlativo Comprobante")

    currency_tc = fields.Float(string='Tipo de Cambio',digits=(1, 6), default=1.0)

    is_invoice_in_me = fields.Boolean(string="Documento en ME",compute="compute_campo_is_invoice_in_me",
        store=True,default=False)

    allow_edit_prefix_code_invoice_number = fields.Boolean(string="Permitir editar Serie y Correlativo",
        related="journal_id.allow_edit_prefix_code_invoice_number",store=True)

    is_closing_process = fields.Boolean(string="Es Asiento Proceso de Cierre", readonly=True)

    is_opening_process = fields.Boolean(string="Es Asiento Proceso de Apertura", readonly=True)

    #################################################################################################################


    def action_account_move_line_views(self):
        if self.line_ids:

            return {
                "name":"Apuntes Contables",
                "type": "ir.actions.act_window",
                "res_model": "account.move.line",
                "view_mode": "list,form",
                "view_id": False,
                "domain":[('id','in',
                    self.line_ids.filtered(lambda t:t.display_type not in ['line_section']).mapped('id') or [])],}



    @api.depends('currency_id')
    def compute_campo_is_invoice_in_me(self):
        for rec in self:
            rec.is_invoice_in_me = False
            if rec.currency_id and rec.currency_id != rec.company_id.currency_id:
                rec.is_invoice_in_me = True
            else:
                rec.is_invoice_in_me = False



    @api.onchange('invoice_date','date','currency_id','partner_id')
    def get_currency_tc(self):
        for rec in self:
            
            v_rate = 1

            if rec.currency_id and rec.currency_id != rec.company_id.currency_id:

                pay_date = False

                if rec.invoice_date:
                    pay_date = rec.invoice_date
                elif rec.date:
                    pay_date = rec.date                    
                else:
                    pay_date = datetime.now(tz=timezone("America/Lima"))

                currency_company = self.env.company.currency_id
                rate = currency_company._convert(1, rec.currency_id , self.env.company, pay_date, round=False)

                v_rate = round(1/(rate if rate > 0 else 1),6)

            rec.currency_tc = v_rate

    ##############################################################

    @api.onchange('l10n_latam_document_number')
    def onchange_l10n_pe_prefix_code_invoice_number(self):
        for rec in self:
            if rec.l10n_latam_document_number and rec.move_type in ['in_invoice','in_refund']:

                name = rec.l10n_latam_document_number
                doc_code_prefix = rec.l10n_latam_document_type_id.doc_code_prefix
                if doc_code_prefix and name:
                    name = name.split(" ", 1)[-1]

                parts = name.split('-')

                if len(parts)==2:
                    rec.l10n_pe_prefix_code = parts[0]
                    rec.l10n_pe_invoice_number = parts[1]
                elif len(parts)==1:
                    rec.l10n_pe_invoice_number = parts[0]
                elif not parts:
                    rec.l10n_pe_prefix_code = ''
                    rec.l10n_pe_invoice_number = ''


    ##############################################################
    def set_l10n_pe_prefix_code_invoice_number(self):

        if self.name and self.move_type in ['out_invoice','out_refund'] and not self.allow_edit_prefix_code_invoice_number:

            name = self.name
            doc_code_prefix = self.l10n_latam_document_type_id.doc_code_prefix
            
            if doc_code_prefix and name:
                name = name.replace(" ", "")

            parts = name.split('-')

            if len(parts)==2:
                self.l10n_pe_prefix_code = parts[0]
                self.l10n_pe_invoice_number = parts[1]
            elif len(parts)==1:
                self.l10n_pe_invoice_number = parts[0]
            elif not parts:
                self.l10n_pe_prefix_code = ''
                self.l10n_pe_invoice_number = ''


    ######################################################################

    def action_post(self):
        result = super(AccountMove,self).action_post()

        for rec in self:
            rec.set_l10n_pe_prefix_code_invoice_number()

        for rec in self:
            for line in rec.line_ids:

                if not line.l10n_pe_prefix_code:
                    line.write({'l10n_pe_prefix_code':rec.l10n_pe_prefix_code or ''})

                if not line.l10n_pe_invoice_number:
                    line.write({'l10n_pe_invoice_number':rec.l10n_pe_invoice_number or ''})

                if line.payment_id:

                    if not line.operation_number:
                        line.write({'operation_number':line.payment_id.operation_number or False})


            if rec.move_type in ['out_invoice','out_refund','in_invoice','in_refund']:

                for line in rec.line_ids:

                    if not line.date_emission:
                        line.write({'date_emission':rec.invoice_date or ''})


        return result
    #######################################################################################


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    id_mov = fields.Char(string="ID Mov",readonly=True,index=True)

    l10n_pe_prefix_code=fields.Char(string="Serie Comprobante")

    l10n_pe_invoice_number=fields.Char(string="Correlativo Comprobante")
    
    operation_number = fields.Char(string="N° Operación")

    currency_tc= fields.Float(related='move_id.currency_tc', string='Tipo de Cambio', digits=(1, 6), store=True)

    date_emission = fields.Date(string="Fecha Emisión")

    is_closing_process = fields.Boolean(string="Es Movimiento Proceso de Cierre", readonly=True,
        related="move_id.is_closing_process", store=True)

    is_opening_process = fields.Boolean(string="Es Movimiento Proceso de Apertura", readonly=True,
        related="move_id.is_opening_process", store=True)

    ##############################################################################################################

    @api.model
    def cron_calculated_prefix_code_invoice_number(self,company_id,fecha_desde,fecha_hasta):

        self.env.cr.execute("""
            SELECT 
                matching_number,
                array_agg(id ORDER BY id) AS move_line_ids
            FROM account_move_line
            WHERE matching_number IS NOT NULL and company_id = %s and date>='%s' and date<='%s' 
            GROUP BY matching_number
        """%(company_id,fecha_desde,fecha_hasta))

        results = self.env.cr.fetchall()

        for matching_number, move_line_ids in results:
            lines = self.env['account.move.line'].browse(move_line_ids)

            llenos = lines.filtered(lambda l: l.l10n_pe_prefix_code or l.l10n_pe_invoice_number)
            if not llenos:
                continue

            prefix_set = set(llenos.mapped('l10n_pe_prefix_code'))
            invoice_set = set(llenos.mapped('l10n_pe_invoice_number'))

            if len(prefix_set) == 1 and len(invoice_set) == 1:
                prefix = list(prefix_set)[0]
                invoice = list(invoice_set)[0]

                for line in lines:
                    if not line.l10n_pe_prefix_code:
                        line.l10n_pe_prefix_code = prefix
                    if not line.l10n_pe_invoice_number:
                        line.l10n_pe_invoice_number = invoice
