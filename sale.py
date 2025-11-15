from datetime import timedelta

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    telefono = fields.Char(string="Teléfono", size=15)
    vehiculo = fields.Char(string="Vehículo", size=40)
    referencia = fields.Char(string="Referencia", size=30)
    recogido = fields.Char(string="Asistido", size=40)
    comentarios = fields.Text(string="Comentarios")
    remolque = fields.Many2one(
        comodel_name="product.category",
        string="Tipo de vehículo",
        ondelete="set null",
        help="Categoría del vehículo asociado al servicio",
    )
    categ_id = fields.Selection(
        selection=[
            ("Remolque", "Remolque"),
            ("Rep in Situ", "Rep in Situ"),
            ("Suplidos", "Suplidos"),
            ("Alquiler", "Alquiler"),
        ],
        string="Acción",
        default="Remolque",
    )
    mes = fields.Char(string="Mes", compute="_compute_mes", store=True)
    date_invoice = fields.Date(string="Fecha de servicio")

    @api.depends('date_order')
    def _compute_mes(self):
        for order in self:
            if order.date_order:
                user_dt = fields.Datetime.context_timestamp(order, order.date_order)
                order.mes = user_dt.strftime('%m')
            else:
                order.mes = False

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()

        if self.date_invoice:
            invoice_vals['invoice_date'] = self.date_invoice
        elif not invoice_vals.get('invoice_date') and self.date_order:
            invoice_vals['invoice_date'] = (self.date_order + timedelta(days=1)).date()

        invoice_vals.update({
            'telefono': self.telefono,
            'vehiculo': self.vehiculo,
            'recogido': self.recogido,
            'comentarios': self.comentarios,
            'categ_id': self.categ_id,
            'remolque': self.remolque.id,
            'total_original': self.amount_total,
            'pricelist_id': self.pricelist_id.id,
            'referencia': self.referencia,
            'matricula': self.client_order_ref,
        })

        if self.referencia and not invoice_vals.get('ref'):
            invoice_vals['ref'] = self.referencia

        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Complemento",
        store=True,
    )

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        if self.order_id and self.order_id.pricelist_id:
            self.pricelist_id = self.order_id.pricelist_id

    def _prepare_invoice_line(self, **optional_values):
        values = super()._prepare_invoice_line(**optional_values)
        if self.pricelist_id:
            values.setdefault('complemento', self.pricelist_id.id)
        return values
