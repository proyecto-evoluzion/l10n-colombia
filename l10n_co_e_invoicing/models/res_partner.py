# -*- coding: utf-8 -*-
# Copyright 2019 Joan Marín <Github@joanmarin>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
	_inherit = "res.partner"
	
	def _get_accounting_partner_party_values(self):
		msg1 = _("'%s' does not have a person type assigned")
		msg2 = _("'%s' does not have a state assigned")
		msg3 = _("'%s' does not have a country assigned")

		if not self.person_type:
			raise UserError(msg1 % self.name)

		if self.country_id:
			if self.country_id.code == 'CO' and not self.state_id:
				raise UserError(msg2 % self.name)
		else:
			raise UserError(msg3 % self.name)

		return {
			'AdditionalAccountID': self.person_type,
			'Name': self.name,
			'AddressID': self.zip_id.code or '',
			'AddressCityName': self.zip_id.city or '',
			'AddressPostalZone': self.zip_id.name or '',
			'AddressCountrySubentity': self.state_id.name or '',
			'AddressCountrySubentityCode': self.state_id.code,
			'AddressLine': self.street  or '',
			'CompanyIDschemeID': self.check_digit,
			'CompanyIDschemeName': self.document_type_id.code,
			'CompanyID': self.identification_document,
			'TaxLevelCode': self.property_account_position_id.tax_level_code_id.code,
			'TaxSchemeID': self.property_account_position_id.tax_scheme_id.code,
			'TaxSchemeName': self.property_account_position_id.tax_scheme_id.name,
			'CorporateRegistrationSchemeName': self.ref,
			'CountryIdentificationCode': self.country_id.code,
			'CountryName': self.country_id.name}

	def _get_tax_representative_party_values(self):
		return {
			'IDschemeID': self.check_digit,
			'IDschemeName': self.document_type_id.code,
			'ID': self.identification_document}
