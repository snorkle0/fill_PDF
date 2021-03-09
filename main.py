import pandas as pd
import numpy as np
import os
import PyPDF2
import pdfrw
import json
from src.CustomFunctions.customFunctions import trigger_rule
from src.utils import is_in_array


#PDF constants
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

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

    for page in template.pages:
        annotations = page[ANNOT_KEY]
        for annotation in annotations:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = annotation[ANNOT_FIELD_KEY][1:-1]
                    print(key)

def transform_data():
    data = read_input()
    data_to_pdf = pd.DataFrame(columns=get_cols('pdf'))
    rules = read_json()

    for index, row in data.iterrows():
        for i in range(len(rules)):
            trigger_rule(data.iloc[index], rules[i], data_to_pdf)

    # print(f'Type from main: {type(data_to_pdf)}')
    # print(data_to_pdf)
    data_to_pdf.to_excel(EXCEL_OUTPUT_NAME)
    return data_to_pdf.to_dict(orient='index')


def fill_pdf():

    data_dict = transform_data()
    template = pdfrw.PdfFileReader(PDF_TEMPLATE_PATH)

    for key in data_dict.keys():
        # print(f'Row {key}: {data_dict[key]}')
        data_row = data_dict[key]  #transform each row into dict
        for page in template.pages:
            annotations = page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        pdf_key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if pdf_key in data_row.keys():


# read_input()
# transform_data()
# list_pdf_fields()
fill_pdf()
