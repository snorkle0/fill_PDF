import pandas as pd
import numpy as np
import os
import PyPDF2
import json
from src.CustomFunctions.customFunctions import trigger_rule

OUTPUT_NAME = 'output.xlsx'
PATH_SEPARATOR = os.sep


def read_input():
    path = f'{os.getcwd()}{PATH_SEPARATOR}Input'
    files = os.listdir(path)
    cols = get_cols('xl')
    all_df = pd.DataFrame(columns=cols)

    for file in files:
        file_path = f'{path}{PATH_SEPARATOR}{file}'
        df = pd.read_excel(file_path, usecols=cols).iloc[1:]
        all_df = all_df.append(df)
    # if os.path.exists(OUTPUT_NAME):
    #     os.remove(OUTPUT_NAME)
    # all_df.to_excel(OUTPUT_NAME, index=False)
    all_df.index = np.arange(1, len(all_df)+1)
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
    path = f'{os.getcwd()}{PATH_SEPARATOR}Template'

    files = os.listdir(path)

    for file in files:
        file_path = f'{path}{PATH_SEPARATOR}{file}'
        f = PyPDF2.PdfFileReader(file_path)
        n_pages = f.getNumPages()

        print(n_pages)
        for i in range(n_pages):
            curr_page = f.getPage(i)
            try:
                for annot in curr_page['/Annots']:
                    print(f'Page {i}: {annot.getObject()}')
                    print('')
            except:
                pass
            return


def transform_data():
    data = read_input()
    data_to_pdf = pd.DataFrame(columns=get_cols('pdf'))
    rules = read_json()

    for index, row in data.iterrows():
        for i in range(len(rules)):
            rule_name = rules[i]['pdfHeader']['name']
            rule_action = rules[i]['pdfHeader']['action']
            rule_index = data_to_pdf.columns.get_loc(rule_name)
            # print(index)
            trigger_rule(data.iloc[index], rule_index, rule_action, data_to_pdf)


def is_in_array(val, arr):
    s = set(arr)
    if val in s:
        return True
    return False


transform_data()

