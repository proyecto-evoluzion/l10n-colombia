# -*- coding: utf-8 -*-
# Copyright 2016 Dominic Krimmer
# Copyright 2016 Luis Alfredo da Silva (luis.adasilvaf@gmail.com)
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def _get_warn_resolution(self):
        warn_remaining = False
        warn_inactive_resolution = False

        if self.journal_id.sequence_id.use_dian_control:
            remaining_numbers = self.journal_id.sequence_id.remaining_numbers
            remaining_days = self.journal_id.sequence_id.remaining_days
            date_range = self.env['ir.sequence.date_range'].search([
                ('sequence_id', '=', self.journal_id.sequence_id.id),
                ('active_resolution', '=', True)])
            today = datetime.strptime(fields.Date.context_today(self), '%Y-%m-%d')

            if date_range:
                date_range.ensure_one()
                date_to = datetime.strptime(date_range.date_to, '%Y-%m-%d')
                days = (date_to - today).days
                numbers = date_range.number_to - date_range.number_next_actual

                if numbers < remaining_numbers or days < remaining_days:
                    warn_remaining = True
            else:
                warn_inactive_resolution = True

        self.warn_inactive_resolution = warn_inactive_resolution
        self.warn_remaining = warn_remaining

    warn_remaining = fields.Boolean(
        string="Warn About Remainings?",
        compute="_get_warn_resolution",
        store=False)
    warn_inactive_resolution = fields.Boolean(
        string="Warn About Inactive Resolution?",
        compute="_get_warn_resolution",
        store=False)
