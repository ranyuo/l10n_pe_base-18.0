# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError
from odoo.tools import float_is_zero, float_compare

import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
	_inherit = 'account.move'

	######################################################################################
	nro_constancia = fields.Char(string="Nro. de Constancia", copy=False)
	######################################################################################

	@api.depends(
		'invoice_line_ids.product_id',
		'invoice_line_ids.price_unit',
		'invoice_line_ids.quantity',
		'invoice_line_ids.price_subtotal',
		'amount_total_signed',
		'currency_id',
		'company_id','invoice_date','amount_total',
		'is_detraction')
	def _compute_detraccion(self):

		for rec in self:
			amount, porce = 0,0.0
			detrac_id = None

			rec.detraccion = False
			rec.detraccion_id = False

			for line in rec.invoice_line_ids:
				if line.detraccion_id:
					if line.detraccion_id.porcentaje > porce:
						porce = line.detraccion_id.porcentaje
						amount = line.detraccion_id.amount
						detrac_id = line.detraccion_id.id
			amount_total_signed = rec.amount_total
			if rec.currency_id and rec.company_id and rec.currency_id != rec.company_id.currency_id:
				currency_id = rec.currency_id
				amount_total_signed = currency_id._convert(rec.amount_total, rec.company_id.currency_id, rec.company_id, rec.invoice_date or fields.Date.today())
			
			if rec.is_detraction:
				rec.detraccion=True
				rec.detraccion_id = detrac_id
			elif abs(amount_total_signed) > amount and detrac_id:	
				rec.detraccion = True
				rec.detraccion_id = detrac_id
			else:
				rec.detraccion = False
				rec.detraccion_id = False
	###########################################################################################################


	@api.depends('detraccion_id', 'amount_total',
		'currency_id', 'company_id','invoice_date')
	def _amount_detraccion(self):

		for rec in self:
			rec.total_detraccion_contabilidad = 0.00
			total_detrac = 0.0
			if rec.detraccion_id:
				total_detrac = rec.amount_total
				if rec.currency_id and rec.company_id and rec.currency_id != rec.company_id.currency_id:
					currency_id = rec.currency_id
					total_detrac = currency_id._convert(rec.amount_total, rec.company_id.currency_id, rec.company_id, rec.invoice_date or fields.Date.today())
				total_detrac = total_detrac * (rec.detraccion_id.porcentaje or 0.0)/100.0
				rec.total_detraccion_contabilidad = total_detrac



	detraccion = fields.Boolean(string="Es Detracción?",compute="_compute_detraccion")#, store=True)
	register_detraction_id = fields.Many2one('account.detraction',string="Registro de Detracción", copy=False)
	detraccion_id = fields.Many2one('tipo.detraccion.line',string="Detracción", compute="_compute_detraccion")#,
	#	store=True)
	total_detraccion_contabilidad = fields.Monetary(string="Total Detracción",compute="_amount_detraccion",
		currency_field='detraccion_company_currency_id',readonly=True)#,store=True , )

	total_detraccion_contabilidad_manual = fields.Monetary(string="Total Detracción Manual",
		compute="compute_total_detraccion_contabilidad",currency_field='detraccion_company_currency_id')#store=True,
	
	is_detraction = fields.Boolean(string="Con Registro detraccion",readonly=False)

	#########################################################################


	@api.depends('total_detraccion_contabilidad')
	def compute_total_detraccion_contabilidad(self):
		for rec in self:
			rec.total_detraccion_contabilidad_manual = 0.00
			if rec.detraccion:
				rec.total_detraccion_contabilidad_manual = round(rec.total_detraccion_contabilidad)

	####################### CAMPOS PARA DETRACCION EN FACTURA CLIENTE
	@api.model
	def _operation_type(self):
		type = [('01', '01 - Venta de bienes o prestación de servicios'),
				('02', '02 - Retiro de bienes'),
				('03', '03 - Traslados que no son venta'),
				('04', '04 - Venta bolsa de productos'),
				('05', '05 - Venta de Bienes exonerados del IGV')]
		return type



	detraccion_journal_id = fields.Many2one('account.journal',string="Diario de Detracción",
		domain="[('detraction', '=', True)]")

	detraccion_currency_id = fields.Many2one('res.currency', string='Moneda')
	
	detraccion_company_currency_id = fields.Many2one('res.currency',string='Moneda Compañia',
		readonly=True,default=lambda self: self.env.user.company_id.currency_id)

	detraccion_nro_constancia = fields.Char(string="Nro. de Constancia")
	detraccion_fecha_pago = fields.Date(string="Fecha de Pago")
	detraccion_fecha_registro = fields.Date(string="Fecha de Registro")
	detraccion_tipo_detraccion_id = fields.Many2one('tipo.detraccion.line',string="Tipo Detracción")
	detraccion_communication = fields.Char(string='Concepto')
	detraccion_destination_account_id = fields.Many2one('account.account',string="cuenta destino")
	detraccion_operation_type = fields.Selection(selection=_operation_type,string="Operation type", default='01')
	detraccion_acc_number = fields.Char(string="Account number")

	exist_detraccion=fields.Boolean(string="Existe Registro de Detracción?",
		compute="compute_campo_exist_detraccion")#,store=True)
	####################################

	@api.onchange('detraccion_journal_id')
	def _change_detraccion_journal_id(self):
		for rec in self:
			if rec.detraccion_journal_id:
				rec.detraccion_acc_number = rec.detraccion_journal_id.bank_account_id.acc_number or ''
	#####################################
	
	def button_view_detraccion(self):
		if self.exist_detraccion:
			return {
				'name': 'Detracción',
				'view_type': 'form',
				'view_mode': 'list,form',
				'res_model': 'account.detraction',
				'view_id': False,
				'type': 'ir.actions.act_window',
				'domain': [('id', 'in', [self.register_detraction_id.id] or [])],
				'context': {'journal_id': self.journal_id.id,}
			}


	@api.depends('register_detraction_id')
	def compute_campo_exist_detraccion(self):
		#self.ensure_one()
		for rec in self:
			rec.exist_detraccion = False

			if rec.register_detraction_id:
				rec.exist_detraccion = True
			else:
				rec.exist_detraccion = False



	def get_account_id(self):
		for rec in self:
			if rec.partner_id:
				if rec.move_type=='out_invoice':
					return rec.partner_id.property_account_receivable_id
				elif rec.move_type=='in_invoice':
					return rec.partner_id.property_account_payable_id
			else:
				return None



	@api.onchange('detraccion')
	def _onchange_is_detraction(self):
		for rec in self:
			rec.is_detraction = rec.detraccion

	
	def action_confirm_detraction(self):
		#self.ensure_one()
		action = self.env.ref('l10n_pe_detraccion.action_detraccion_template').read()[0]
		form = self.env.ref('l10n_pe_detraccion.view_detracction_form', False)
		action['views'] = [(form and form.id or False, 'form')]
		action['res_id'] = self.register_detraction_id.id
		return action

	###########################################################################################################
	def action_detraction_open(self):
		if self.detraccion and (self.move_type in ['in_invoice','in_refund']) and self.is_detraction:
			if self.register_detraction_id:
				return self.action_confirm_detraction()
			return self.open_detraction_form()

	###########################################################################################################
	
	"""
	def action_post(self):
		ctx = self._context or {}
		if ctx.get('detraction'):
			return super(AccountMove, self).action_post()

		if self.detraccion and (self.move_type in ['in_invoice']) and self.is_detraction:
			if self.register_detraction_id:
				return self.action_confirm_detraction()
			return self.open_detraction_form()

		return super(AccountMove, self).action_post()
	"""

	def open_detraction_form(self):
		self.ensure_one()
		view = self.env.ref('l10n_pe_detraccion.view_invoice_detracction_form')

		invoice_date = self.invoice_date or fields.Date.context_today(self)
		date = self.date or fields.Date.context_today(self)
		
		is_autodetraction = False

		if self.amount_residual_signed == 0.00:
			is_autodetraction = True
		else:
			is_autodetraction = False

		return {
			'name': "Registro de Detracción",
			'view_mode': 'form',
			'view_type': 'form',
			'res_model': 'account.detraction',
			'view_id': view.id,
			'views': [(view.id, 'form')],
			'type': 'ir.actions.act_window',
			'target': 'new',
			'context': {
				'default_origin_move_id': self.id,
				'default_is_autodetraction':is_autodetraction,
				'default_detraccion_id' : self.detraccion_id.id,
				'default_fecha_movimiento' : invoice_date,
				'default_fecha_registro' : date,
				'default_fecha_pago' : date,
				'default_communication' : self.name or 'registro de detracción proveedor',
				'default_amount_real' : self.total_detraccion_contabilidad,
				'default_amount' : self.total_detraccion_contabilidad_manual,
				'default_currency_id' : self.currency_id.id,
				'origin_move_id' : self.id,
			}
		}

	
	def copy(self, default=None):
		default = dict(default or {})
		default.update(
			detraccion = self.detraccion,
			detraccion_id = self.detraccion_id.id or False,
			total_detraccion_contabilidad = self.total_detraccion_contabilidad or 0.00,
			total_detraccion_contabilidad_manual = self.total_detraccion_contabilidad_manual or 0.00,
			)
		return super(AccountMove, self).copy(default)

	################################################################################

class AccountMoveLine(models.Model):
	_inherit = 'account.move.line'

	@api.model
	def _compute_amount_fields(self, amount, src_currency, company_currency):

		amount_currency = False
		currency_id = False
		date = self.env.context.get('date') or fields.Date.today()
		company = self.env.context.get('company_id')
		company = self.env['res.company'].browse(company) if company else self.env.user.company_id
		
		if src_currency and src_currency != company_currency:
			amount_currency = amount
			amount = src_currency._convert(amount, company_currency, company, date)
			currency_id = src_currency.id
		else:
			amount_currency = amount
			currency_id = company_currency.id

		debit = amount > 0 and amount or 0.0
		credit = amount < 0 and -amount or 0.0
		return debit, credit, amount_currency, currency_id


	detraccion_id = fields.Many2one('tipo.detraccion.line',
		string="Detracción",
		compute="_compute_product_detraccion")#, store=True)


	@api.depends('product_id','move_id.invoice_date')
	def _compute_product_detraccion(self):
		#self.ensure_one()
		for rec in self:

			rec.detraccion_id = False
			date = rec.move_id.invoice_date or fields.Date.context_today(rec)
			detrac = False
			if rec.product_id:
				detrac = self.env['tipo.detraccion.line'].sudo().get_detraccion(rec.product_id.id, date).id or False
			rec.detraccion_id = detrac


	##########################################################################
	detraction_id = fields.Many2one('account.detraction', 
		string="Origen detraccion", help="Detraccion de la factura relacionada", copy=False)
	nro_constancia = fields.Char(string="Nro. Constancia Detracción", copy=False)
	operation_type = fields.Selection(related="detraction_id.operation_type",string="Tipo de Operación")
	acc_number = fields.Char(related="detraction_id.acc_number",string="Número de Cuenta Detracción")
	##########################################################################