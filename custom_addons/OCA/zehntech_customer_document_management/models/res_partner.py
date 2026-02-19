from odoo import models, fields,api, _
class ResPartner(models.Model):
    _inherit = 'res.partner'

    document_ids = fields.One2many(
        comodel_name='res.partner.document',
        inverse_name='partner_id',
        string='Documents'
    )


