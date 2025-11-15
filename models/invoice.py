from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    telefono = fields.Char(string="Teléfono", size=15, copy=True)
    matricula = fields.Char(string="Matrícula", size=15, copy=True)
    total_original = fields.Float(string="Total servicio original", copy=True)
    vehiculo = fields.Char(string="Vehículo", size=40, copy=True)
    referencia = fields.Char(string="Referencia", size=30, copy=True)
    recogido = fields.Char(string="Asistido", size=40, copy=True)
    comentarios = fields.Text(string="Comentarios", copy=True)
    categ_id = fields.Selection(
        selection=[
            ("Remolque", "Remolque"),
            ("Rep in Situ", "Rep in Situ"),
            ("Suplidos", "Suplidos"),
            ("Alquiler", "Alquiler"),
        ],
        string="Acción",
        copy=True,
    )
    remolque = fields.Many2one(
        comodel_name="product.category",
        string="Tipo de vehículo",
        ondelete="set null",
        help="Selecciona la categoría de vehículo asociada.",
        copy=True,
    )
    pricelist_id = fields.Many2one(
        comodel_name="product.pricelist",
        string="Complemento",
        help="Lista de precios aplicada en el pedido de origen.",
        copy=True,
    )

    @api.onchange('partner_id', 'company_id', 'move_type')
    def _onchange_partner_id(self):
        result = super()._onchange_partner_id()
        if self.partner_id and self.move_type in ('out_invoice', 'out_refund') and self.partner_id.journal_id:
            self.journal_id = self.partner_id.journal_id
        return result

    def _reverse_move_vals(self, default_values=None, cancel=False):
        values_list = super()._reverse_move_vals(default_values=default_values, cancel=cancel)
        for vals in values_list:
            vals.update({
                'telefono': self.telefono,
                'matricula': self.matricula,
                'total_original': self.total_original,
                'vehiculo': self.vehiculo,
                'referencia': self.referencia,
                'recogido': self.recogido,
                'comentarios': self.comentarios,
                'categ_id': self.categ_id,
                'remolque': self.remolque.id,
                'pricelist_id': self.pricelist_id.id,
            })
        return values_list


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    complemento = fields.Many2one(
        comodel_name="product.pricelist",
        string="Complemento",
        copy=True,
        ondelete="set null",
        store=True,
    )

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        if self.move_id and self.move_id.pricelist_id:
            self.complemento = self.move_id.pricelist_id
