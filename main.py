import pandas as pd
import os
import PyPDF2
import json

OUTPUT_NAME = 'output.xlsx'
PATH_SEPARATOR = os.sep


def read_input():
    path = f'{os.getcwd()}{PATH_SEPARATOR}Input'
    files = os.listdir(path)
    cols = read_json()

    all_df = pd.DataFrame(columns=cols)

    for file in files:
        file_path = f'{path}{PATH_SEPARATOR}{file}'
        df = pd.read_excel(file_path).iloc[1:]
        all_df = all_df.append(df)
    all_df.dropna(how='all', axis=1, inplace=True)
    if os.path.exists(OUTPUT_NAME):
        os.remove(OUTPUT_NAME)
    all_df.to_excel(OUTPUT_NAME, index=False)


def read_json():
    json_path = f'{os.getcwd()}{PATH_SEPARATOR}Settings{PATH_SEPARATOR}inputHeaders.json'

    with open(json_path) as json_file:
        data = json.load(json_file)
        return data['headers']


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


read_input()