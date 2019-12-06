isinpackage = not __name__ in ['unit', '__main__']
if isinpackage:
    from .unit import *
    from .common import roundtex
else:
    from unit import *
    from common import roundtex


class Value:
    '''
    単位と数値を合わせた意味のある値を保持する
    ```
    l = Value(1.0, m) # 1.0m
    ```
    '''

    def __init__(self, value, unit=Unit({})):
        self.value = value
        self.unit = unit

    def clone(self):
        return Value(self.value, self.unit.clone())

    def normarize_scale(self):
        e = self.unit.get_scale()
        self.unit.scale_zero()
        self.value *= 10 ** e
        return self

    def __add__(self, e):
        if isinstance(e, Value):
            if self.unit.is_same_dim(e.unit):
                if self.unit != e.unit:
                    _self = self.clone().normarize_scale()
                    _e = e.clone().normarize_scale()
                else:
                    _self = self
                    _e = e
                return Value(_self.value + _e.value, _self.unit)
            else:
                raise 'illegal addition (different dimention)'
        else:
            if self.unit.is_zero_dim():
                return Value(self.value + e, self.unit.clone())
            else:
                raise 'illegal addition (ambigant dimention)'

    def __mul__(self, e):
        _self = self.clone().normarize_scale()
        if isinstance(e, Value):
            _e = e.clone().normarize_scale()
            return Value(_self.value*_e.value, _self.unit*e.unit)
        else:
            return Value(_self.value*e, _self.unit)

    def __pow__(self, e):
        if isinstance(e, Value):
            if e.unit.is_zero_dim():
                _e = e.value
            else:
                raise "pow with not zero dimention value"
        else:
            _e = e

        _self = self.clone().normarize_scale()
        return Value(_self.value**_e, _self.unit**_e)

    def __truediv__(self, e):
        return self * e**-1

    def __radd__(self, e):
        return self + e

    def __rsub__(self, e):
        return self*(-1) + e

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
        return self + (-1)*e

    def __repr__(self):
        return f"<{self.value} {self.unit}>"

    def expect(self, *us):
        _unit = self.unit.expect(*us)
        return Value(self.value*10**_unit.get_scale(),
                     _unit.set_scale(Unit.sum_scale(us)))

    def totex(self, digits, unit=True):
        return f"{roundtex(self.value,digits)}{self.unit.totex() if unit else ''}"


isinpackage = not __name__ in ['value', '__main__']
if not isinpackage:
    # # 新しい単位
    # nN = (nano*N)('nN')

    # p = Value(3.0, nano*Pa)
    # s = Value(1.0, m**2)
    # f = p*s*10

    # print(f)
    # # <3.0000000000000004e-09 <kgms-2>>
    # print(f.expect(nN))
    # # <3.0000000000000004 <nN>>

    a = Value(1, nano * s)
    print(a.totex(4))
    print(a.expect(s).totex(2))
