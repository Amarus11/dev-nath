from odoo import models, fields, api,_
from datetime import date, timedelta
from odoo.exceptions import ValidationError

class CustomerDocumentDashboard(models.Model):
    _name = 'customer.document.dashboard'
    _description ='Customer Document Dashboard'
    # _description = 'Customer Document Dashboard'

    name = fields.Char(string="Status")
    count = fields.Integer(string="Document Count")
    dashboard_title = fields.Char(string='Dashboard Title')

    # Dummy fields just for visual layout (not recommended for production)
    spacer = fields.Boolean(string='Spacer')
    space1 = fields.Boolean(string='Space1')
    space2 = fields.Boolean(string='Space2')
    space3 = fields.Boolean(string='Space3')
    expired_docs_count = fields.Integer("Expired Documents")
    not_expired_docs_count = fields.Integer("Not Expired Documents")
    total_docs_count = fields.Integer("Total Documents")
    
    # name = fields.Char(string=_("Status"))
    # count = fields.Integer(string=_("Document Count"))
    # expired_docs_count = fields.Integer(string=_("Expired Documents"))
    # not_expired_docs_count = fields.Integer(string=_("Not Expired Documents"))
    # total_docs_count = fields.Integer(string=_("Total Documents"))

    
    state = fields.Selection(
        selection=lambda self: [
            ('draft', _('Draft')),
            ('approved', _('Approved')),
            ('rejected', _('Rejected')),
        ],
        string='Status'
    )


    document_count = fields.Integer(string="Document Count")

    total_documents = fields.Integer("Total Documents", compute="_compute_document_counts")
    expired_documents = fields.Integer("Expired Documents", compute="_compute_document_counts")
    not_expired_documents = fields.Integer("Not Expired Documents", compute="_compute_document_counts")

    document_count_7_days = fields.Integer(
        string="Expiring Soon (Next 7 Days)", compute="_compute_document_count_7_days"
    )

    @api.depends('total_documents', 'expired_documents', 'not_expired_documents')
    def _compute_document_counts(self):
        """ Compute total, expired, and not expired documents """
        for record in self:
            record.total_documents = self.env["res.partner.document"].search_count([])
            record.expired_documents = self.env["res.partner.document"].search_count([("expiry_date", "<", date.today())])
            record.not_expired_documents = record.total_documents - record.expired_documents

    @api.depends('document_count_7_days')
    def _compute_document_count_7_days(self):
        """ Compute the count of documents expiring in the next 7 days """
        today = date.today()
        next_7_days = today + timedelta(days=7)

        for record in self:
            record.document_count_7_days = self.env["res.partner.document"].search_count([
                ('expiry_date', '>=', today),
                ('expiry_date', '<=', next_7_days)
            ])

    def action_open_expiring_soon_documents(self):
        """ Open tree view for documents expiring in the next 7 days """
        today = date.today()
        next_7_days = today + timedelta(days=7)

        return {
            'name': 'Expiring Soon (Next 7 Days)',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner.document',
            'view_mode': 'list,form',
            'domain': [('expiry_date', '>=', today), ('expiry_date', '<=', next_7_days)],
            'target': 'current',
        }
        
        
    @api.constrains('attachment', 'expiry_date')
    def _check_expiry_not_today(self):
        for record in self:
            if record.attachment and record.expiry_date == fields.Date.today():
                raise ValidationError(_("You cannot upload a document with today's expiry date. Please choose a future date."))
            
    @api.constrains('expiry_date')
    def _check_expiry_not_today(self):
        for record in self:
            if record.expiry_date == fields.Date.today():
                raise ValidationError(_("Expiry date cannot be today's date. Please choose a future date."))


    @api.model
    def calculate_expiry_data(self):
        """ Calculate the number of expired, not expired, total, and soon-to-expire documents """
        today = date.today()
        next_7_days = today + timedelta(days=7)

        expired_count = self.env['res.partner.document'].search_count([('expiry_date', '<', today)])
        not_expired_count = self.env['res.partner.document'].search_count([('expiry_date', '>=', today)])
        total_count = self.env['res.partner.document'].search_count([])
        expiring_soon_count = self.env['res.partner.document'].search_count([
            ('expiry_date', '>=', today),
            ('expiry_date', '<=', next_7_days)
        ])
        

        # Store values globally for easy access
        config = self.env['ir.config_parameter'].sudo()
        config.set_param('document_expired_count', expired_count)
        config.set_param('document_not_expired_count', not_expired_count)
        config.set_param('document_total_count', total_count)
        config.set_param('document_expiring_soon_count', expiring_soon_count)

        # Clear previous data with sudo() to bypass access restrictions
        self.sudo().search([]).unlink()

        # Create new records for dashboard display
        self.sudo().create([
            {
                'name':_('Document Summary'),
                'count': total_count,
                'expired_docs_count': expired_count,
                'not_expired_docs_count': not_expired_count,
                'total_docs_count': total_count
            },
            {
                'name':_('Outdated Records'),
                'count': expired_count,
                'expired_docs_count': expired_count,
                'not_expired_docs_count': not_expired_count
            },
            {
                'name':_('Valid Documents'),
                'count': not_expired_count,
                'expired_docs_count': expired_count,
                'not_expired_docs_count': not_expired_count
            },
            {
                'name':_('Expiring (Within 7 Days)'),
                'count': expiring_soon_count
            }
        ])








        # Create new records for the dashboard
        # self.sudo().create([
        #     {
        #         'name': self._get_translated_text("Document Summary"),
        #         'count': total_count,
        #         'expired_docs_count': expired_count,
        #         'not_expired_docs_count': not_expired_count,
        #         'total_docs_count': total_count
        #     },
        #     {
        #         'name': self._get_translated_text("Outdated Records"),
        #         'count': expired_count,
        #         'expired_docs_count': expired_count,
        #         'not_expired_docs_count': not_expired_count
        #     },
        #     {
        #         'name': self._get_translated_text("Valid Documents"),
        #         'count': not_expired_count,
        #         'expired_docs_count': expired_count,
        #         'not_expired_docs_count': not_expired_count
        #     },
        #     {
        #         'name': self._get_translated_text("Upcoming Expiry (Within 7 Days)"),
        #         'count': expiring_soon_count
        #     }
        # ])

    

    def action_refresh_dashboard(self):
        """ Manually trigger the update """
        self.calculate_expiry_data()

    def action_open_total_documents(self):
        """ Open tree view for all documents """
        return {
            'name': 'All Documents',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner.document',
            'view_mode': 'list,form',
            'domain': [],
            'target': 'current',
        }

    def action_open_expired_documents(self):
        """ Open tree view for expired documents """
        today = date.today()
        return {
            'name': 'Expired Documents',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner.document',
            'view_mode': 'list,form',
            'domain': [('expiry_date', '<', today)],
            'target': 'current',
        }

    def action_open_not_expired_documents(self):
        """ Open tree view for not expired documents """
        today = date.today()
        return {
            'name': 'Not Expired Documents',
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner.document',
            'view_mode': 'list,form',
            'domain': [('expiry_date', '>=', today)],
            'target': 'current',
        }



