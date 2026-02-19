import logging

_logger = logging.getLogger(__name__)
from odoo import models, fields, api, http
from odoo.exceptions import ValidationError
from odoo.http import request
from datetime import date

from datetime import datetime, timedelta
 
class CustomerDocument(models.Model):
    _name = 'customer.document'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Customer Document'
 
    name = fields.Char(string="Document Name", required=True)
    expiry_date= fields.Date(string="Expiry Date", required=True, tracking=True)
    expiry_time = fields.Float(string="Expiry Time")  # Store HH.MM format for better precision
    notify_expiry = fields.Boolean(string="Notify on Expiry")
    document = fields.Binary(string="Document File")  # Add this field if missing
    
    partner_id = fields.Many2one("res.partner", string="Customer", required=True)
  
    category_id = fields.Many2one("customer.document.category", string="Category")
    tags = fields.Many2many('res.partner.category', string="Tags")
 
    is_expired = fields.Boolean(string="Expired", compute="_compute_is_expired", store=True)
    
    
    expiry_status = fields.Selection(
        [
            ('expired', 'Expired'),
            ('expiring_soon', 'Expiring Soon'),
            ('valid', 'Valid'),
            ('no_expiry', 'No Expiry Date')
        ],
        string="Status",
        compute="_compute_expiry_status",
        store=False
    )
    
    
   

    @api.depends('expiry_date')
    def _compute_expiry_status(self):
      today = date.today()
      for record in self:
        if record.expiry_date:
            if record.expiry_date < today:
                record.expiry_status = 'expired'
            elif today <= record.expiry_date <= today + timedelta(days=7):
                record.expiry_status = 'expiring_soon'
            else:
                record.expiry_status = 'valid'
        else:
            record.expiry_status = 'no_expiry'



    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = date.today()
        for record in self:
            record.is_expired = record.expiry_date and record.expiry_date <= today
     
    @api.model
    def update_expiry_status(self):
        """ Update expiry status for all documents daily """
        self.search([])._compute_is_expired()
        
        
        



    @api.model
    def _update_cron_time(self):
        """Update the cron job execution time based on the saved settings."""
        cron = self.env.ref("zehntech_customer_document_management.cron_document_expiry_notification", raise_if_not_found=False)
        if cron:
            config = self.env["ir.config_parameter"].sudo()
            cron_time = config.get_param("zehntech_customer_document_management.cron_execution_time", "15:20")

            try:
                hours, minutes = map(int, cron_time.split(":"))
                cron.write({
                    "nextcall": datetime.now().replace(hour=hours, minute=minutes, second=0).strftime('%Y-%m-%d %H:%M:%S')
                })
            except ValueError:
                pass  # Ignore errors if time format is incorrect








    @api.model
    def _update_cron_time(self):
        """Update the cron job execution time based on user-defined notification date & time."""
        cron = self.env.ref("zehntech_customer_document_management.cron_document_expiry_notification", raise_if_not_found=False)
        if not cron:
            _logger.error("Cron job not found: zehntech_customer_document_management.cron_document_expiry_notification")
            return

        # Fetch user-defined expiry notification time
        config = self.env["ir.config_parameter"].sudo()
        cron_time_str = config.get_param("zehntech_customer_document_management.email_notification_time", False)

        if not cron_time_str:
            _logger.warning("No expiry notification time set in settings.")
            return

        try:
            next_run = fields.Datetime.from_string(cron_time_str)

            # Ensure the next execution is in the future
            if next_run < datetime.now():
                next_run += timedelta(days=1)

            cron.sudo().write({"nextcall": next_run.strftime('%Y-%m-%d %H:%M:%S')})
            _logger.info(f"Cron job updated to run at {next_run}")

        except ValueError:
            _logger.error(f"Invalid date-time format for cron execution: {cron_time_str}")

