import numpy as np
import math
from src.value import Value


def point_digit_to_significant_figure(n, point_digit=0):
    return math.ceil(math.log10(n * 10 ** -point_digit))


def decimal_point(data, point_digit, unit):
    '''
    data : 数字のリスト
    point_digit : その桁数以上の数字を有効数字とする（小数点第一位は-1）
    unit : Unitオブジェクト
    '''
    return np.array(list(map(lambda n:
                             Value(n, unit.clone(), point_digit_to_significant_figure(n, point_digit)), data)))


def multi(data, significant, unit=None):
    return np.array(list(map(lambda e: Value(e, unit.clone(), significant), data)))
