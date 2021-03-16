import pandas as pd
import numpy as np
import os
import PyPDF2
import pdfrw
import json
from src.CustomFunctions.customFunctions import trigger_rule
from src.utils import is_in_array, slice_dict


#PDF constants
ANNOT_KEY = '/Annots'           # key for all annotations within a page
ANNOT_FIELD_KEY = '/T'          # Name of field. i.e. given ID of field
ANNOT_FORM_type = '/FT'         # Form type (e.g. text/button)
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
ANNOT_FORM_button = '/Btn'      # ID for buttons, i.e. a checkbox
ANNOT_FORM_text = '/Tx'         # ID for textbox

#Other constants
EXCEL_OUTPUT_NAME = 'output.xlsx'
PATH_SEPARATOR = os.sep
OUTPUT_FOLDER = 'Output'
PDF_TEMPLATE_PATH = f'Template{PATH_SEPARATOR}ssp1-interactive.pdf'


def read_input():
    path = f'{os.getcwd()}{PATH_SEPARATOR}Input'
    files = os.listdir(path)
    cols = get_cols('xl')
    all_df = pd.DataFrame(columns=cols)

    for file in files:
        file_path = f'{path}{PATH_SEPARATOR}{file}'
        df = pd.read_excel(file_path, usecols=cols).iloc[1:]
        all_df = all_df.append(df)
    # all_df.index = np.arange(1, len(all_df)+1)
    return all_df


def read_json():
    json_path = f'{os.getcwd()}{PATH_SEPARATOR}Settings{PATH_SEPARATOR}inputHeaders.json'

    with open(json_path) as json_file:
        data = json.load(json_file)
        return data['headers']


def get_cols(colType):

    data = read_json()
    cols = []

    for i in range(len(data)):
        if colType == 'pdf':
            col = data[i]['pdfHeader']['name']
            if not is_in_array(col, cols):
                cols.append(col)
        else:
            arr_len = len(data[i]['pdfHeader']['xlHeaders'])
            for j in range(arr_len):
                col = data[i]['pdfHeader']['xlHeaders'][j]
                if not is_in_array(col, cols):
                    cols.append(col)
    return cols


def list_pdf_fields():

    template = pdfrw.PdfFileReader(PDF_TEMPLATE_PATH)
    pages = template.pages

    for page in range(1, len(pages)+1):
        annotations = pages[page-1][ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    print(f' Page {page}: {key}, '
                          f'type {annotation[ANNOT_FORM_type]}, '
                          f'current value: {annotation[ANNOT_VAL_KEY]}')


def transform_data():
    data = read_input()
    data_to_pdf = pd.DataFrame(columns=get_cols('pdf'))
    rules = read_json()

    for index, row in data.iterrows():
        for i in range(len(rules)):
            trigger_rule(data.iloc[index], rules[i], data_to_pdf)
    # data_to_pdf.to_excel(EXCEL_OUTPUT_NAME)
    return data_to_pdf.to_dict(orient='index')


def transform_data_dict(data_dict):

    new_dict = {k.split('.')[0]: k for k in data_dict.keys()}

    for k in new_dict.keys():
        new_dict[k] = slice_dict(data_dict, k)
    return new_dict


def fill_pdf():

    data_dict = transform_data()
    template = pdfrw.PdfFileReader(PDF_TEMPLATE_PATH)
    pages = template.pages

    for key in data_dict.keys():
        data_row = transform_data_dict(data_dict[key])
        for page in range(1, len(pages)+1):
            if data_row.get(str(page)) is None:
                print(f'Skipping page {page} in file {key}...')
                continue
            page_data = data_row[str(page)]
            page_data = {k.split('.')[1]: v for k, v in page_data.items()}
            annotations = pages[page-1][ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        pdf_key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if pdf_key in page_data.keys():
                            # if annotation[ANNOT_FORM_type] == ANNOT_FORM_button:
                            #     print(f'Updating page {page}: {key},'
                            #           f'field {pdf_key},'
                            #           f' new value: {page_data[pdf_key]}')
                            #     annotation.update(pdfrw.PdfDict(V=pdfrw.PdfDict(page_data[pdf_key]),
                            #     AS=pdfrw.PdfName(page_data[pdf_key]) ))
                            if annotation[ANNOT_FORM_type] == ANNOT_FORM_text:
                                print(f'Updating file {key}:'
                                      f' page {page}:'
                                      f'field {pdf_key},'
                                      f' new value: {page_data[pdf_key]}')
                                annotation.update(pdfrw.PdfDict(V=page_data[pdf_key],
                                                                AP=page_data[pdf_key]))

        template.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        output_pdf_path = f'{OUTPUT_FOLDER}{PATH_SEPARATOR}{key}.pdf'
        pdfrw.PdfWriter().write(output_pdf_path, template)


def clear_output_folder():
    output_files = os.listdir(OUTPUT_FOLDER)

    for file in output_files:
        os.remove(f'{OUTPUT_FOLDER}{PATH_SEPARATOR}{file}')


if __name__ == '__main__':
    # clear_output_folder()
    # fill_pdf()
    list_pdf_fields()