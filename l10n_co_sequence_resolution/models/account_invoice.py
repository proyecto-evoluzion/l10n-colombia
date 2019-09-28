# -*- coding: utf-8 -*-
# Copyright 2016 Dominic Krimmer
# Copyright 2016 Luis Alfredo da Silva (luis.adasilvaf@gmail.com)
# Copyright 2019 Joan Marín <Github@joanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime
from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.one
    def _get_warn_remaining(self):
        warn_remaining = False

        if self.journal_id.sequence_id.use_dian_control:
            remaining_numbers = self.journal_id.sequence_id.remaining_numbers
            remaining_days = self.journal_id.sequence_id.remaining_days
            active_resolution = self.env['ir.sequence.date_range'].search([
                ('sequence_id', '=', self.journal_id.sequence_id.id),
                ('active_resolution', '=', True)])
            today = datetime.strptime(fields.Date.context_today(self), '%Y-%m-%d')

            if len(active_resolution) == 1:
                active_resolution.ensure_one()
                date_to = datetime.strptime(active_resolution.date_to, '%Y-%m-%d')
                days = (date_to - today).days
                numbers = active_resolution.number_to - active_resolution.number_next_actual

                if numbers < remaining_numbers or days < remaining_days:
                    warn_remaining = True

        return warn_remaining

    warn_remaining = fields.Boolean(
        string="Warn Remaining",
        compute="_get_warn_remaining")
