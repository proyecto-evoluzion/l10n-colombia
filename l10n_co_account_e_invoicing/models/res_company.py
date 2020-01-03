# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@JoanMarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from validators import url
from global_functions import get_pkcs12, get_xml_soap_with_signature, get_template_xml
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from requests import post, exceptions
from lxml import etree


class ResCompany(models.Model):
    _inherit = "res.company"

    einvoicing_enabled = fields.Boolean(string='E-Invoicing Enabled')
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
    files_path = fields.Char(string='Files Path')
    einvoicing_email = fields.Char(
        string='E-invoice Email From',
        help="Enter the e-invoice sender's email.")
    einvoicing_partner_no_email = fields.Char(
        string='Failed Emails To', 
        help='Enter the email where the invoice will be sent when the customer does not have an email.')
    report_template = fields.Many2one(
        string='Report Template',
        comodel_name='ir.actions.report.xml')
    notification_group_ids = fields.One2many(
        comodel_name='einvoice.notification.group',
        inverse_name='company_id',
        string='Notification Group')

    @api.onchange('signature_policy_url')
    def onchange_signature_policy_url(self):
        if not url(self.signature_policy_url):
            raise ValidationError(_('Invalid URL.'))

    @api.multi
    def write(self, vals):
        rec = super(ResCompany, self).write(vals)
        get_pkcs12(self.certificate_file, self.certificate_password)

        return rec

    def getProductionData(self):
        msg1 = _("Unknown Error,\nStatus Code: %s,\nReason: %s,\nContact with your administrator "
                "or you can choose a journal with a Contingency Checkbook E-Invoicing sequence "
                "and change the Invoice Type to 'Factura por Contingencia Facturador'.")
        msg2 = _("Unknown Error: %s\nContact with your administrator "
                "or you can choose a journal with a Contingency Checkbook E-Invoicing sequence "
                "and change the Invoice Type to 'Factura por Contingencia Facturador'.")
        b = "http://schemas.datacontract.org/2004/07/UploadDocumentResponse"
        wsdl = "DIAN['wsdl-hab']"

        SendBillAsync_values = self._get_SendBillAsync_values()
        xml_soap_with_signature = get_xml_soap_with_signature(
            get_template_xml(SendBillAsync_values, 'ProductionStage'),
            SendBillAsync_values['Id'],
            self.company_id.certificate_file,
            self.company_id.certificate_password)
        wsdl = "DIAN['wsdl']"

        try:
            response = post(
                wsdl,
                headers={'content-type': 'application/soap+xml;charset=utf-8'},
                data=etree.tostring(xml_soap_with_signature))

            if response.status_code == 200:
                root = etree.fromstring(response.text)
                return True
            elif response.status_code in (500, 503, 507):
                pass
            else:
                raise ValidationError(msg1 % (response.status_code, response.reason))

            return False
        except exceptions.RequestException as e:
            raise ValidationError(msg2 % (e))

        return False