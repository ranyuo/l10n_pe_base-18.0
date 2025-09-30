# -*- coding: utf-8 -*-
# Copyright (c) 2025-Present Harrison Jonathan Chumpitaz Alverca (hchumpitaz92@gmail.com)

from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    operation_number = fields.Char(string="Operation number")
    