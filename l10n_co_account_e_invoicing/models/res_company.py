# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from validators import url
from global_functions import get_pkcs12
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    einvoicing_enabled = fields.Boolean(string='E-Invoicing Enabled')
    out_invoice_sent = fields.Integer(string='Invoices Sent')
    out_refund_credit_sent = fields.Integer(string='Credit Notes Sent')
    out_refund_debit_sent = fields.Integer(string='Debit Notes Sent')
    profile_execution_id = fields.Selection(
        [('1', 'Production'), ('2', 'Test')],
        'Destination Environment of Document',
        default='2',
        required=True)
    test_set_id = fields.Char(string='Test Set Id')
    software_id = fields.Char(string='Software Id')
    software_pin = fields.Char(string='Software PIN')
    certificate_filename = fields.Char(string='Certificate Filename')
    certificate_file = fields.Binary(string='Certificate File')
    certificate_password = fields.Char(string='Certificate Password')
    signature_policy_url = fields.Char(string='Signature Policy Url')
    signature_policy_description = fields.Char(string='Signature Policy Description')
    signature_policy_filename = fields.Char(string='Signature Policy Filename')
    signature_policy_file = fields.Binary(string='Signature Policy File')
    files_path = fields.Char(string='Files Path')
    einvoicing_email = fields.Char(string='E-invoice email from', help="Enter the e-invoice sender's email.")
    einvoicing_partner_no_email = fields.Char(string='Failed Emails to', 
        help='Enter the email where the invoice will be sent when the customer does not have an email.')
    report_template = fields.Many2one(string='Report Template', comodel_name='ir.actions.report.xml')

    @api.onchange('signature_policy_url')
    def onchange_signature_policy_url(self):
        if not url(self.signature_policy_url):
            raise ValidationError(_('Invalid URL.'))

    @api.multi
    def write(self, vals):
        rec = super(ResCompany, self).write(vals)
        get_pkcs12(self.certificate_file, self.certificate_password)

        return rec
