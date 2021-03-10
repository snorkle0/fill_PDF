

def isNaN(str):
    return str != str


def is_in_array(val, arr):
    s = set(arr)
    if val in s:
        return True
    return False


def slice_dict(d, s):
    return {k: v for k, v in d.items() if k.startswith(s)}