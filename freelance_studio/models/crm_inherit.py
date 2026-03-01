from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    project_type = fields.Selection([
        ('ui_ux', 'UI/UX'),
        ('logo', 'Logo'),
        ('web', 'Web')
    ], string="Project Type")

    def write(self, vals):
        if 'stage_id' in vals:
            stage = self.env['crm.stage'].browse(vals['stage_id'])
            if stage.is_won:
                for lead in self:
                    if not lead.stage_id.is_won: 
                        lead._generate_freelance_project()
        return super(CrmLead, self).write(vals)

    def _generate_freelance_project(self):
        for lead in self:
            vals_so = {
                'partner_id': lead.partner_id.id,
                'user_id': lead.user_id.id,
                'team_id': lead.team_id.id,
                'origin': lead.name,
            }
            sale_order = self.env['sale.order'].create(vals_so)

            product = self.env['product.product'].search([('name', '=', 'Jasa')], limit=1)
            if not product:
                product = self.env['product.product'].create({'name': 'Jasa', 'type': 'service'})

            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': product.id,
                'name': "Proyek: " + (lead.name or ''),
                'price_unit': lead.expected_revenue,
            })

            vals_project = {
                'name': lead.name,
                'partner_id': lead.partner_id.id,
                'user_id': lead.user_id.id,
                'project_type': lead.project_type,
                'base_price': lead.expected_revenue,
                'sale_order_id': sale_order.id, # <--- INI KUNCI ANTI DOBELNYA
            }
            new_project = self.env['project.project'].create(vals_project)
            
            stage_names = ['Tugas Baru', 'Sedang Dikerjakan', 'Selesai', 'Revisi', 'Selesai Revisi']
            tugas_baru_id = False
            for i, name in enumerate(stage_names):
                stage = self.env['project.task.type'].search([('name', '=', name)], limit=1)
                if not stage:
                    stage = self.env['project.task.type'].create({
                        'name': name,
                        'sequence': i,
                    })
                stage.write({'project_ids': [(4, new_project.id)]})
                if name == 'Tugas Baru':
                    tugas_baru_id = stage.id

            vals_task = {
                'name': lead.name,
                'project_id': new_project.id,
                'partner_id': lead.partner_id.id,
                'user_ids': [(4, self.env.user.id)],
                'description': "Generated from CRM: " + (lead.name or ''),
                'stage_id': tugas_baru_id
            }
            self.env['project.task'].create(vals_task)

            lead.message_post(body="System: Project, Task, dan Draft Quotation berhasil dibuat! (Akan otomatis jadi Sales Order Hijau saat Task Selesai)")
