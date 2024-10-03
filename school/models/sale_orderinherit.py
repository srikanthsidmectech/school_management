from odoo import models, fields


# sale order inherit model for accounting section
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field = fields.Char(string='Custom Field')
    bank_Name = fields.Char(string="Bank Name")
    bank_Account_number = fields.Char(string="Bank Account Number")
    bank_Branch = fields.Char(string="Bank Branch Name")
    bank_Ifsc_code = fields.Char(string="Bank Ifsc Code")

    def _prepare_invoice(self):
        values = super(SaleOrder, self)._prepare_invoice()
        values.update({
            'bank_Name': self.bank_Name,
            'bank_Account_number': self.bank_Account_number,
            'bank_Branch': self.bank_Branch,
            'bank_Ifsc_code': self.bank_Ifsc_code,
            # 'invoice_line_ids': [(0, 0, {'brand_id': self.order_line.brand_id.brand_name})]

        })
        return values


# sale order inline sections product brand view
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', string='Brand')

    def _prepare_invoice_line(self, **optional_values):
        # Call the super method with the optional values
        values = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        values.update({
            'brand_ids': self.brand_id.id,  # Use self.brand_id.id for Many2one
        })
        return values


class User_Payment_Terms(models.Model):
    _inherit = 'res.users'

    payment_term = fields.Char("payment terms")
