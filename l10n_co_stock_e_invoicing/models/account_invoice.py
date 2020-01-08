# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    invoice_type_code = fields.Selection(selection_add=[('02', 'Factura de Exportación')])
