import numpy as np
import math
from .value import Value
from .unit import Unit
from .calc import Calc


def point_digit_to_significant_figure(n, point_digit=0):
    return math.ceil(math.log10(n * 10 ** -point_digit))


def decimal_point(data, unit=Unit({}), point_digit=0):
    '''
    data : 数字のリスト
    point_digit : その桁数以上の数字を有効数字とする（小数点第一位は-1）
    unit : Unitオブジェクト
    '''
    return np.array(list(map(lambda n:
                             Value(n, unit and unit.clone(), point_digit_to_significant_figure(n, point_digit)), data)))


def multi(data, unit=Unit({}), significant=math.inf):
    '''
    複数の値に同一の有効桁数を設定する
    '''
    return np.array(list(map(lambda e: Value(e, unit and unit.clone(), significant), data)))


def from_strs(data, unit=Unit({})):
    '''
    文字列のリストをValueのリストに変換
    '''
    return np.array(list(map(lambda e: Value.from_str(e, unit), data)))

def auto(data, unit=Unit({})):
    if isinstance(data, np.ndarray):
        pass
    elif isinstance(data, list):
        data = np.array(data)
    else:
        data = np.array([data])

def c(data, unit=Unit({}), sig_figs=math.inf):
    return Calc(Value(data, unit, sig_figs))