from odoo import models, fields

class ResPartnerDocumentTag(models.Model):
    _name = 'res.partner.document.tag'
    _description = 'Document Tag'

    name = fields.Char(string="Tag Name", required=True)



