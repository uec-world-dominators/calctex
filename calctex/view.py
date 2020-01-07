import numpy as np


def _validate(data, header=[], transpose=False, row_header=None):
    if isinstance(data, list):
        if all(isinstance(e, list) and len(e) == len(data[0]) for e in data):
            data = np.array(data)
        elif all(not isinstance(e, list) for e in data):
            data = np.array(data).reshape(1, -1)
        else:
            raise Exception('each list-of-list is not same length')
    elif isinstance(data, np.ndarray):
        if len(data.shape) != 2:
            raise Exception('dimention is not 2')
    else:
        raise Exception('input type error')

    if transpose:
        data = data.T

    if row_header and len(row_header) == data.shape[0]:
        data = np.concatenate((np.array(row_header).reshape(1, -1).T, data), axis=1)

    if len(header) and data.shape[1] != len(header):
        raise Exception('dimention does not match with header length')

    return data, header


def _to_str_list(data, transferer=id):
    return list(map(lambda e: transferer(e), data))


def _to_markdown_row(data, transferer=id):
    return f"|{'|'.join(_to_str_list(data,transferer))}|"


def _to_tex_row(data):
    return f"{' & '.join(_to_str_list(data,str))} \\\\"


def _to_str_matrix(data):
    if isinstance(data, (list, np.ndarray)):
        return [_to_str_matrix(e) for e in data]
    elif isinstance(data, str):
        return data
    else:
        return str(data)


def _max_str_len(data):
    if isinstance(data, (list, np.ndarray)):
        return max(map(_max_str_len, data))
    else:
        return len(data)


def to_markdown_table(data, header=[], transpose=False, row_header=None, corner=' '*3):
    if row_header:
        header.insert(0, corner)
    data, header = _validate(data, header, transpose, row_header)
    result = []
    header_str, data_str = _to_str_matrix(header), _to_str_matrix(data)
    max_len = _max_str_len([header_str, data_str, '---']) + 1
    def transferer(e): return e.ljust(max_len)
    if len(header):
        result.append(_to_markdown_row(header_str, transferer))
        result.append(_to_markdown_row(list(map(lambda e: '-'*max_len, header)), transferer))
    for row in data_str:
        result.append(_to_markdown_row(row, transferer))
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
