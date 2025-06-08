import os
from borb.pdf import Document, Page, PDF, FixedColumnWidthTable, TableCell, Paragraph, HexColor, Image, TrueTypeFont, Alignment, SingleColumnLayoutWithOverflow
from decimal import Decimal
from pathlib import Path

PATH_FILE_PDF = f'{os.path.dirname(__file__)}\\file.pdf'
BAHNSCHRIFT = TrueTypeFont.true_type_font_from_file(Path(f'{os.path.dirname(__file__)}\\fonts\\bahnschrift.ttf'))
RIGHTEOUS_REGULAR = TrueTypeFont.true_type_font_from_file(Path(f'{os.path.dirname(__file__)}\\fonts\\righteous-regular.ttf'))

def delete_pdf_file():
    if os.path.isfile(PATH_FILE_PDF):
        os.remove(PATH_FILE_PDF)

def create_check_order(id_order: str, address_shop: str, payment_method: str, date_ordering: str, list_data: list[dict]) -> str:
    def setting_table_cell(content):
        return TableCell(content, border_width=Decimal(0))
    
    def setting_paragraph(content):
        return Paragraph(content, font_size=Decimal(14), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED)
    
    document = Document()
    page = Page()
    main_layout = SingleColumnLayoutWithOverflow(page)
    layout = FixedColumnWidthTable(14 + len(list_data), 1)
    layout_logo_text = FixedColumnWidthTable(1, 2, column_widths=[Decimal(200), Decimal(397.5)])
    document.add_page(page)
    
    
    layout_logo_text.add(TableCell(Image(Path(f'{os.path.dirname(__file__)}\\logo_company.png'), horizontal_alignment=Alignment.RIGHT), border_width=Decimal(0)))
    layout_logo_text.add(TableCell(Paragraph('TechWay', font_color=HexColor('FF9900'), font_size=Decimal(50), font=RIGHTEOUS_REGULAR, text_alignment=Alignment.LEFT, padding_left=Decimal(5), padding_top=Decimal(5)), border_width=Decimal(0)))

    layout.add(TableCell(layout_logo_text, border_width=Decimal(0)))
    layout.add(setting_table_cell(setting_paragraph('ООО “TechWay”')))
    layout.add(setting_table_cell(setting_paragraph(address_shop)))
    layout.add(setting_table_cell(setting_paragraph(f'Документ на продажу №{id_order}')))
    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    layout.add(setting_table_cell(setting_paragraph('Чек *Заказ товара(-ов)*')))
    layout.add(setting_table_cell(setting_paragraph('-'*60)))
    for item in range(len(list_data)):
        item_data = list_data[item]
        layout.add(setting_table_cell(Paragraph(f'{item + 1}.  {item_data["name"]} {item_data["price"]} ₽  *  {item_data["amount"]}  =  {item_data["price"] * item_data["amount"]} ₽', font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, margin_top=Decimal(15), font_size=Decimal(12))))

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


def create_report(start_period: str, stop_period: str, all_sum: int, items_list: list[list]) -> str:
    def table_cell_for_report(content, background_color = None, column_span=1):
        return TableCell(content, background_color=background_color, column_span=column_span, padding_bottom=Decimal(5), padding_left=Decimal(5), padding_right=Decimal(5), padding_top=Decimal(5))
    
    def create_new_text(text):
        new_text = ''
        for i in range(len(text)):
            if i == 30: 
                new_text += '\n'
            
            new_text += text[i]

        return new_text

    document = Document()
    page = Page(1920, 1080)
    main_layout = SingleColumnLayoutWithOverflow(page)
    table_layout = FixedColumnWidthTable(number_of_rows=6 + len(items_list), number_of_columns=5, border_width=Decimal(0))
    document.add_page(page)
    
    table_layout.add(TableCell(Paragraph('Компания ООО “TechWay”', font_size=Decimal(15), font=BAHNSCHRIFT, horizontal_alignment=Alignment.RIGHT, vertical_alignment=Alignment.TOP), column_span=5, border_width=Decimal(0)))
    table_layout.add(TableCell(Paragraph('ОТЧЁТ О ЗАКАЗАХ', font_size=Decimal(32), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED), column_span=5, border_width=Decimal(0)))
    table_layout.add(TableCell(Paragraph(f'Начала периода: {start_period}', font_size=Decimal(20), font=BAHNSCHRIFT), column_span=5, border_width=Decimal(0)))
    table_layout.add(TableCell(Paragraph(f'Конец периода: {stop_period}', font_size=Decimal(20), font=BAHNSCHRIFT), column_span=5, border_width=Decimal(0), padding_bottom=Decimal(10)))

    table_layout.add(table_cell_for_report(Paragraph('Номер клиента', font_size=Decimal(16), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD')))
    table_layout.add(table_cell_for_report(Paragraph('Номер заказа', font_size=Decimal(16), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD')))
    table_layout.add(table_cell_for_report(Paragraph('Дата заказа', font_size=Decimal(16), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD')))
    table_layout.add(table_cell_for_report(Paragraph('Сумма заказа', font_size=Decimal(16), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD')))
    table_layout.add(table_cell_for_report(Paragraph('Тип оплаты', font_size=Decimal(16), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD')))

    for item in items_list:
        table_layout.add(TableCell(Paragraph(str(item[0]), font_size=Decimal(12), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('D9D9D9')))
        table_layout.add(TableCell(Paragraph(str(item[1]), font_size=Decimal(12), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('D9D9D9')))
        table_layout.add(TableCell(Paragraph(str(item[2]), font_size=Decimal(12), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('D9D9D9')))
        table_layout.add(TableCell(Paragraph(str(item[3]), font_size=Decimal(12), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('D9D9D9')))
        table_layout.add(TableCell(Paragraph(str(item[4]), font_size=Decimal(12), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('D9D9D9')))
    
    table_layout.add(table_cell_for_report(Paragraph('Итого', font_size=Decimal(16), font=BAHNSCHRIFT, horizontal_alignment=Alignment.LEFT, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD'), 3))

    table_layout.add(table_cell_for_report(Paragraph(create_new_text(str(all_sum)), font_size=Decimal(14), font=BAHNSCHRIFT, horizontal_alignment=Alignment.CENTERED, vertical_alignment=Alignment.MIDDLE), HexColor('F3FFCD')))

    table_layout.add(table_cell_for_report(Paragraph(''), HexColor('F3FFCD')))


    main_layout.add(table_layout)

    with open(PATH_FILE_PDF, "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, document)

    return PATH_FILE_PDF