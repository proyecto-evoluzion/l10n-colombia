# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields
import odoo.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    cost_price = fields.Float(
        string='Cost Price',
        digits=dp.get_precision('Product Price'),
        default=0)
    reference_price = fields.Float(
        string='Reference Price',
        digits=dp.get_precision('Product Price'),
        default=0)

    def _get_invoice_lines_taxes(self, tax, tax_amount, invoice_line_taxes_total):
        tax_code = tax.tax_group_id.tax_group_type_id.code
        tax_name = tax.tax_group_id.tax_group_type_id.name
        tax_percent = '{:.2f}'.format(tax_amount)

        if tax_code not in invoice_line_taxes_total:
            invoice_line_taxes_total[tax_code] = {}
            invoice_line_taxes_total[tax_code]['total'] = 0
            invoice_line_taxes_total[tax_code]['name'] = tax_name
            invoice_line_taxes_total[tax_code]['taxes'] = {}

        if tax_percent not in invoice_line_taxes_total[tax_code]['taxes']:
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent] = {}
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['base'] = 0
            invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['amount'] = 0

        invoice_line_taxes_total[tax_code]['total'] += (
            self.price_subtotal * tax_amount / 100)
        invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['base'] += (
            self.price_subtotal)
        invoice_line_taxes_total[tax_code]['taxes'][tax_percent]['amount'] += (
            self.price_subtotal * tax_amount / 100)

        return invoice_line_taxes_total

    def _get_information_content_provider_party_values(self):
        return {
            'IDschemeID': False,
            'IDschemeName': False,
            'ID': False}
