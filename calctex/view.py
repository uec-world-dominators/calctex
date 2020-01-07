import numpy as np
import unicodedata


def _validate(data, header=[], transpose=False, row_header=None, corner=''):
    '''
    データ形式の検証と正則化
    '''
    if row_header:
        header.insert(0, corner)

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
    '''
    何らかのリストを文字列のリストにする
    '''
    return list(map(lambda e: transferer(e), data))


def _to_str_list_w(widths):
    '''
    幅を指定して文字列のリストにする
    '''
    return lambda data: list(map(lambda e: str(e[1]).ljust(widths[e[0]] - _len(e[1]) + len(e[1])), enumerate(data)))


def _to_markdown_row(data, _to_str=_to_str_list):
    '''
    Markdown形式の行を出力する
    '''
    return f"|{'|'.join(_to_str(data))}|"


def _to_tex_row(data):
    '''
    TeX形式の行を出力する
    '''
    return f"{' & '.join(_to_str_list(data,str))} \\\\"


def _to_str_matrix(data):
    '''
    何らかの行列を文字列の行列に変換する
    '''
    if isinstance(data, (list, np.ndarray)):
        return [_to_str_matrix(e) for e in data]
    elif isinstance(data, str):
        return data
    else:
        return str(data)


def _len(s):
    count = 0
    for c in s:
        t = unicodedata.east_asian_width(c)
        if t == 'F' or t == 'W' or t == 'A':
            count += 2
        else:
            count += 1
    return count


def _max_str_len(data):
    '''
    リストの中で最も文字列長が長いものを求める
    '''
    if isinstance(data, (list, np.ndarray)):
        return max(map(_max_str_len, data))
    else:
        return len(data)


def _max_str_lens(data):
    '''
    各列ごとの最大の文字列長を求める
    '''
    max_lens = np.max(np.frompyfunc(lambda e: _len(e), 1, 1)(data), axis=0)
    max_lens = np.where(max_lens < 3, 3, max_lens + 1)
    return max_lens


def to_markdown_table(data, header=[], transpose=False, row_header=None, corner=''):
    data, header = _validate(data, header, transpose, row_header, corner)

    # 列ごとの最大文字列長を求める
    header_str, data_str = _to_str_matrix(header), _to_str_matrix(data)
    max_lens = _max_str_lens(np.concatenate(
        (np.array(header_str).reshape(1, -1), np.array(data_str)), axis=0))
    _to_str = _to_str_list_w(max_lens)

    result = []
    if len(header):
        result.append(_to_markdown_row(header_str, _to_str))
        result.append(_to_markdown_row(list(map(lambda e: '-'*e[1], enumerate(max_lens))), _to_str))
    for row in data_str:
        result.append(_to_markdown_row(row, _to_str))
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
