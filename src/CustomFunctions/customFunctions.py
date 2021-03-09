from datetime import datetime
from src.utils import isNaN


def trigger_rule(row, rules, output):

    rule_action = rules['pdfHeader']['action']
    rule_name = rules['pdfHeader']['name']
    function_name = rule_action.split('(')[0]
    rule_index = output.columns.get_loc(rule_name)

    functionList = {
        'grabValue': grabValue,
        'defaultValue': defaultValue,
        'getTodaysDate': getTodaysDate,
        'combineWithDelimiter': combineWithDelimiter,
        'convertToDate': convertToDate,
        'extractTextByDelimiter': extractTextByDelimiter
    }

    parameters = {
        'data': row,
        'xlHeaders': rules['pdfHeader']['xlHeaders'],
        'optional_arg': rule_action.split('(')[1].split(')')[0]
    }

    rule_result = functionList[function_name](**parameters)
    output.at[row.name, rule_name] = rule_result
    # print(f'Type from custom functions: {type(output)}')
    return output


def grabValue(data='1', xlHeaders='1', optional_arg = '1'):
    val = data[xlHeaders[0]]
    return val


def defaultValue(data='1', xlHeaders='1', optional_arg = '1'):
    return optional_arg


def getTodaysDate(data='1', xlHeaders='1', optional_arg = '1'):
    return datetime.today().strftime('%d.%m.%y')


def combineWithDelimiter(data='1', xlHeaders='1', optional_arg = '1'):
    vals = []
    delimiter = optional_arg

    for i in range(len(xlHeaders)):
        val = data[xlHeaders[i]]
        if not isNaN(val):
            vals.append(val)

    delimiter = delimiter.join(vals)
    result = delimiter

    return result


def convertToDate(data='1', xlHeaders='1', optional_arg = '1'):
    val = data[xlHeaders[0]]
    result = val
    return result


def extractTextByDelimiter(data='1', xlHeaders='1', optional_arg = '1'):
    val = data[xlHeaders[0]]
    extract_direction = optional_arg.split(',')[0]

    if extract_direction == 'before':
        arr_pos = 0
    else:
        arr_pos = 1

    delimiter = optional_arg.split(',')[1].strip()
    result = val.split(delimiter)[arr_pos]

    return result


