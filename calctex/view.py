import numpy as np


def _validate(data, header=[]):
    if isinstance(data, list):
        if all(isinstance(e, list) and len(e) == len(data[0]) for e in data):
            data = np.array(data)
        else:
            raise Exception('each list-of-list is not same length')
    elif isinstance(data, np.ndarray):
        if len(data.shape) != 2:
            raise Exception('dimention is not 2')
    else:
        raise Exception('input type error')

    if len(header) and data.shape[1] != len(header):
        raise Exception('dimention does not match with header length')

    return data, header


def _to_str_list(data):
    return list(map(lambda e: str(e), data))


def _to_markdown_row(data):
    return f"|{'|'.join(_to_str_list(data))}|"


def _to_tex_row(data):
    return f"{' & '.join(_to_str_list(data))} \\\\"


def to_markdown_table(data, header=[]):
    data, header = _validate(data, header)
    result = []
    if len(header):
        result.append(_to_markdown_row(header))
        result.append(_to_markdown_row(list(map(lambda e: '---', header))))
    for row in data:
        result.append(_to_markdown_row(row))
    return '\n'.join(result)


def to_tex_table(data, header=[]):
    data, header = _validate(data, header)
    result = []
    if len(header):
        result.append(_to_tex_row(header))
    for row in data:
        result.append(_to_tex_row(row))
    return '\n'.join(result)


__all__ = ['to_markdown_table', 'to_tex_table']
