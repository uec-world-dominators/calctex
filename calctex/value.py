import math
from .unit import Unit
from .common import roundtex


class Value:
    '''
    単位と数値を合わせた意味のある値を保持する
    ```
    l = Value(1.0, m) # 1.0m
    ```
    '''

    def __init__(self, value, unit=Unit({}), significant=math.inf, trans_normarized=False):
        self.unit = unit and unit.clone() or Unit({})
        self.significant = significant
        self.value = value if trans_normarized else self.unit.inv_trans_value(value)
        if len(self.unit.rules):
            self.unit.rules = []
            self.unit.rules_history = ''
            self.unit.symbol = None

    def clone(self):
        return Value(self.value, self.unit.clone(), self.significant)

    def info(self):
        return f"""
        value           : {self.value}
        significant     : {self.significant}
        unit            : {self.unit.info()}
        """

    def normarize_scale(self):
        self.unit.symbol = None
        e = self.unit.get_scale()
        self.unit.scale_zero()
        self.value *= 10 ** e
        return self

    def normarize(self):
        self.normarize_scale()
        return self

    def __add__(self, e):
        if isinstance(e, Value):
            if self.unit.is_same_dim(e.unit):
                if self.unit != e.unit:
                    _self = self.clone().normarize()
                    _e = e.clone().normarize()
                else:
                    _self = self
                    _e = e
                significant = min(_self.significant, _e.significant)
                return Value(_self.value + _e.value, _self.unit.clone(), significant, True)
            else:
                raise 'illegal addition (different dimention)'
        else:
            if self.unit.is_zero_dim():
                return Value(self.value + e, self.unit.clone(), self.significant)
            else:
                raise 'illegal addition (ambigant dimention)'

    def __mul__(self, e):
        _self = self.clone().normarize()
        if isinstance(e, Value):
            _e = e.clone().normarize()
            significant = min(_self.significant, _e.significant)
            return Value(_self.value * _e.value, _self.unit * e.unit, significant, True)
        else:
            return Value(_self.value * e, _self.unit.clone(), _self.significant, True)

    def __pow__(self, e):
        if isinstance(e, Value):
            if e.unit.is_zero_dim():
                _e = e.value
            else:
                raise "pow with not zero dimention value"
        else:
            _e = e
        _self = self.clone().normarize()
        return Value(_self.value**_e, _self.unit**_e, _self.significant, True)

    def __truediv__(self, e):
        return self * e**-1

    def __radd__(self, e):
        return self + e

    def __rsub__(self, e):
        return self * (-1) + e

    def __rmul__(self, e):
        return self * e

    def __rtruediv__(self, e):
        return self**-1 * e

    def __rpow__(self, e):
        if self.unit.is_zero_dim():
            return Value(e**self.value)
        else:
            raise "pow with not zero dimention value (self has dimention)"

    def __sub__(self, e):
        return self + (-1) * e

    def __repr__(self):
        return f"<{self.value} {self.unit}>"

    def __or__(self,e):
        _self = self.clone()
        _self.significant = e
        return _self

    def expect(self, *us):
        _self = self.clone()
        _self.normarize()
        _unit = _self.unit.expect(*us)
        e = _unit.get_scale()
        _self.unit = _unit.set_scale(Unit.sum_scale(us) + e)
        _self.value = _unit.trans_value(_self.value) * 10 ** e
        return _self

    def tex(self, significant=None, unit=True):
        if not significant and self.significant == math.inf:
            main = str(self.value)
        else:
            main = roundtex(self.value, self.significant if significant == None else significant)
        return main + (' \\,' + self.unit.tex() if unit and not self.unit.is_zero_dim() else '')

    def fn(self, fn, multi_dim=False):
        '''
        numpy用の関数適用
        multi_dim : 非零次元を許可するか
        '''
        if not multi_dim and self.unit.is_zero_dim():
            return Value(fn(self.value), self.unit.clone(), self.significant)
        else:
            raise "not zero dimention"

    def sin(self):
        return self.fn(math.sin)

    def cos(self):
        return self.fn(math.cos)

    def tan(self):
        return self.fn(math.tan)

    def sinh(self):
        return self.fn(math.sinh)

    def cosh(self):
        return self.fn(math.cosh)

    def tanh(self):
        return self.fn(math.tanh)

    def arcsin(self):
        return self.fn(math.asin)

    def arccos(self):
        return self.fn(math.acos)

    def arctan(self):
        return self.fn(math.atan)

    def arctan2(self):
        return self.fn(math.atan2)

    def arcsinh(self):
        return self.fn(math.asinh)

    def arccosh(self):
        return self.fn(math.acosh)

    def arctanh(self):
        return self.fn(math.atanh)

    def exp(self):
        return self.fn(math.exp)

    def log(self):
        return self.fn(math.log)

    def log10(self):
        return self.fn(math.log10)

    def log2(self):
        return self.fn(math.log2)

    def log1p(self):
        return self.fn(math.log1p)

    def floor(self):
        return self.fn(math.floor, multi_dim=True)

    def trunc(self):
        return self.fn(math.trunc, multi_dim=True)

    def ceil(self):
        return self.fn(math.ceil, multi_dim=True)

    def __abs__(self):
        return self.fn(abs, multi_dim=True)

    def rint(self):
            return self.fn(round, multi_dim=True)

    @staticmethod
    def from_str(data: [str], unit: Unit = Unit({})): 
        '''
        文字列から有効桁数を読み取る
        '''
        v = float(data)
        return Value(v, unit and unit.clone(), significant=len(data) - bool(v % 1))
