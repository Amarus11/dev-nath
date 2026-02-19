from odoo import models, fields, api

class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    
    # Add document type field
    document_type = fields.Selection(
        [('pdf', 'PDF'), 
         ('image', 'Image'),
         ('office', 'Office'),
         ('other', 'Other')],
        string='Document Type',
        compute='_compute_document_type',
        store=True
    )
    
    @api.depends('mimetype', 'name')
    def _compute_document_type(self):
        for attachment in self:
            if attachment.mimetype:
                if 'pdf' in attachment.mimetype:
                    attachment.document_type = 'pdf'
                elif 'image' in attachment.mimetype:
                    attachment.document_type = 'image'
                elif any(x in attachment.mimetype for x in ['word', 'excel', 'powerpoint']):
                    attachment.document_type = 'office'
                else:
                    attachment.document_type = 'other'
            else:
                # Fallback to file extension
                name = (attachment.name or '').lower()
                if name.endswith('.pdf'):
                    attachment.document_type = 'pdf'
                elif any(name.endswith(x) for x in ['.jpg', '.jpeg', '.png', '.gif']):
                    attachment.document_type = 'image'
                elif any(name.endswith(x) for x in ['.doc', '.docx', '.xls', '.xlsx']):
                    attachment.document_type = 'office'
                else:
                    attachment.document_type = 'other'