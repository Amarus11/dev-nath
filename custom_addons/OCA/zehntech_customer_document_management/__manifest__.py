{
    "name": "Customer Document Management",
    "description": """ Customer Document Management helps you manage customer documents efficiently. It allows multiple documents uploads, sends automatic email reminders before, after, and on the expiry date, and provides real-time dashboards for document status. Documents can be organized using tags and categories, making them easy to find. With role-based access, admins have full control while customers can only access their own documents.""",
    "summary": """Odoo module for multi-document upload, expiry alerts, analytics dashboards, secure role-based access, and document organization.""",
    "version": '18.0.1.0.0',
    "category": "Document Management",
    "author": "Zehntech Technologies Inc.",
    "company": "Zehntech Technologies Inc.",
    "maintainer": "Zehntech Technologies Inc.",
    "contributor": "Zehntech Technologies Inc.",
    "website": "https://www.zehntech.com/",
    "support": "odoo-support@zehntech.com",
    "images": ["static/description/banner.png"],
    "depends": ['base', 'contacts','web'],
    "data": [
        "security/ir.model.access.csv",
        "security/res_partner_document_rules.xml",
        "data/email_templates.xml",
        "data/cron_jobs.xml",
        "views/res_config_settings_view.xml",
        "views/customer_document_dashboard.xml",
        "views/dashboard_menu.xml",
        "views/res_partner_document_views.xml",
        "views/document_dashboard_piechart.xml",
        "views/res_partner_document_search.xml",
        "views/customer_document_views.xml",
        "views/res_partner_views.xml",
       
    ],
    'assets': {
        'web.assets_backend': [
            'zehntech_customer_document_management/static/src/css/status.css'
            
        ],
    },
    'i18n': [
            'i18n/es.po',
            'i18n/fr.po',
            'i18n/de.po',
            'i18n/ja.po',
    ],
 
    "license": "OPL-1",
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 00.00,
    "currency": "USD"
}
