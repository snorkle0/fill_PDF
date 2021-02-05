import pandas as pd
import os
import PyPDF2
import csv
import json


def read_input():
    path = os.getcwd() + '\Input'


    files = os.listdir(path)

    all_df = pd.DataFrame()

    for file in files:
        file_path = f'{path}\{file}'
        df = pd.read_excel(file_path).iloc[1:]
        # df.iloc[1:]
        all_df.append(df)
        print(df)

    # print(all_df)

def read_json():
    json_path = os.getcwd() + '\Template\inputHeaders.json'


read_input()

def list_PDF_fields():
    path = os.getcwd() + '\Template'

    files = os.listdir(path)

    for file in files:
        file_path = f'{path}\{file}'
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

def write_csv(fields):
    fname = 'test.csv'
    with open(fname,'wb') as f:
        w = csv.writer(f)
        w.writerow(fields.keys())
        w.writerow(dict.values())


# list_PDF_fields()
# testDict = list_PDF_fields()
#
#
# write_csv(testDict)
