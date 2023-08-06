from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)
try:
    from stdnum.es.nie import is_valid as valid_nie
except (ImportError, IOError) as err:
    _logger.debug(err)


class SubscriptionRequest(models.Model):
    _inherit = 'subscription.request'

    iban = fields.Char(required=True)

    type = fields.Selection(
        selection_add=[(
            'sponsorship_coop_agreement',
            'Sponsorship Coop Agreement'
        )])

    coop_agreement_id = fields.Many2one(
        'coop.agreement',
        string='Coop Agreement'
    )
    nationality = fields.Many2one('res.country', 'Nationality')

    payment_type = fields.Selection([
        ('single', 'One single payment'),
        ('split', 'Ten payments')
    ])

    state_id = fields.Many2one('res.country.state', 'Province')
    discovery_channel_id = fields.Many2one('discovery.channel', 'Discovery Channel')

    verbose_name = fields.Char(compute='_get_verbose_name', store=True)
    _rec_name = 'verbose_name'

    @api.depends('firstname', 'lastname', 'type', 'company_name')
    def _get_verbose_name(self):
        for sr in self:
            if sr.is_company:
                sr.verbose_name = f'{sr.company_name} - {sr.type}'
            else:
                sr.verbose_name = "{} {} - {}".format(
                    sr.firstname, sr.lastname, sr.type
                )

    def get_journal(self):
        # Redefine the get_journal of EMC to get the SUBJ journal:
        # https://github.com/coopiteasy/vertical-cooperative/blob/12.0/easy_my_coop/models/coop.py#L522  # noqa
        return self.env.ref('somconnexio.subscription_journal')

    def get_partner_company_vals(self):
        values = super().get_partner_company_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id
        values["vat"] = self.get_vat()
        values["state_id"] = self.state_id.id
        values["phone"] = self.phone
        values["email"] = self.email
        return values

    def get_partner_vals(self):
        values = super().get_partner_vals()
        values['coop_agreement_id'] = self.coop_agreement_id and \
            self.coop_agreement_id.id
        values["vat"] = self.get_vat()
        values["nationality"] = self.nationality.id
        values["state_id"] = self.state_id.id
        return values

    @api.one
    def vinculate_partner_in_lead(self):
        leads = self.env['crm.lead'].search([
            ('subscription_request_id', '=', self.id)
        ])
        for lead in leads:
            lead.partner_id = self.partner_id

    @api.one
    def validate_subscription_request(self):
        try:
            invoice = super().validate_subscription_request()
        except UserError:
            if self.ordered_parts == 0 and self.type == 'sponsorship_coop_agreement':
                pass
            else:
                raise
        else:
            self.vinculate_partner_in_lead()
            return invoice

        self.partner_obj = self.env['res.partner']

        self._check_already_cooperator()

        if not self.partner:
            self.partner = self.create_coop_partner()
        else:
            self.partner = self.partner[0]

        self.partner_id = self.partner
        self.partner.nationality = self.nationality
        self.partner.state_id = self.state_id

        self.partner.cooperator = True

        self._create_company_contact()

        self.write({'state': 'done'})
        self.vinculate_partner_in_lead()
        return True

    @api.one
    @api.constrains('coop_agreement_id', 'type')
    def _check_coop_agreement_id(self):
        if self.type == 'sponsorship_coop_agreement' and not self.coop_agreement_id:
            raise ValidationError(
                "If it's a Coop Agreement sponsorship the Coop Agreement must be set."
            )

    @api.one
    @api.constrains('vat', 'nationality')
    def _check_nie_nationality(self):
        if valid_nie(self.vat) and not self.nationality:
            raise ValidationError('If a NIE is provided, nationality is mandatory.')

    def get_invoice_vals(self, partner):
        invoice_vals = super().get_invoice_vals(partner)
        if self.payment_type == 'split':
            invoice_vals['payment_term_id'] = self.env.ref(
                'somconnexio.account_payment_term_10months'
            ).id
        invoice_vals['payment_mode_id'] = self.env.ref(
            'somconnexio.payment_mode_inbound_sepa'
        ).id
        return invoice_vals

    def get_vat(self):
        if self.vat[:2] == 'ES':
            return self.vat
        return "ES{}".format(self.vat)

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    @api.model
    def create(self, vals):
        partner_obj = self.env["res.partner"]

        if not vals.get("partner_id"):
            cooperator = False
            if vals.get("email"):
                cooperator = partner_obj.get_cooperator_from_email(
                    vals.get("email")
                )
            if cooperator:
                # TODO remove the following line once it has
                # been found a way to avoid double encoding
                cooperator = cooperator[0]
                vals["type"] = "subscription"
                vals = self.is_member(vals, cooperator)
                vals["partner_id"] = cooperator.id
        else:
            cooperator_id = vals.get("partner_id")
            cooperator = partner_obj.browse(cooperator_id)
            vals = self.is_member(vals, cooperator)

        if not cooperator.cooperator:
            cooperator.write({"cooperator": True})
        subscr_request = super(models.Model, self).create(vals)

        if self._send_confirmation_email():
            mail_template_notif = subscr_request.get_mail_template_notif(False)
            mail_template_notif.send_mail(subscr_request.id)

        return subscr_request

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    @api.model
    def create_comp_sub_req(self, vals):
        vals["name"] = vals["company_name"]
        if not vals.get("partner_id"):
            cooperator = self.env["res.partner"].get_cooperator_from_crn(
                vals.get("company_register_number")
            )
            if cooperator:
                vals["partner_id"] = cooperator.id
                vals["type"] = "increase"
                vals["already_cooperator"] = True
        subscr_request = super(models.Model, self).create(vals)

        if self._send_confirmation_email():
            confirmation_mail_template = subscr_request.get_mail_template_notif(
                True
            )
            confirmation_mail_template.send_mail(subscr_request.id)

        return subscr_request

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    def _send_confirmation_email(self):
        return self.company_id.send_confirmation_email

    # TODO: Remove this code when a release of EasyMyCoop with:
    # https://github.com/coopiteasy/vertical-cooperative/pull/146
    def send_capital_release_request(self, invoice):
        email_template = self.get_capital_release_mail_template()

        if self.company_id.send_capital_release_email:
            # we send the email with the capital release request in attachment
            # TODO remove sudo() and give necessary access right
            email_template.sudo().send_mail(invoice.id, True)
            invoice.sent = True
