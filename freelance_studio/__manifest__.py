{
    'name': 'Management Freelance',
    'version': '18.0.1.0.0',
    'category': 'Services/Project',
    'summary': 'Integrated ERP for Freelance Designers',
    'website': 'https://rafi-awanda-portofolio.vercel.app/',
    'description': """
        Freelance Management System including:
        - CRM Deal Trigger
        - Project Capacity Management
        - Automated Deadline Reminders
        - Integrated Menus for Sales, Project, Accounting, and Analytics
    """,
    'author': 'Rafi Awanda',
    'depends': ['base', 'crm', 'sale_management', 'project', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/invoice_report_template.xml',
        'data/email_templates.xml',
        'data/cron_jobs.xml',
        'views/freelance_menus.xml',
        'views/project_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
