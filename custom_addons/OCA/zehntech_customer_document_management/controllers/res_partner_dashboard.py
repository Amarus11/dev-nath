from odoo import http
from odoo.http import request

class PartnerDocumentDashboardController(http.Controller):
    @http.route('/res_partner_document_expiry_data', type='json', auth='user')
    def res_partner_document_expiry_data(self):
       if not request.env.user.has_group('base.group_system'):
           return {'error': 'Access Denied'}  # Restrict access for non-admins

       request.env['customer.document.dashboard'].calculate_expiry_data()
       data = request.env['customer.document.dashboard'].search_read([], ['name', 'count'])
       return data
    

