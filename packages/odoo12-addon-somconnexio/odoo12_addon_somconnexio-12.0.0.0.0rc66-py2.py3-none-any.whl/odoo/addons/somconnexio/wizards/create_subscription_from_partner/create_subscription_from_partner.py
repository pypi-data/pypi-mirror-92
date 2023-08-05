from odoo import _, api, models, fields
from odoo.exceptions import UserError


class PartnerCreateSubscription(models.TransientModel):
    _inherit = "partner.create.subscription"
    bank_id = fields.Many2one('res.partner.bank', 'Bank Account', required=True)
    payment_type = fields.Selection([
        ('single', 'One single payment'),
        ('split', 'Ten payments')
    ], required=True)

    @api.multi
    def create_subscription(self):
        sub_req = self.env["subscription.request"]
        partner_obj = self.env["res.partner"]

        cooperator = self.cooperator
        vals = {
            "partner_id": cooperator.id,
            "share_product_id": self.share_product.id,
            "ordered_parts": self.share_qty,
            "cooperator": True,
            "user_id": self.env.uid,
            "email": self.email,
            "source": "crm",
            "address": self.cooperator.street,
            "zip_code": self.cooperator.zip,
            "city": self.cooperator.city,
            "country_id": self.cooperator.country_id.id,
            "lang": self.cooperator.lang,
        }

        if self.is_company:
            vals["company_name"] = cooperator.name
            vals["company_email"] = cooperator.email
            vals["name"] = "/"
            vals["company_register_number"] = self.register_number
            vals["is_company"] = True
        else:
            vals["name"] = cooperator.name
            vals["firstname"] = cooperator.firstname
            vals["lastname"] = cooperator.lastname

        coop_vals = {}
        if not self._get_email():
            coop_vals["email"] = self.email

        if not self._get_register_number():
            if self.is_company:
                coop_vals["company_register_number"] = self.register_number

        if self.is_company and not self._get_representative():
            representative = False
            if self.representative_email:
                representative = partner_obj.search(
                    [("email", "=", self.representative_email)]
                )

            if representative:
                if len(representative) > 1:
                    raise UserError(
                        _(
                            "There is two different persons with "
                            "the same national register number. "
                            "Please proceed to a merge before to "
                            "continue"
                        )
                    )
                if representative.parent_id:
                    raise UserError(
                        _(
                            "A person can't be representative of "
                            "two different companies."
                        )
                    )
                representative.parent_id = cooperator.id
            else:
                if self.representative_email:
                    represent_vals = {
                        "name": self.representative_name,
                        "cooperator": True,
                        "email": self.representative_email,
                        "parent_id": cooperator.id,
                        "representative": True,
                    }
                    partner_obj.create(represent_vals)

        vals["iban"] = self.bank_id.acc_number
        vals["payment_type"] = self.payment_type
        if self.is_company:
            representative = self._get_representative()
            vals["name"] = representative.name

        if coop_vals:
            cooperator.write(coop_vals)

        new_sub_req = sub_req.create(vals)

        return {
            "type": "ir.actions.act_window",
            "view_type": "form, tree",
            "view_mode": "form",
            "res_model": "subscription.request",
            "res_id": new_sub_req.id,
            "target": "current",
        }
