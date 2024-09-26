# from odoo import models, fields, api
#
#
# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     customer_name = fields.Char(string='Parent Name')
#     customer_ph_no = fields.Char(string='parent mobile No')
#
#     student_id=fields.Many2one('school.student',string="student")
#
#     bank_Name = fields.Char(string="Bank Name")
#     bank_Account_number = fields.Char(string="Bank Account Number")
#     bank_Branch = fields.Char(string="Bank Branch Name")
#     bank_Ifsc_code = fields.Char(string="Bank Ifsc Code")
#
#
#
#
# class AccountMoveLine(models.Model):
#     _inherit = 'account.move.line'
#
#     fee_structure_ids = fields.Many2one(
#         'school.fee.structure',
#         string='Fee Structure'
#     )
#
# #

from odoo import models
import base64
import tempfile
import re

class PartnerXlsx(models.AbstractModel):
    _name = 'report.school.report_partner_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.hide_gridlines(2)  # 2 means hide gridlines

            # Define a border format
            border_format = workbook.add_format({'border': 1, 'align': 'center' })
            # partner_name = obj.partner_id.name #partner name
            # bold = workbook.add_format({'bold': True})
            # sheet.write(0, 0, partner_name, bold) #sheet partner name at row 0 , col 0
            header_format = workbook.add_format({
                'bg_color': '#1D66B8',
                'font_color': 'white',
                'bold': True,
                # 'align': 'center',
                # 'valign': 'vcenter'
            })

            h_b_format = workbook.add_format({
                'bg_color': '#1D66B8',
                'font_color': 'white',
                'bold': True,
                'border': 1,
                'align': 'center',
                # 'valign': 'vcenter'
            })

            company_logo = obj.company_id.logo
            if company_logo:
                # Decode the base64 image
                logo_data = base64.b64decode(company_logo)
                # Create a temporary file to save the logo
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_logo_file:
                    temp_logo_file.write(logo_data)
                    temp_logo_file_path = temp_logo_file.name
                    # Define the desired height and width in Excel's units (1 unit = 1/72 inches)
                height = 60
                width = 60

                # Insert the logo into the worksheet with specific dimensions
                sheet.insert_image(0, 0, temp_logo_file_path, {'x_scale': width / 100, 'y_scale': height / 100})

            company_name = obj.company_id.name
            # company_street=obj.company_id.stree2.id
            company_ciy = obj.company_id.city
            company_stree2 = obj.company_id.street
            company_zip = obj.company_id.zip
            company_state = obj.company_id.state_id.name
            company_country = obj.company_id.country_id.name

            sheet.merge_range('A8:D8', company_name)
            # sheet.write(7,0,company_street)
            sheet.merge_range('A9:D9', f"{company_ciy},{company_stree2}")
            sheet.merge_range('A10:D10', f"{company_zip},{company_state},{company_country}")

            sheet.merge_range('K2:N3', f"QUOTATION",workbook.add_format({'bold':True,'font_size': 20,'align':'center',}))
            sheet.write(7,10, f"Date:")
            sheet.merge_range('L8:N8', f"{obj.invoice_date.strftime('%d %B, %Y')}")

            sheet.merge_range('A13:D13', f"INVOICE ADDRESS", h_b_format)
            sheet.merge_range('A14:D14', f"{obj.partner_id.city},{obj.partner_id.street}")
            sheet.merge_range('A15:D15', f"{obj.partner_id.state_id.name},{obj.partner_id.country_id.name}")
            sheet.merge_range('A16:D16', f"{obj.partner_id.zip}")

            sheet.merge_range('K13:N13', f"SHIPPING ADDRESS", h_b_format)
            sheet.merge_range('K14:N14', f"{obj.partner_id.city},{obj.partner_id.street}")
            sheet.merge_range('K15:N15', f"{obj.partner_id.state_id.name},{obj.partner_id.country_id.name}")
            sheet.merge_range('K16:N16', f"{obj.partner_id.zip}")

            sheet.merge_range('A20:B20', "SALES PERSON", h_b_format)
            sheet.merge_range('C20:E20', f"SHIPPING METHOD", h_b_format)
            sheet.merge_range('F20:H20', f"SHIPPING TERMS", h_b_format)
            sheet.merge_range('I20:J20', f"PAYMENT TERMS", h_b_format)
            sheet.merge_range('K20:L20', f"DUE DATE", h_b_format)
            sheet.merge_range('M20:N20', f"DELIVERY DATE", h_b_format)

            sheet.merge_range('A21:B21', f"{obj.invoice_user_id.name}", border_format)
            sheet.merge_range('C21:E21', f"", border_format)
            sheet.merge_range('F21:H21', f"", border_format)
            sheet.merge_range('I21:J21', f"{obj.invoice_payment_term_id.name}", border_format)
            sheet.merge_range('K21:L21', f"{obj.invoice_date_due}", border_format)
            sheet.merge_range('M21:N21', f"{obj.delivery_date}", border_format)

            sheet.merge_range('A24:F24', f"DESCRIPTION", h_b_format)
            sheet.merge_range('G24:I24', f"UNIT PRICE", h_b_format)
            sheet.merge_range('J24:K24', f"QTY", h_b_format)
            sheet.merge_range('L24:N24', f"AMOUNT", h_b_format)
            start_row = 24

            # Iterate through each invoice line item
            for line in obj.invoice_line_ids:
                # product_name=line.name.split(',')
                # product_names=""
                # if len(product_name)>1:
                #     for product in product_name:
                #         product_names+="\n"+ "*"+product
                # else:
                #     product_names=product_name[0]
                sheet.merge_range(start_row, 0, start_row, 5, line.name, workbook.add_format({'border': 1, 'text_wrap': True}))  # Write DESCRIPTION in column A
                sheet.merge_range(start_row, 6, start_row, 8, f"{obj.currency_id.symbol} {line.price_unit}",
                                  border_format)  # Write UNIT PRICE in column G
                sheet.merge_range(start_row, 9, start_row, 10, line.quantity, border_format)  # Write QTY in column I
                sheet.merge_range(start_row, 11, start_row, 13, f"{obj.currency_id.symbol} {line.price_total}",
                                  border_format)  # Write AMOUNT in column K

                # Move to the next row for the next invoice line
                start_row += 1

            # Write additional information after all products
            start_row += 1
            sheet.merge_range(start_row, 0, start_row, 6, "Special Notes and Instructions", h_b_format)
            if obj.narration:
                # First, find and split based on closing tags
                # closing_tags = re.findall(r'</[^>]+>', obj.narration)  # Find closing tags
                narration_lines = re.split(r'</[^>]+>', obj.narration)  # Split at closing tags

                # Clean each line and prepare for writing to the sheet
                cleaned_lines = [re.sub(r'<.*?>', '', line).strip() for line in narration_lines]

                # Write each cleaned line to a new row in the sheet
                for i, line in enumerate(cleaned_lines):
                    # Calculate the current row index
                    current_row = start_row + 1 + i

                    # Only write non-empty lines
                    if line:
                        sheet.merge_range(current_row, 0, current_row, 6, line, workbook.add_format({'border': 1, 'align': 'left' }))

            # Add borders to the entire range

            sheet.merge_range(start_row, 10, start_row, 11, "UNTAXED AMOUNT", border_format)
            sheet.merge_range(start_row, 12, start_row, 13, f"{obj.currency_id.symbol} {obj.amount_untaxed}", border_format)

            # Move to the next row after notes
            start_row += 1

            # Assuming tax_totals is populated correctly
            tax_groups = obj.tax_totals['groups_by_subtotal'].get('Untaxed Amount', [])

            if isinstance(tax_groups, list) and len(tax_groups) > 0:
                sheet.merge_range(start_row, 10, start_row, 11, tax_groups[0]['tax_group_name'], border_format)
                sheet.merge_range(start_row, 12, start_row, 13, tax_groups[0]['formatted_tax_group_amount'],
                                  border_format)
                start_row += 1
                sheet.merge_range(start_row, 10, start_row, 11, tax_groups[1]['tax_group_name'], border_format)
                sheet.merge_range(start_row, 12, start_row, 13, tax_groups[1]['formatted_tax_group_amount'],
                                  border_format)
            else:
                sheet.merge_range(start_row, 10, start_row, 11, "No tax group", border_format)
                sheet.merge_range(start_row, 12, start_row, 13, "0", border_format)

            # Move to the next row for total amount
            start_row += 2  # Adjust for spacing
            sheet.merge_range(start_row, 10, start_row, 11, "TOTAL AMOUNT", border_format)
            sheet.merge_range(start_row, 12, start_row, 13, f"{obj.currency_id.symbol} {obj.amount_total}",
                              border_format)

            # Move to the next row for thank you message
            start_row += 3  # Adjust for spacing
            sheet.write(f"F{start_row}:L{start_row}", "THANK YOU FOR BUSINESS!",workbook.add_format({'bold':True}))
            sheet.merge_range(f"C{start_row+1}:M{start_row+1}",f"Should you have any enquiries concerning this quotation, please contact {obj.invoice_user_id.name} on {obj.invoice_user_id.mobile}")
            sheet.merge_range(f"C{start_row+2}:N{start_row+2}",f"{obj.company_id.street2},{obj.company_id.city},{obj.company_id.name},{obj.company_id.street},{obj.company_id.zip},{obj.company_id.state_id.name},{obj.company_id.country_id.name}")
            sheet.merge_range(f"C{start_row+3}:N{start_row+3}",f"E-mail: {obj.company_id.email},Mobile no:{obj.company_id.mobile},Website:{obj.company_id.website}")

