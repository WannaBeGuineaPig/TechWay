from borb.pdf import Document, Page, PDF, FixedColumnWidthTable, SingleColumnLayout, TableCell, Paragraph, HexColor, Image, TrueTypeFont, Alignment
from decimal import Decimal
import os
from pathlib import Path

PATH_FILE_PDF = f'{os.path.dirname(__file__)}\check.pdf'

def create_check_order(address_shop: str, id_order, payment_method, date_ordering, list_data: list[dict]):
    def setting_table_cell(content):
        return TableCell(content, border_width=Decimal(0))
    
    def setting_paragraph(content):
        return Paragraph(content, font_size=Decimal(14), font=bahnschrift, horizontal_alignment=Alignment.CENTERED)
    
    document = Document()
    page = Page()
    main_layout = SingleColumnLayout(page)
    layout = FixedColumnWidthTable(14 + len(list_data), 1)
    layout_logo_text = FixedColumnWidthTable(1, 2, column_widths=[Decimal(200), Decimal(397.5)])
    document.add_page(page)
    
    bahnschrift = TrueTypeFont.true_type_font_from_file(Path(f'{os.path.dirname(__file__)}\\fonts\\bahnschrift.ttf'))
    righteous_regular = TrueTypeFont.true_type_font_from_file(Path(f'{os.path.dirname(__file__)}\\fonts\\righteous-regular.ttf'))
    
    layout_logo_text.add(TableCell(Image(Path(f'{os.path.dirname(__file__)}\\logo_company.png'), horizontal_alignment=Alignment.RIGHT), border_width=Decimal(0)))
    layout_logo_text.add(TableCell(Paragraph('TechWay', font_color=HexColor('FF9900'), font_size=Decimal(50), font=righteous_regular, text_alignment=Alignment.LEFT, padding_left=Decimal(5), padding_top=Decimal(5)), border_width=Decimal(0)))

    layout.add(TableCell(layout_logo_text, border_width=Decimal(0)))
    layout.add(setting_table_cell(setting_paragraph('ООО “TechWay”')))
    layout.add(setting_table_cell(setting_paragraph(address_shop)))
    layout.add(setting_table_cell(setting_paragraph(f'Документ на продажу №{id_order}')))
    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    layout.add(setting_table_cell(setting_paragraph('Чек *Заказ товара(-ов)*')))
    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    for item in range(len(list_data)):
        item_data = list_data[item]
        layout.add(setting_table_cell(Paragraph(f'{item + 1}.  {item_data["name"]} {item_data["price"]} ₽  *  {item_data["amount"]}  =  {item_data["price"] * item_data["amount"]} ₽', font=bahnschrift, horizontal_alignment=Alignment.CENTERED, margin_top=Decimal(15), font_size=Decimal(12))))

    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    layout.add(setting_table_cell(setting_paragraph(payment_method)))
    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    all_sum = 0
    for item in list_data:
        all_sum += item['price'] * item['amount']
    layout.add(setting_table_cell(setting_paragraph(f'ИТОГО К ОПЛАТЕ = {all_sum} ₽')))
    layout.add(setting_table_cell(setting_paragraph(f'ДАТА И ВРЕМЯ ЗАКАЗА: {date_ordering}')))
    layout.add(setting_table_cell(setting_paragraph('СПАСИБО ЗА ЗАКАЗ!')))
    main_layout.add(layout)
    
    with open(PATH_FILE_PDF, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, document)

    return PATH_FILE_PDF