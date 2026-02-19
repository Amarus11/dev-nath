from odoo import models, fields
class SignatureWizard(models.TransientModel):
    _name = 'customer.document.signature.wizard'
    _description = 'Customer Document Signature Wizard'

    signature = fields.Binary(string="Signature", attachment=True)

    def save_signature(self):
        document_id = self.env.context.get('active_id')
        if document_id:
            document = self.env['res.partner.document'].browse(document_id)
            document.signature = self.signature
        return {'type': 'ir.actions.act_window_close'}
