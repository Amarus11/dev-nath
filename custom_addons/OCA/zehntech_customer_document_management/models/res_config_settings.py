import logging
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date
from odoo import _

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
   
    def _update_cron_time(self):
        # Example: Find the cron job and update its execution time
        cron = self.env.ref('zehntech_customer_document_management.ir_cron_document_expiry_notification', raise_if_not_found=False)
        if cron:
            cron.write({'interval_number': 1, 'interval_type': 'days'})

    
    email_notification_time = fields.Datetime(
    string='Expiry Notification Date & Time',
  
    )

    @api.constrains('email_notification_time')
    def _check_email_notification_time_not_in_past(self):
        for record in self:
            if record.email_notification_time:
                now = fields.Datetime.now()
                if record.email_notification_time < now:
                    raise ValidationError(_("You cannot set a past date and time for expiry notifications."))

    
    # Define Unsplash API fields
    unsplash_access_key = fields.Char(
        string="Unsplash Access Key",
        config_parameter='zehntech_customer_document_management.unsplash_access_key',
        help="API access key for integrating Unsplash."
    )

    unsplash_app_id = fields.Char(
        string="Unsplash App ID",
        config_parameter='zehntech_customer_document_management.unsplash_app_id',
        
    )

    # Define notification settings
    notify_days_before_expiry = fields.Integer(
        string="Days Before Expiry Notification",
        config_parameter='zehntech_customer_document_management.notify_days_before_expiry',
        default=7,
       
    )

    notify_days_after_expiry = fields.Integer(
        string="Days After Expiry Notification",
        config_parameter='zehntech_customer_document_management.notify_days_after_expiry',
        default=1,
        
    )

    
    def set_values(self):
        """Save settings values and update cron job execution time dynamically."""
        super(ResConfigSettings, self).set_values()
        
        config_param = self.env['ir.config_parameter'].sudo()
        config_param.set_param('zehntech_customer_document_management.email_notification_time', str(self.email_notification_time or ''))

        # Update cron job timing only if email_notification_time is set
        if self.email_notification_time:
            cron = self.env.ref('zehntech_customer_document_management.cron_document_expiry_notification', raise_if_not_found=False)

            if cron:
                cron_time = fields.Datetime.to_datetime(self.email_notification_time)  # Convert to datetime
                cron.write({
                    'interval_number': 1,
                    'interval_type': 'days',
                    'nextcall': cron_time.strftime('%Y-%m-%d %H:%M:%S'),
                })

    @api.model
    def get_values(self):
        """Retrieve settings values."""
        res = super(ResConfigSettings, self).get_values()
        res.update(
            email_notification_time=self.env['ir.config_parameter'].sudo().get_param('zehntech_customer_document_management.email_notification_time')
        )
        return res


    # def set_values(self):
    #     """Save the settings and update cron execution time."""
    #     super(ResConfigSettings, self).set_values()

    #     # Save configuration parameters
    #     self.env['ir.config_parameter'].sudo().set_param(
    #         'zehntech_customer_document_management.cron_execution_time', self.cron_execution_time
    #     )

    #     # Convert stored cron execution time (HH:MM) to datetime
    #     cron_time_str = self.cron_execution_time or "15:20"  # Default if empty
    #     cron_hour, cron_minute = map(int, cron_time_str.split(":"))
    #     next_run = datetime.now().replace(hour=cron_hour, minute=cron_minute, second=0)

    #     # If the next execution time is in the past, schedule for the next day
    #     if next_run < datetime.now():
    #         next_run += timedelta(days=1)

    #     # Update the cron job's nextcall
    #     cron_job = self.env.ref('zehntech_customer_document_management.cron_document_expiry_notification', raise_if_not_found=False)
    #     if cron_job:
    #         cron_job.sudo().write({'nextcall': next_run})

    #     cron_time_str = self.cron_execution_time or "15:20"  # Default if empty
    #     cron_hour, cron_minute = map(int, cron_time_str.split(":"))
    #     now = datetime.now()
    #     next_run = now.replace(hour=cron_hour, minute=cron_minute, second=0, microsecond=0)

    #     # If the next execution time is in the past, schedule for the next day
    #     if next_run < now:
    #         next_run += timedelta(days=1)

    #     # Update the cron job's nextcall
    #     cron_job = self.env.ref('zehntech_customer_document_management.cron_document_expiry_notification', raise_if_not_found=False)
    #     if cron_job:
    #         cron_job.sudo().write({'nextcall': next_run, 'active': True})

# from odoo import models, fields



# class ResConfigSettings(models.TransientModel):
#     _inherit = 'res.config.settings'
    
    


#     cron_run_time = fields.Float(
#         string="Cron Job Run Time (24h Format)",
#         default=15.33,  # 3:20 PM Default
#         help="Set the time (in hours, e.g., 15.33 for 3:20 PM) when the document expiry cron job should run.",
#     )
    
#     cron_execution_time = fields.Char(
#         string="Expiry Notification Execution Time",
#         config_parameter="zehntech_customer_document_management.cron_execution_time",
#         default="15:20"  # Default to 3:20 PM
#     )

#     # Define Unsplash API fields
#     unsplash_access_key = fields.Char(
#         string="Unsplash Access Key",
#         config_parameter='zehntech_customer_document_management.unsplash_access_key'
#     )

#     unsplash_app_id = fields.Char(  # Ensure this field exists if referenced in views
#         string="Unsplash App ID",
#         config_parameter='zehntech_customer_document_management.unsplash_app_id'
#     )

#     # Define notification settings
#     notify_days_before_expiry = fields.Integer(
#         string="Days Before Expiry Notification",
#         config_parameter='zehntech_customer_document_management.notify_days_before_expiry',
#         default=7
#     )

#     notify_days_after_expiry = fields.Integer(
#         string="Days After Expiry Notification",
#         config_parameter='zehntech_customer_document_management.notify_days_after_expiry',
#         default=1
#     )
    
    
#     def set_values(self):
#         """ Save the cron run time setting and update cron next execution """
#         super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param(
#             'zehntech_customer_document_management.cron_run_time', self.cron_run_time
#         )
#         self.env['res.partner.document'].update_cron_time()



#     def set_values(self):
#         super(ResConfigSettings, self).set_values()
#         self.env['ir.config_parameter'].sudo().set_param('zehntech_customer_document_management.cron_run_time', self.cron_run_time)

    
    
    
    
    
 

   