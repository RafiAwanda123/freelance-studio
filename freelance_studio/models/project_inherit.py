from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_paid_custom = fields.Monetary(string="Sudah Dibayar", compute="_compute_invoice_payment_custom", store=True)
    payment_status_custom = fields.Selection([
        ('not_paid', 'Belum Bayar'),
        ('partial', 'Sebagian'),
        ('paid', 'Lunas')
    ], string="Status Lunas", compute="_compute_invoice_payment_custom", store=True)

    @api.depends('invoice_ids.payment_state', 'invoice_ids.amount_total')
    def _compute_invoice_payment_custom(self):
        for order in self:
            paid_amount = 0.0
            status = 'not_paid'
            invoices = order.invoice_ids.filtered(lambda x: x.state == 'posted' and x.move_type == 'out_invoice')
            for inv in invoices:
                if inv.payment_state in ['paid', 'in_payment', 'reversed']:
                    paid_amount += inv.amount_total
                    status = 'paid'
                elif inv.payment_state == 'partial':
                    paid_amount += (inv.amount_total - inv.amount_residual)
                    if status != 'paid':
                        status = 'partial'
            order.amount_paid_custom = paid_amount
            order.payment_status_custom = status

class ProjectProject(models.Model):
    _inherit = 'project.project'

    project_type = fields.Selection([
        ('ui_ux', 'UI/UX'),
        ('logo', 'Logo'),
        ('web', 'Web')
    ], string="Project Type")
    website_name = fields.Char(string="Website Name")
    base_price = fields.Float(string="Base Price")
    schedule_date = fields.Date(string="Schedule Date")
    override_limit = fields.Boolean(string="Paksa Jadwal (Bypass Limit)", default=False)
    sale_order_id = fields.Many2one('sale.order', string="Terkait SO")

    @api.constrains('schedule_date', 'override_limit')
    def _check_schedule_limit(self):
        for project in self:
            if not project.schedule_date:
                continue
            start_of_week = project.schedule_date - timedelta(days=project.schedule_date.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            domain = [
                ('schedule_date', '>=', start_of_week),
                ('schedule_date', '<=', end_of_week),
                ('id', '!=', project.id)
            ]
            count = self.search_count(domain)
            if count >= 4 and not project.override_limit:
                 raise ValidationError("Jadwal Penuh! Maksimal 4 project per minggu.")

class ProjectTask(models.Model):
    _inherit = 'project.task'

    revision_count = fields.Integer(string='Jumlah Revisi', default=0)
    final_price = fields.Float(string="Harga Akhir (Bila Revisi)")
    revision_note = fields.Char(string="Keterangan Tambahan")

    def write(self, vals):
        res = super(ProjectTask, self).write(vals)
        if 'stage_id' in vals:
            for task in self:
                new_stage = task.env['project.task.type'].browse(vals['stage_id'])
                stage_name = new_stage.name.lower() if new_stage.name else ''
                
                update_vals = {}
                today_date = fields.Date.context_today(task)
                cust_name = task.partner_id.name if task.partner_id else 'Klien'
                proj_name = task.project_id.name if task.project_id else 'Proyek'
                
                if stage_name == 'selesai':
                    if task.date_deadline:
                        deadline_date = fields.Date.to_date(task.date_deadline)
                        if today_date < deadline_date:
                            tag = task.env['project.tags'].search([('name', '=', 'Selesai Sebelum Deadline')], limit=1)
                            if not tag:
                                tag = task.env['project.tags'].create({'name': 'Selesai Sebelum Deadline', 'color': 10})
                            task.write({'tag_ids': [(4, tag.id)]})
                    
                    sale_order = task.project_id.sale_order_id

                    if sale_order and sale_order.state in ['draft', 'sent']:
                        if sale_order.order_line:
                            line = sale_order.order_line[0]
                            if task.final_price > 0 and task.final_price != line.price_unit:
                                line.price_unit = task.final_price
                                ket = task.revision_note if task.revision_note else "Penyesuaian biaya"
                                line.name = f"{line.name}\nTambahan revisi: {ket}"

                        sale_order.action_confirm()
                        try:
                            with task.env.cr.savepoint():
                                sale_order._create_invoices()
                        except Exception as e:
                            task.message_post(body="Note: Draf Invoice gagal dibuat otomatis.")

                    update_vals['name'] = f"Selesai {cust_name} dengan proyek {proj_name}"
                    update_vals['date_deadline'] = today_date
                    update_vals['state'] = '1_done'
                    
                elif stage_name == 'revisi':
                    new_rev_count = task.revision_count + 1
                    update_vals['revision_count'] = new_rev_count
                    update_vals['name'] = f"Revisi {new_rev_count} {cust_name} dengan proyek {proj_name}"
                    update_vals['state'] = '04_waiting_normal'
                    
                elif stage_name == 'selesai revisi':
                    update_vals['name'] = f"Selesai Revisi {task.revision_count} {cust_name} dengan proyek {proj_name}"
                    update_vals['date_deadline'] = today_date
                    update_vals['state'] = '1_done'
                
                elif stage_name in ['sedang dikerjakan', 'tugas baru']:
                    update_vals['state'] = '01_in_progress'
                    
                if update_vals:
                    super(ProjectTask, task).write(update_vals)
        return res

    def action_send_deadline_reminder(self):
        tomorrow = fields.Date.today() + timedelta(days=1)
        tasks = self.search([
            ('date_deadline', '=', tomorrow),
        ])
        template = self.env.ref('self_management_freelance.email_template_task_deadline_reminder')
        for task in tasks:
            if task.stage_id and task.stage_id.name != 'Selesai': 
                template.send_mail(task.id, force_send=True)
