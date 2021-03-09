

def isNaN(str):
    return str != str


def is_in_array(val, arr):
    s = set(arr)
    if val in s:
        return True
    return False
