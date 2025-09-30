from odoo import api, models, fields, _, _lt
from odoo.exceptions import ValidationError
from odoo.addons.l10n_pe_edi_stock.models.stock_picking import PE_TRANSFER_REASONS
import re

PE_TRANSFER_REASONS.extend([
    ('02', 'Compras'),
    ('05', 'Consignación'),
    ('06', 'Devolución'),
    ('07', 'Recojo de bienes transformados'),
    ('08', 'Importación'),
    ('09', 'Exportación')
])
class StockPicking(models.Model):
    _inherit = 'stock.picking'


    
    bultos = fields.Integer(string='Bultos', default=1)
    l10n_pe_edi_reason_for_transfer = fields.Selection(selection_add=[
                                                        ('02', 'Compras'),
                                                        ('05', 'Consignación'),
                                                        ('06', 'Devolución'),
                                                        ('07', 'Recojo de bienes transformados'),
                                                        ('08', 'Importación'),
                                                        ('09', 'Exportación')])
    
    def _l10n_pe_edi_generate_missing_data_error_list(self):
        """ Check that all the required data is present before generating the delivery guide.
            Based on SUNAT resolution 000123-2022 (published 2022-07-12), pages 48-54,
            and on the list of checks published at
            https://cpe.sunat.gob.pe/sites/default/files/inline-files/ValidacionesGREv20221020_publicacion.xlsx
        """
        super()._l10n_pe_edi_generate_missing_data_error_list()
        errors = []
        if not self.partner_id and self.l10n_pe_edi_reason_for_transfer == '01':
            errors.append(_('Please set a Delivery Address as the delivery guide needs one.'))
        if not self.partner_id.l10n_pe_district  and self.l10n_pe_edi_reason_for_transfer == '01':
            errors.append(_('The client must have a defined district.'))
        
        """
        if self.picking_type_id.code == 'internal' and self.l10n_pe_edi_reason_for_transfer != '04':
            errors.append('Las transferencias internas deben tener el motivo de transferencia establecido en "04 - Transferencias entre establecimientos de la misma empresa')
        if self.picking_type_id.code != 'internal' and self.l10n_pe_edi_reason_for_transfer == '04':
            errors.append('Las transferencias internas deben tener el motivo de transferencia establecido en "04 - Transferencias entre establecimientos de la misma empresa')
        """
         
        if not self.l10n_pe_edi_transport_type:
            errors.append(_('You must select a transport type to generate the delivery guide.'))
        if not self.l10n_pe_edi_reason_for_transfer:
            errors.append(_('You must choose the reason for the transfer.'))
        if not self.l10n_pe_edi_departure_start_date:
            errors.append(_('You must choose the start date of the transfer.'))
        if self.l10n_pe_edi_transport_type == '02' and not self.l10n_pe_edi_vehicle_id:
            errors.append(_('You must choose the transfer vehicle.'))
        if not self.company_id.partner_id.l10n_latam_identification_type_id:
            errors.append(_('A document type is required for the company.'))
        if not self.company_id.partner_id.vat:
            errors.append(_('An identification number is required for the company.'))
        warehouse_address = self.picking_type_id.warehouse_id.partner_id or self.company_id.partner_id
        if not warehouse_address.l10n_pe_district:
            errors.append(_('The origin address must have a defined district.'))
        if not warehouse_address.street:
            errors.append(_('The origin address must have a defined street.'))
        if self.company_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code != "6":
            errors.append(_("The company's ID type must be set to RUC on the company contact page."))
        if (self.l10n_pe_edi_transport_type == '02' and not self.l10n_pe_edi_operator_id and not self.l10n_pe_edi_vehicle_id.is_m1l
            or self.l10n_pe_edi_transport_type == '01' and not self.l10n_pe_edi_operator_id):
            errors.append(_("You must choose the transfer operator."))
        return errors

    l10n_pe_edi_related_document_type = fields.Selection(selection_add=[('07','Nota de Crédito')])

    l10n_pe_edi_related_document_date = fields.Date("Fecha de Documento Relacionado")
            
    invoices_ids = fields.Many2many(
        'account.move',
        string="Facturas",
        help="Facturas asociadas a la orden de venta"
    )
    
    def action_update_state_invoice(self):
        for picking in self:
            picking.associate_invoices()
                

    def associate_invoices(self):
        for picking in self:
            if picking.sale_id:
                invoices = picking.sale_id.invoice_ids.filtered(lambda inv: inv.state == 'posted' and \
                                                                inv.payment_state in ('paid','in_payment'))
                
                picking.invoices_ids = [(6,0,invoices.ids)]

    @api.constrains('l10n_pe_edi_related_document_type', 'l10n_pe_edi_related_document_date')
    def _check_related_document_date_required(self):
        for rec in self:
            if rec.l10n_pe_edi_related_document_type and not rec.l10n_pe_edi_related_document_date:
                raise ValidationError(_('Debe ingresar la fecha del documento relacionado.'))


    @api.constrains('l10n_pe_edi_related_document_type','l10n_pe_edi_document_number')
    def _check_format_related_document(self):
        for rec in self:
            if rec.l10n_pe_edi_related_document_type == '01' and rec.l10n_pe_edi_document_number:
                pattern_01 = r'^[F|E][A-Za-z0-9]{3}-\d{1,8}$'
                if not re.match(pattern_01, rec.l10n_pe_edi_document_number):
                    raise ValidationError(_('El Factura relacionada debe tener el formato FXXX-NNNNNNNN o EXXX-NNNNNNNN, donde X es alfanumérico y N son solo dígitos.'))
                        
            
            if rec.l10n_pe_edi_related_document_type == '03' and rec.l10n_pe_edi_document_number:
                pattern_03 = r'^[B|E][A-Za-z0-9]{3}-\d{1,8}$'
                if not re.match(pattern_03, rec.l10n_pe_edi_document_number):
                    raise ValidationError(_('La Boleta relacionada debe tener el formato BXXX-NNNNNNNN o EXXX-NNNNNNNN, donde X es alfanumérico y N son solo dígitos.'))

            if rec.l10n_pe_edi_related_document_type == '09' and rec.l10n_pe_edi_document_number:
                pattern_09 = r'^T[A-Za-z0-9]{3}-\d{1,8}$'
                pattern_09_1 = r'^EG[A-Za-z0-9]{2}-\d{1,8}$'
                if not re.match(pattern_09, rec.l10n_pe_edi_document_number) and not re.match(pattern_09_1, rec.l10n_pe_edi_document_number):
                    raise ValidationError(_('La guía de remisión relacionada debe tener el formato EGXX-NNNNNNNN o TXXX-NNNNNNNN, donde X es alfanumérico y N son solo dígitos.'))


            if rec.l10n_pe_edi_related_document_type == '31' and rec.l10n_pe_edi_document_number:
                pattern_31 = r'^[V][A-Za-z0-9]{3}-\d{1,8}$'
                pattern_31_1 = r'^[EG][A-Za-z0-9]{2}-\d{1,8}$'
                if not re.match(pattern_31, rec.l10n_pe_edi_document_number) and not re.match(pattern_31_1, rec.l10n_pe_edi_document_number):
                    raise ValidationError(_('La guía de remisión relacionada debe tener el formato EGXX-NNNNNNNN o VXXX-NNNNNNNN, donde X es alfanumérico y N son solo dígitos.'))
