from odoo import models, exceptions, _


class PrintXlsxParser(models.AbstractModel):
    _name = 'report.query_deluxe_xlsx.xlsx_layout'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Query Deluxe xlsx parser'

    def get_datas(self, doc):
        headers, bodies = self.env['querydeluxe'].get_result_from_query(doc.name)
        return headers, bodies

    def generate_xlsx_report(self, workbook, data, queries):
        self = self.sudo()

        bold = workbook.add_format({"bold": True})
        grey_format = workbook.add_format({"bg_color": '#D3D3D3'})
        white_format = workbook.add_format({"bg_color": 'white'})

        for query in queries:
            headers, bodies = self.get_datas(query)

            sheet = workbook.add_worksheet(str(query.name or ''))
            col = 0
            for header in headers:
                sheet.write(0, col, str(header), bold)
                col += 1
            row = 1
            for body in bodies:
                line_format = grey_format if row % 2 == 0 else white_format
                col = 0
                for value in body:
                    display_value = ''
                    if value is not None:
                        display_value = str(value)
                    sheet.write(row, col, display_value, line_format)
                    col += 1
                row += 1
