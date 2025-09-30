import re

from odoo import models,_
from odoo.tools import html2plaintext, cleanup_xml_node


L10N_PE_EDI_CHARGE_REASON = {
    '01': 'Intereses por mora',
    '02': 'Aumento en el valor',
    '03': 'Penalidades/ otros conceptos',
    '11': 'Ajustes de operaciones de exportación',
    '12': 'Ajustes afectos al IVAP',
}


class AccountEdiXmlUBLPE(models.AbstractModel):
    _inherit = 'account.edi.xml.ubl_pe'

    def _get_invoice_monetary_total_vals(self, invoice, taxes_vals, line_extension_amount, allowance_total_amount, charge_total_amount):
        result = super(AccountEdiXmlUBLPE, self)._get_invoice_monetary_total_vals(
            invoice, taxes_vals, line_extension_amount, allowance_total_amount, charge_total_amount
        )
        if invoice.is_invoice_regular_with_advanced_payments:
            prepaid_with_taxes = sum(
                abs(line.price_total) for line in invoice.invoice_line_ids if line.is_downpayment
            )
            
            prepaid_without_taxes = sum(
                abs(line.price_subtotal) for line in invoice.invoice_line_ids if line.is_downpayment
            )
            
            result["tax_exclusive_amount"] = result["tax_exclusive_amount"] + prepaid_without_taxes
            result["tax_inclusive_amount"] = result["tax_inclusive_amount"] + prepaid_with_taxes
            result["prepaid_amount"] = prepaid_with_taxes
            
        if invoice.tip_amount > 0:
            result["tax_inclusive_amount"] = result["tax_inclusive_amount"] - invoice.tip_amount
            
        return result

    def _get_note_vals_list(self, invoice):
        return [{'note': re.sub(r'[^\w ]|[áéíóúÁÉÍÓÚ]','',html2plaintext(invoice.narration)).strip()[:190]}] if invoice.narration else []

    def _get_invoice_line_price_vals(self, line):
        vals = super(AccountEdiXmlUBLPE,self)._get_invoice_line_price_vals(line)
        if len(line.tax_ids.filtered(lambda ta: ta.l10n_pe_edi_tax_code == "9996")) > 0:
            vals.update(price_amount=0)
        return vals

    def _get_invoice_tax_totals_vals_list(self, invoice, taxes_vals):
        # EXTENDS account.edi.xml.ubl_21
        vals = super()._get_invoice_tax_totals_vals_list(invoice, taxes_vals)

        def grouping_key_generator(base_line, tax_values):
            tax = tax_values['tax']
            return {
                'l10n_pe_edi_code': tax.tax_group_id.l10n_pe_edi_code,
                'l10n_pe_edi_international_code': tax.l10n_pe_edi_international_code,
                'l10n_pe_edi_tax_code': tax.l10n_pe_edi_tax_code,
            }

        tax_details_grouped = invoice._prepare_edi_tax_details(grouping_key_generator=grouping_key_generator,filter_invl_to_apply=lambda l: not any(l.tax_ids.mapped("l10n_pe_edi_is_tip")))
        isc_tax_amount = abs(sum([
            line.amount_currency
            for line in invoice.line_ids.filtered(lambda l: l.tax_line_id.tax_group_id.l10n_pe_edi_code == 'ISC')
        ]))
        vals[0]['tax_subtotal_vals'] = []
        for grouping_vals in tax_details_grouped['tax_details'].values():
            
            if grouping_vals["l10n_pe_edi_tax_code"] == "9996":
                taxable_amount = sum([line.quantity*line.price_unit for line in grouping_vals["records"] if line.flag_free_line])
                tax_amount = taxable_amount*1.18
            else:
                taxable_amount = (
                        grouping_vals['base_amount_currency']
                        - (isc_tax_amount if grouping_vals['l10n_pe_edi_code'] != 'ISC' else 0)
                    )
                tax_amount = grouping_vals['tax_amount_currency'] or 0.0

            vals[0]['tax_subtotal_vals'].append({
                'currency': invoice.currency_id,
                'currency_dp': invoice.currency_id.decimal_places,
                'taxable_amount': taxable_amount,
                'tax_amount': tax_amount,
                'tax_category_vals': {
                    'tax_scheme_vals': {
                        'id': grouping_vals['l10n_pe_edi_tax_code'],
                        'name': grouping_vals['l10n_pe_edi_code'],
                        'tax_type_code': grouping_vals['l10n_pe_edi_international_code'],
                    },
                },
            })

        return vals

    def _get_invoice_line_tax_totals_vals_list(self, line, taxes_vals):
        # OVERRIDES account.edi.xml.ubl_21
        vals = {
            'currency': line.currency_id,
            'currency_dp': line.currency_id.decimal_places,
            'tax_amount': line.price_total - line.price_subtotal,
            'tax_subtotal_vals': [],
        }
        for tax_detail_vals in taxes_vals['tax_details'].values():
            tax = tax_detail_vals['taxes_data'][0]['tax']
            
            if line.flag_free_line:
                taxable_amount = line.quantity*line.price_unit
                percent = tax.amount
                tax_amount = taxable_amount*(1+percent/100)
            else:
                taxable_amount = tax_detail_vals['base_amount_currency'] if tax.tax_group_id.l10n_pe_edi_code != 'ICBPER' else None
                percent = tax.amount if tax.amount_type == 'percent' else None
                tax_amount = tax_detail_vals['tax_amount_currency'] or 0.0

            vals['tax_subtotal_vals'].append({
                'currency': line.currency_id,
                'currency_dp': line.currency_id.decimal_places,
                'taxable_amount': taxable_amount,
                'tax_amount': tax_amount,
                'base_unit_measure_attrs': {
                    'unitCode': line.product_uom_id.l10n_pe_edi_measure_unit_code,
                },
                'base_unit_measure': int(line.quantity) if tax.tax_group_id.l10n_pe_edi_code == 'ICBPER' else None,
                'tax_category_vals': {
                    'percent': percent,
                    'tax_exemption_reason_code': (
                        line.l10n_pe_edi_affectation_reason
                        if tax.tax_group_id.l10n_pe_edi_code not in ('ISC', 'ICBPER') and line.l10n_pe_edi_affectation_reason
                        else None
                    ),
                    'tier_range': tax.l10n_pe_edi_isc_type if tax.tax_group_id.l10n_pe_edi_code == 'ISC' and tax.l10n_pe_edi_isc_type else None,
                    'tax_scheme_vals': {
                        'id': tax.l10n_pe_edi_tax_code,
                        'name': tax.tax_group_id.l10n_pe_edi_code,
                        'tax_type_code': tax.l10n_pe_edi_international_code,
                    },
                },
            })
        return [vals]

    def _get_invoice_line_vals(self, line, line_id, taxes_vals):
        if len(line.tax_ids.filtered(lambda ta: ta.l10n_pe_edi_tax_code == "9996")) > 0:

            vals = super(AccountEdiXmlUBLPE, self)._get_invoice_line_vals(line, line_id, taxes_vals)
            vals.update(allowance_charge_vals=[])

            vals['pricing_reference_vals'] = {
                'alternative_condition_price_vals': [{
                    'currency': line.currency_id,
                    'price_amount': line.price_unit,
                    'price_amount_dp': self.env['decimal.precision'].precision_get('Product Price'),
                    'price_type_code': '02'
                }]
            }
            vals.update(line_extension_amount=line.price_unit * line.quantity)

            return vals
        else:
            return super(AccountEdiXmlUBLPE, self)._get_invoice_line_vals(line, line_id, taxes_vals)

    def _get_document_allowance_charge_vals_list(self, invoice, taxes_vals=None):
        vals_list = super(AccountEdiXmlUBLPE, self)._get_document_allowance_charge_vals_list(invoice, taxes_vals)
        global_discount_subtotal = sum(
            [abs(line.price_subtotal) for line in invoice.invoice_line_ids if line.flag_discount_global])
        
        if global_discount_subtotal > 0:
            vals_list.append({
                'charge_indicator': 'false',
                'allowance_charge_reason_code': '02',
                'base_amount': abs(invoice.subtotal_venta) + abs(global_discount_subtotal),
                'amount': abs(global_discount_subtotal),
                'currency_dp': 2,
                'currency_name': invoice.currency_id.name,
            })
    
        if invoice.tip_amount > 0:
            vals_list.append({
                'charge_indicator': 'true',
                'allowance_charge_reason_code': '46',
                'base_amount': abs(invoice.total_venta),
                'amount': abs(invoice.tip_amount),
                'currency_dp': 2,
                'currency_name': invoice.currency_id.name,
            })   
        
        if invoice.is_invoice_regular_with_advanced_payments:
            # Total de factura sin Impuestos
            base_amount = amount = sum(
                abs(line.price_subtotal) for line in invoice.invoice_line_ids if not line.is_downpayment
            ) 
            
            # Total de anticipos sin impuestos
            amount = sum(
                abs(line.price_subtotal) for line in invoice.invoice_line_ids if line.is_downpayment
            ) 
            
            vals_list.append({
                'charge_indicator': 'false',
                'allowance_charge_reason_code': '04',
                'base_amount': base_amount,
                'amount': amount,
                'currency_dp': 2,
                'currency_name': invoice.currency_id.name,
            })

        return vals_list

    def _export_invoice_vals(self, invoice):
        vals = super(AccountEdiXmlUBLPE, self)._export_invoice_vals(invoice)
        order_reference = vals["vals"]["order_reference"]
        order_reference = re.sub(r'\W+', '', order_reference)
        taxes_vals = vals.get('taxes_vals', [])
        document_allowance_charge_vals_list = self._get_document_allowance_charge_vals_list(invoice, taxes_vals)
        
        # Compute values for invoice lines.
        line_extension_amount = 0.0
        invoice_lines = invoice.invoice_line_ids.filtered(
            lambda line: line.display_type not in ('line_note', 'line_section') and not line.is_downpayment)

        invoice_line_vals_list = []
        for line_id, line in enumerate(invoice_lines):
            line_taxes_vals = taxes_vals['tax_details_per_record'][line]
            line_vals = self._get_invoice_line_vals(line, line_id, line_taxes_vals)

            if not line.flag_discount_global and not line.is_tip:
                invoice_line_vals_list.append(line_vals)

            if not line.flag_free_line and not line.is_tip:
                line_extension_amount += line_vals['line_extension_amount']

        # Compute the total allowance/charge amounts.
        allowance_total_amount = 0.0
        charge_total_amount = 0.0
        for allowance_charge_vals in document_allowance_charge_vals_list:
            if allowance_charge_vals['charge_indicator'] == 'false' and \
                    allowance_charge_vals['allowance_charge_reason_code'] in ('00', '01', '47', '48'):
                allowance_total_amount += allowance_charge_vals['amount']
            elif allowance_charge_vals['charge_indicator'] == 'true':
                charge_total_amount += allowance_charge_vals['amount']

        vals["vals"]["line_vals"] = invoice_line_vals_list
        vals["vals"]["order_reference"] = order_reference[:20]
        vals["vals"]["monetary_total_vals"] = self._get_invoice_monetary_total_vals(
            invoice,
            taxes_vals,
            line_extension_amount,
            allowance_total_amount,
            charge_total_amount,
        )
        
        
        if vals['document_type'] == 'credit_note':
            if invoice.l10n_latam_document_type_id.code == '07':
                vals['vals'].update({
                    'discrepancy_response_vals': [{
                        'response_code': invoice.l10n_pe_edi_refund_reason,
                        'description': invoice.l10n_pe_edi_cancel_reason
                    }]
                })
            if invoice.reversed_entry_id:
                vals['vals'].update({
                    'billing_reference_vals': {
                        'id': invoice.reversed_entry_id.name.replace(' ', ''),
                        'document_type_code': invoice.reversed_entry_id.l10n_latam_document_type_id.code,
                    },
                })
        
        if vals['document_type'] == 'debit_note':
            if invoice.l10n_latam_document_type_id.code == '08':
                vals['vals'].update({
                    'discrepancy_response_vals': [{
                        'response_code': invoice.l10n_pe_edi_charge_reason,
                        'description': L10N_PE_EDI_CHARGE_REASON[invoice.l10n_pe_edi_charge_reason]
                    }]
                })
            if invoice.debit_origin_id:
                vals['vals'].update({
                    'billing_reference_vals': {
                        'id': invoice.debit_origin_id.name.replace(' ', ''),
                        'document_type_code': invoice.debit_origin_id.l10n_latam_document_type_id.code,
                    },
                })
                
                  
        if invoice.despatch_document_reference_ids.exists():
            vals['vals'].update({
                'despatch_document_reference_vals': [{
                    'id': ref.l10n_pe_document_number,
                    'document_type_code': ref.l10n_pe_document_code,
                } for ref in invoice.despatch_document_reference_ids],
            })
            
        additional_document_reference_list = []
        if invoice.document_reference_ids.exists():
            additional_document_reference_list += [{
                    'id': ref.l10n_pe_document_number,
                    'document_type_code': ref.l10n_pe_document_code,
                } for ref in invoice.document_reference_ids]
            
        def get_document_type_code(doc):
            if re.match(r'^(F|E)\w{3}-\d{8}$',doc) :
                return '02'
            elif re.match(r'^(B)\w{3}-\d{8}$',doc) :
                return '03'
            return None
        
        prepaid_payment_list = []
        if invoice.is_invoice_regular_with_advanced_payments:
            additional_document_reference_list +=[{
                'id': line.downpayment_ref,
                'document_type_code': get_document_type_code(line.downpayment_ref),
                'document_status_code': line.id,
                'party_identification_id':line.move_id.company_id.vat
            } for line in invoice.invoice_line_ids.filtered(lambda line:line.is_downpayment)]

            prepaid_payment_list += [{
                'id': line.id,
                'paid_amount': abs(line.price_total),
                'currency_name': invoice.currency_id.name,
                'currency_dp': 2
            } for line in invoice.invoice_line_ids.filtered(lambda line:line.is_downpayment)]
            
            vals["vals"].update({
                "prepaid_payment_list": prepaid_payment_list,
            })
            
        if additional_document_reference_list:
            vals['vals'].update({
                'additional_document_reference_list': additional_document_reference_list,
            })
        
        return vals



    def _get_invoice_payment_terms_vals_list(self, invoice):

        vals = super(AccountEdiXmlUBLPE,self)._get_invoice_payment_terms_vals_list(invoice)
        # OVERRIDES account.edi.xml.ubl_21
        spot = invoice._l10n_pe_edi_get_spot()
        spot_amount = 0
        
        if invoice.is_retention:
            spot_amount = invoice.retention_amount 
        elif spot:
            spot_amount = spot['amount'] if invoice.currency_id == invoice.company_id.currency_id else spot['spot_amount']

        invoice_date_due_vals_list = []


        #for line in invoice.line_ids.filtered(lambda l: l.display_type == 'payment_term').sorted('date_maturity'):
        for rec_line in invoice.line_ids.filtered(lambda l: l.account_type == 'asset_receivable').sorted('date_maturity'):
            
            amount = rec_line.amount_currency
            
            if spot or invoice.is_retention:
                line_percentaje = abs(rec_line.amount_currency/invoice.amount_total)
                cuota_detraccion = line_percentaje*spot_amount
                cuota_detraccion = round(cuota_detraccion, 2)
                amount -= cuota_detraccion
            
            invoice_date_due_vals_list.append({
                'currency_name': rec_line.currency_id.name,
                'currency_dp': rec_line.currency_id.decimal_places,
                'amount': amount,
                'date_maturity': rec_line.date_maturity,
            })

        payment_means_id = invoice._l10n_pe_edi_get_payment_means()
        
        if not (spot or invoice.is_retention):
            total_after_spot = abs(invoice.amount_total)
        else:
            if payment_means_id == "Contado":
                total_after_spot = abs(invoice.amount_total) - spot_amount
            else:
                total_after_spot = sum([l["amount"] for l in invoice_date_due_vals_list])

            
        vals = []
        if spot:
            vals.append({
                'id': spot['id'],
                'currency_name': 'PEN',
                'currency_dp': 2,
                'payment_means_id': spot['payment_means_id'],
                'payment_percent': spot['payment_percent'],
                'amount': spot['amount'],
            })
        if invoice.move_type not in ('out_refund', 'in_refund'):
            if payment_means_id == 'Contado':
                vals.append({
                    'id': 'FormaPago',
                    'payment_means_id': payment_means_id,
                })
            else:
                vals.append({
                    'id': 'FormaPago',
                    'currency_name': invoice.currency_id.name,
                    'currency_dp': invoice.currency_id.decimal_places,
                    'payment_means_id': payment_means_id,
                    'amount': total_after_spot,
                })
                for i, due_vals in enumerate(invoice_date_due_vals_list):
                    vals.append({
                        'id': 'FormaPago',
                        'currency_name': due_vals['currency_name'],
                        'currency_dp': due_vals['currency_dp'],
                        'payment_means_id': 'Cuota' + '{0:03d}'.format(i + 1),
                        'amount': due_vals['amount'],
                        'payment_due_date': due_vals['date_maturity'],
                    })

        return vals