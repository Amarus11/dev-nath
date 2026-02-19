from odoo import models, fields

class ResPartnerDocumentCategory(models.Model):
    _name = 'res.partner.document.category'
    _description = 'Document Category'
    
    name = fields.Char(string="Category Name", required=True)
    

    category_id = fields.Many2one('res.partner.document.category', string="Category")