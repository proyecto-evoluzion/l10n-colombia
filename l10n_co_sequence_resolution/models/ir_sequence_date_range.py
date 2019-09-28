# -*- coding: utf-8 -*-
# Copyright 2016 Dominic Krimmer
# Copyright 2016 Luis Alfredo da Silva (luis.adasilvaf@gmail.com)
# Copyright 2019 Joan Marín <Github@joanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import ValidationError


class IrSequenceDateRange(models.Model):
    _inherit = 'ir.sequence.date_range'

    prefix = fields.Char(string='Prefix')
    use_dian_control = fields.Boolean(
        related='sequence_id.use_dian_control',
        string='Journal Type',
        store=False)
    resolution_number = fields.Char(string='Resolution Number')
    number_from = fields.Integer( string='Initial Number', default=False)
    number_to = fields.Integer(string='Final Number', default=False)
    active_resolution = fields.Boolean(string='Active Resolution')

    def _next(self):
        msg = _('Number Next must be included in Number Range.')

        if self.number_from and self.number_to:
            if (self.number_next_actual > self.number_to
                    or self.number_from > self.number_next_actual):
                raise ValidationError(msg)

        return super(IrSequenceDateRange, self)._next()
