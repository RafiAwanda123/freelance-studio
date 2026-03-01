from odoo import http
from odoo.http import request

class FreelanceController(http.Controller):

    @http.route(['/freelance/download/invoice/<int:invoice_id>'], type='http', auth='user')
    def download_invoice(self, invoice_id, **kw):
    
        invoice = request.env['account.move'].browse(invoice_id)
        
    
        if not invoice.exists():
            return request.not_found()

        pdf_content, _ = request.env['ir.actions.report']._render_qweb_pdf('self_management_freelance.report_freelance_invoice', [invoice_id])

        pdfheader = [
            ('Content-Type', 'application/pdf'),
            ('Content-Length', len(pdf_content)),
            ('Content-Disposition', f'attachment; filename="Invoice_{invoice.name}.pdf"')
        ]
        
        return request.make_response(pdf_content, headers=pdfheader)
