from odoo import models, fields


class SaleOrderLineExtension(models.Model):
    _inherit = 'sale.order.line'

    product_image = fields.Binary(related='product_id.image_1920', store=False)