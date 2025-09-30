from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from odoo.tools import format_date,float_round
import re
import logging
_logger = logging.getLogger(__name__)


DICCIONARIO_DETRACCION = {
      '001':'Azúcar y melaza de caña',
      '002':'Arroz',
      '003':'Alcohol etílico',
      '004':'Recursos hidrobiológicos',
      '005':'Maíz amarillo duro',
      '006':'Algodón (Obsoleto)',
      '007':'Caña de azúcar',
      '008':'Madera',
      '009':'Arena y piedra',
      '010':'Residuos, subproductos, desechos, recortes y desperdicios',
      '011':'Bienes gravados con el IGV, o renuncia a la exoneración',
      '012':'Intermediación laboral y tercerización',
      '013':'Animales vivos',
      '014':'Carnes y despojos comestibles',
      '015':'Abonos, cueros y pieles de origen animal',
      '016':'Aceite de pescado',
      '017':'Harina, polvo y “pellets” de pescado, crustáceos, moluscos y demás invertebrados acuáticos',
      '018':'Embarcaciones pesqueras (Obsoleto)',
      '019':'Arrendamiento de bienes muebles',
      '020':'Mantenimiento y reparación de bienes muebles',
      '021':'Movimiento de carga',
      '022':'Otros servicios empresariales',
      '023':'Leche',
      '024':'Comisión mercantil',
      '025':'Fabricación de bienes por encargo',
      '026':'Servicio de transporte de personas',
      '027':'Servicio de transporte de carga',
      '028':'Transporte de pasajeros',
      '029':'Algodón en rama sin desmontar (Obsoleto)',
      '030':'Contratos de construcción',
      '031':'Oro gravado con el IGV',
      '032':'Páprika y otros frutos de los géneros capsicum o pimienta',
      '033':'Espárragos (Obsoleto)',
      '034':'Minerales metálicos no auríferos',
      '035':'Bienes exonerados del IGV',
      '036':'Oro y demás minerales metálicos exonerados del IGV',
      '037':'Demás servicios gravados con el IGV',
      '039':'Minerales no metálicos',
      '040':'Bien inmueble gravado con IGV',
      '041':'Plomo',
      '099':'Ley 30737',
      }

class AccountMove(models.Model):
    _inherit = "account.move"
    
    #CAMPO OBSOLETO
    l10n_pe_refund_reason = fields.Selection(
        selection=[
            ('01', 'Cancelación de la operación'),
            ('02', 'Cancelación por error en el RUC'),
            ('03', 'Corrección por error en la descripción'),
            ('04', 'Descuento global'),
            ('05', 'Descuento por item'),
            ('06', 'Reembolso total'),
            ('07', 'Reembolso por item'),
            ('08', 'Bonificación'),
            ('09', 'Disminución en el valor'),
            ('10', 'Otros conceptos'),
            ('11', 'Ajuste en operaciones de exportación'),
            ('12', 'Ajuste afectos al IVAP'),
            ('13', 'Ajuste en montos y/o fechas de pago'),
        ],
        string="Razón de nota de crédito (obsoleto)")

    l10n_pe_reason = fields.Char(string="Sustento")
    l10n_pe_reversed_date=fields.Date(related="reversed_entry_id.invoice_date", string="Fecha de comprobante")

    def action_post(self):
        if self.l10n_latam_document_type_id and self.l10n_latam_document_type_id.id == self.env.ref("l10n_pe.document_type01").id and \
                self.partner_id.l10n_latam_identification_type_id and \
                (self.partner_id.l10n_latam_identification_type_id != self.env.ref("l10n_pe.it_RUC") and \
                not (self.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code == '0' and self.l10n_pe_edi_operation_type in ('0200','0201','0202'))):
            raise ValidationError("Solo se puede publicar facturas para empresas con RUC o empresas no domiciliadas")
        super(AccountMove, self).action_post()


    ##############################################
    total_sale_taxed = fields.Monetary(
        string="Gravado",
        default=0.0,
        compute="_compute_amount",
        store=True)

    total_sale_igv = fields.Monetary(
        string="IGV",
        default=0.0,
        compute="_compute_amount",
        store=True)

    total_sale_export = fields.Monetary(
        string="Exportación",
        default=0.0,
        compute="_compute_amount",
        store=True)

    total_sale_unaffected = fields.Monetary(
        string="Inafecto",
        default=0.0,
        compute="_compute_amount",
        store=True)

    total_sale_exonerated = fields.Monetary(
        string="Exonerado",
        default=0.0,
        compute="_compute_amount",
        store=True)

    total_sale_free = fields.Monetary(
        string="Gratuita",
        default=0.0,
        compute="_compute_amount",
        store=True)

    total_selective_tax = fields.Monetary(
        string="Impuesto selectivo",
        default=0.0,
        compute="_compute_amount",
        store=True)

    subtotal_venta = fields.Monetary(
        string="Sub Total",
        default=0.0,
        compute="_compute_amount_total",
        store=True)

    total_venta = fields.Monetary(
        string="Total",
        default=0.0,
        compute="_compute_amount_total",
        store=True)

    total_sale_icbper = fields.Monetary(
        string="ICBPER",
        default=0.0,
        compute="_compute_amount",
        store=True)

    global_discount_total = fields.Monetary(
        string="Descuento Global - Imp. Incl",
        default=0.0,
        compute="_compute_amount",
        store=True
    )

    global_discount_subtotal = fields.Monetary(
        string="Descuento Global - Imp. Excl",
        default=0.0,
        compute="_compute_amount",
        store=True
    )
    
    tip_amount = fields.Monetary(
        string="Propina",
        default=0.0,
        compute="_compute_tip_amount",
        store=True
    )

    @api.depends('invoice_line_ids', 'invoice_line_ids.price_unit', 'invoice_line_ids.quantity')
    def _compute_tip_amount(self):
        for move in self:
            tip = 0.0
            for line in move.invoice_line_ids:
                if line.is_tip:
                    tip += line.price_subtotal
            move.tip_amount = tip

    total_discounts = fields.Monetary(
        string="Total de descuentos",
        default=0.0,
        compute="_compute_amount",
        store=True
    )

    subtotal_before_discount = fields.Monetary(
        string="Subtotal antes de descuentos",
        default=0.0,
        compute="_compute_amount",
        store=True
    )

    ##############################################

    @api.depends('invoice_line_ids', 'invoice_line_ids.quantity',
                 'invoice_line_ids.price_unit', 'invoice_line_ids.tax_ids')
    def _compute_amount(self):
        super(AccountMove, self)._compute_amount()

        for move in self:
            total_free = 0
            total_taxed = 0
            total_unaffected = 0
            total_exonerated = 0
            selective_tax = 0
            total_export = 0
            total_igv = 0
            #global_discount_total = 0
            #global_discount_subtotal = 0
            total_icbper = 0

            for line in move.invoice_line_ids:
                for line_tax in line.tax_ids:
                    if line_tax.l10n_pe_edi_tax_code == "9996":
                        total_free += line.quantity*line.price_unit
                    elif line_tax.l10n_pe_edi_tax_code == "9998":
                        total_unaffected += line.price_subtotal
                    elif line_tax.l10n_pe_edi_tax_code == "9997":
                        total_exonerated += line.price_subtotal
                    elif line_tax.l10n_pe_edi_tax_code == "9995":
                        total_export += line.price_subtotal
                    elif line_tax.l10n_pe_edi_tax_code == "2000":
                        selective_tax += line.price_subtotal
                    elif line_tax.l10n_pe_edi_tax_code == "7152":
                        total_icbper += (line_tax.amount or 0.00) * (line.quantity or 0.00)
                    elif line_tax.l10n_pe_edi_tax_code == "1000":
                        total_taxed += line.price_subtotal

                        ##################### IGV ######################
                        #if move.company_id.tax_calculation_rounding_method == 'round_per_line':
                        #    total_igv += (line.price_total - line.price_subtotal)
                        #elif move.company_id.tax_calculation_rounding_method == 'round_globally':
                        #    total_igv += (line.price_subtotal * line_tax.amount * 0.01)
                        ##############################################################

            for line in move.line_ids:
                if line.tax_line_id.l10n_pe_edi_tax_code == "1000":
                    total_igv += line.amount_currency

            """
            # CALCULO DE IMPUESTO SEGÚN METODO REDONDEO DE LA CONFIG:
            if move.company_id.tax_calculation_rounding_method == 'round_per_line':
                for line in move.line_ids:
                    for line_tax in line.tax_ids:
                        if line_tax.l10n_pe_edi_tax_code == "1000":
                            total_igv += line.price_subtotal * (line_tax.amount * 0.01)

            elif move.company_id.tax_calculation_rounding_method == 'round_globally':
                total_igv = sum([
                    line.price_subtotal * [line_tax.amount for line_tax in line.tax_ids
                                           if line_tax.l10n_pe_edi_tax_code == "1000"][0] * 0.01

                    for line in move.invoice_line_ids
                    if len([line.price_subtotal for line_tax in line.tax_ids
                            if line_tax.l10n_pe_edi_tax_code == "1000"])
                ])
            """

            move.total_discounts = sum(
                [abs(line.discount_amount if not line.flag_free_line and not line.flag_discount_global else 0) + abs(line.price_total if line.flag_discount_global else 0) for line in
                 move.invoice_line_ids])
            
            move.global_discount_total = sum([line.price_total for line in move.invoice_line_ids if line.flag_discount_global ])
            move.global_discount_subtotal = sum([line.price_subtotal for line in move.invoice_line_ids if line.flag_discount_global ])
            
            move.total_sale_free = total_free
            move.total_sale_taxed = total_taxed
            move.total_sale_unaffected = total_unaffected
            move.total_sale_exonerated = total_exonerated
            move.total_sale_export = total_export
            move.total_selective_tax = selective_tax
            move.total_sale_igv = abs(total_igv)
            move.total_sale_icbper = total_icbper
            move.subtotal_before_discount =  total_taxed + total_unaffected + total_exonerated + total_export + selective_tax + total_icbper + abs(move.global_discount_subtotal)
            """
            subtotal = move.tax_totals.get('subtotals', [])
            move.total_venta = move.tax_totals.get('amount_total', 0)
            if subtotal:
                move.subtotal_venta = subtotal[0]['amount'] if subtotal else 0
            """
    
    @api.depends('line_ids','tax_totals')
    def _compute_amount_total(self):
        for rec in self:
            

            _logger.info("rec.tax_totals: %s", rec.tax_totals)
            
            if rec.tax_totals:
                subtotal = rec.tax_totals.get('subtotals', [])
                rec.total_venta = rec.tax_totals.get('total_amount_currency', 0)
                if subtotal:
                    rec.subtotal_venta = subtotal[0]['base_amount_currency'] if subtotal else 0
            else:
                rec.subtotal_venta = 0
                rec.total_venta = 0

    remission_guide_ids = fields.Many2many('stock.picking',string="Movimientos Stock Asociados")

    correlative_remission_guides = fields.Char(string="Guías Remisión Asociadas",
        compute="compute_field_correlative_remission_guides",store=True)

    document_reference_ids = fields.One2many("account.move.document.reference", "move_id", string="Otros documentos relacionados")
    despatch_document_reference_ids = fields.One2many("despatch.document.reference", "move_id", string="Guías de Remisión")
    
    def search_and_set_stock_picking(self):
        for rec in self:
            if rec.move_type in ['out_invoice','out_refund'] and not rec.remission_guide_ids:
                query = """
                    select 
                        sp.id as picking_id
                        from account_move_line as aml
                        left join account_move am on am.id = aml.move_id 
                        left join sale_order_line_invoice_rel solir on solir.invoice_line_id = aml.id 
                        left join sale_order_line sol on sol.id = solir.order_line_id 
                        left join stock_move sm on sm.sale_line_id = sol.id 
                        left join stock_picking sp on sp.id = sm.picking_id 
                        where sp.state = 'done' and am.move_type in ('out_invoice','out_refund') and am.id=%s """%(rec.id)

                self.env.cr.execute(query)
                records = self.env.cr.dictfetchall()
                if records:
                    rec.remission_guide_ids = [i['picking_id'] for i in records if i['picking_id']]
                    
                    for doc in rec.remission_guide_ids:
                        if doc.l10n_latam_document_number:
                            self.env['despatch.document.reference'].create({
                                'move_id': rec.id,
                                'l10n_pe_document_number': doc.l10n_latam_document_number,
                                'l10n_pe_document_code': '09'
                            })


    @api.depends('remission_guide_ids')
    def compute_field_correlative_remission_guides(self):
        for rec in self:
            rec.correlative_remission_guides = ''
            if rec.remission_guide_ids:
                array_guides = list(rec.remission_guide_ids.filtered(lambda t:t.l10n_latam_document_number).\
                    mapped('l10n_latam_document_number'))

                if array_guides:
                    str_array_guides = ', '.join(array_guides)
                    rec.correlative_remission_guides = str_array_guides


    #####################################################################################
    
    is_invoice_regular_with_advanced_payments = fields.Boolean("Factura Regular con Pagos Anticipados",compute="_compute_is_invoice_regular_with_advanced_payments")

    @api.depends("invoice_line_ids","invoice_line_ids.account_id")
    def _compute_is_invoice_regular_with_advanced_payments(self):
        for record in self:
            record.is_invoice_regular_with_advanced_payments = any(record.invoice_line_ids.mapped(lambda r:r.is_downpayment))
            """
            used = []
            if record.is_invoice_regular_with_advanced_payments:
                for invoice in self:
                    order = self.env["sale.order"].search([("name","=",invoice.invoice_origin)])
                    for line in invoice.invoice_line_ids.filtered(lambda r: r.is_downpayment):
                        if order.exists():
                            lines = order.invoice_ids.filtered(lambda r: r.move_type == "out_invoice" and not r.reversal_move_id.exists() and not r.is_invoice_regular_with_advanced_payments and r.edi_state == "to_send").mapped("invoice_line_ids").filtered(lambda r: r.price_subtotal + line.price_subtotal == 0 and r not in used)
                            if lines.exists():
                                line.downpayment_ref = lines[0].move_id.name
                                used.append(lines[0])
            """
            
    @api.constrains('invoice_line_ids')
    def _check_downpayment_ref_format(self):
        for record in self:
            for line in record.invoice_line_ids:
                if line.is_downpayment and record.state == "posted":
                    if not re.match(r'^(F|B|E)\w{3}-\d{8}$', line.downpayment_ref or "") or not line.downpayment_ref:
                        raise ValidationError("El formato de referencia de pago anticipado debe ser 'FXXX-XXXXXXXX' para facturas o 'BXXX-XXXXXXXX' para boletas.")


    refund_moves_count = fields.Integer("Número de Notas de crédito", compute="_compute_refund_related_moves")
    is_refunded = fields.Boolean(compute="_compute_refund_related_moves")



    def _compute_refund_related_moves(self):
        for move in self:
            move.refund_moves_count = len(move.reversal_move_ids)
            move.is_refunded = move.refund_moves_count > 0


    def action_view_refund_moves(self):
        return {
            "name": "Notas de crédito",
            "view_mode": "tree,form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.mapped("reversal_move_ids").ids)],
        }


    def action_view_invoice_moves(self):
        return {
            "name": "Facturas",
            "view_mode": "tree,form",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "domain": [("id", "in", self.mapped("reversed_entry_id").ids)],
        }
        

    has_multi_code_detraccion = fields.Boolean(string="Tiene mas de un concepto de Detracción",
        compute="compute_campo_has_multi_code_detraccion",store=True)

    codigo_detraccion = fields.Char(string="Código Detracción",
        compute="compute_campo_has_multi_code_detraccion",store=True)

    porcentaje_detraccion = fields.Float(string="% Detracción",
        compute="compute_campo_has_multi_code_detraccion",store=True)

    monto_detraccion = fields.Monetary(string="Monto Detracción",currency_field="company_currency_id",
        compute="compute_campo_has_multi_code_detraccion",store=True)

    cuenta_detraccion = fields.Char(string="Cuenta Detracción",
        compute="compute_campo_has_multi_code_detraccion",store=True)


    @api.depends(
        'invoice_line_ids',
        'invoice_line_ids.product_id',
        'state',
        'l10n_pe_edi_operation_type')
    def compute_campo_has_multi_code_detraccion(self):
        for rec in self:
            rec.has_multi_code_detraccion = False

            max_percent = max(rec.invoice_line_ids.mapped('product_id.l10n_pe_withhold_percentage'), default=0)
            if max_percent and rec.l10n_pe_edi_operation_type in ['1001', '1002', '1003', '1004'] and rec.move_type == 'out_invoice':

                if rec.invoice_line_ids:
                    detraccion_codes = rec.invoice_line_ids.mapped('product_id.l10n_pe_withhold_code')
                    if len(detraccion_codes or '')>1:
                        rec.has_multi_code_detraccion = True
                ##########################################################################
                line = rec.invoice_line_ids.filtered(lambda r: r.product_id.l10n_pe_withhold_percentage == max_percent)[0]

                rec.codigo_detraccion = "%s-%s"%(
                    line.product_id.l10n_pe_withhold_code,
                    rec.get_concept_detraccion(line.product_id.l10n_pe_withhold_code))

                rec.porcentaje_detraccion = max_percent or 0.00

                rec.monto_detraccion = float_round(rec.amount_total_signed * (max_percent / 100.0), precision_rounding=1)

                national_bank = rec.env.ref('l10n_pe.peruvian_national_bank')
                national_bank_account = rec.company_id.bank_ids.filtered(lambda b: b.bank_id == national_bank)
                national_bank_account_number = national_bank_account[0].acc_number if national_bank_account else False

                rec.cuenta_detraccion = national_bank_account_number or ''
    ################################################################################################

    def get_concept_detraccion(self,code):
        if code:
            if code in DICCIONARIO_DETRACCION:
                return DICCIONARIO_DETRACCION[code] or ''
            else:
                return ''


    @api.depends('show_payment_term_details','monto_detraccion')
    def _compute_payment_term_details(self):
        super(AccountMove,self)._compute_payment_term_details()

        for invoice in self:
            spot = invoice._l10n_pe_edi_get_spot()
            spot_amount = 0
            if invoice.is_retention:
                spot_amount = invoice.retention_amount
            elif spot:
                spot_amount = spot['amount'] if invoice.currency_id == invoice.company_id.currency_id else spot['spot_amount']

            invoice.payment_term_details = False
            if invoice.show_payment_term_details and abs(invoice.amount_total) != 0:

                sign = 1 if invoice.is_inbound(include_receipts=True) else -1
                payment_term_details = []

                for line in invoice.line_ids.filtered(lambda l: l.display_type == 'payment_term').sorted('date_maturity'):

                    line_percentaje = abs(line.amount_currency/invoice.amount_total)
                    cuota_detraccion = line_percentaje*spot_amount

                    payment_term_details.append({
                        'date': format_date(self.env, line.date_maturity),
                        'amount': sign * line.amount_currency - cuota_detraccion,
                    })

                invoice.payment_term_details = payment_term_details
                
    inverse_currency_rate = fields.Float("Tipo de Cambio",compute="_compute_inverse_currency_rate",digits=[1,3])
    
    @api.depends('currency_id', 'invoice_date', 'company_id')
    def _compute_inverse_currency_rate(self):
        for move in self:
            move.inverse_currency_rate = self.env['res.currency']._get_conversion_rate(
                from_currency=move.currency_id,
                to_currency=move.company_id.currency_id,
                company=move.company_id,
                date=move.invoice_date or fields.Datetime.now().date(),
            )