from odoo import api, fields, models, exceptions
from random import randint
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = "sale.order"
    x_test = fields.Text(string="Test", default=randint(1, 100))

    @api.onchange('date_order', 'tax_totals_json')
    def _test__update(self):
        if self.amount_total \
                or (abs(datetime.now() - self.date_order) > timedelta(seconds=1)):
            date = fields.Datetime.context_timestamp(self, self.date_order)
            self.x_test = f'{format(self.amount_total, ".2f")} - {date.strftime("%d/%m/%Y %H:%M:%S")}'

    @api.model
    def create(self, vals):
        self._test__length_control(vals)
        return super().create(vals)

    def write(self, vals):
        self._test__length_control(vals)
        return super().write(vals)

    @staticmethod
    def _test__length_control(vals):
        if len(vals['x_test']) > 50:
            raise exceptions.ValidationError("Длина текста должна быть меньше 50 символов!")
    # test
    # 123456789-123456789-123456789-123456789-123456789

    # @api.onchange('x_test')
    # def _test__length_control(self):
    #     if len(self.x_test) > 50:
    #         return {
    #             'warning': {'title': "Warning",
    #                         'message': "Длина текста должна быть меньше 50 символов!",
    #                         # 'type': 'notification',
    #                         },
    #         }

    # Поле исчезает, если оно пустое
    # x_hide = fields.Boolean(string="Hide", compute="_set_hide", store=False)
    # @api.depends('x_test')
    # def _set_hide(self):
    #     self.x_hide = bool(self.x_test)



