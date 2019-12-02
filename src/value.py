# from .unit import Unit, Pa
from unit import Unit, Pa, s, m


class Value:
    def __init__(self, value, unit):
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
            raise 'illegal addition (ambigant dimention)'

    def __mul__(self, e):
        if isinstance(e, Value):
            _self = self.clone().normarize_scale()
            _e = e.clone().normarize_scale()
            return Value(_self.value*_e.value, _self.unit.mul(e.unit))
        else:
            raise 'illegal addition (ambigant dimention)'

    def __pow__(self, e):
        _self = self.clone().normarize_scale()
        return Value(_self.value**e, _self.unit**e)

    def __truediv__(self, e):
        return self * e**-1

    def __sub__(self, e):
        return self + (-1)*e

    def __repr__(self):
        return f"<{self.value} {self.unit}>"


isinpackage = not __name__ in ['value', '__main__']
if not isinpackage:
    l = Value(1.0, m)
    t = Value(2.0, s)
    print(l/t)
