isinpackage = not __name__ in ['unit', '__main__']

import math
import functools


class Unit:
    '''
    基本的な単位・複雑な単位（Pa）
    # 使い方
    ```py
    m = Unit('m')
    s = Unit('s')
    kg = Unit('kg')
    N = kg * m * s**-2
    Pa = N * m**-2
    mm = m * 1e-3
    nm = m * 1e-9
    print(N, Pa, m, mm, nm)
    ```
    '''

    def __init__(self, e={}, symbol=''):
        '''
        ```py
        Unit('m')
        Unit({'m':2,'s':1})
        ```
        '''
        if isinstance(e, dict):
            self.table = e
            self.e = 0
            self.symbol = symbol
        elif isinstance(e, str):
            self.table = {e: 1}
            self.e = 0
            self.symbol = e

    def clone(self):
        u = Unit(self.table.copy())
        u.symbol = self.symbol
        u.e = self.e
        return u

    def __mul__(self, e):
        u = self.clone()
        u.symbol = None
        if isinstance(e, Unit):
            u.e += e.e
            for key, value in e.table.items():
                u.table[key] = u.table.get(key, 0) + e.table[key]
        else:
            u.e += math.log10(e)
        return u

    def __pow__(self, e):
        u = self.clone()
        u.symbol = None
        u.e *= e
        for k in u.table.keys():
            u.table[k] *= e
        return u

    def __rmul__(self, e):
        return self.clone() * e

    def __truediv__(self, e):
        return self.clone() * e**-1

    def __repr__(self):
        if self.symbol:
            return f"<{self.symbol}>"
        else:
            return f"<{self.to_expr()}>"

    def __call__(self, symbol):
        '''
        シンボルを設定する
        ```
        Pa = (N * m**-2)('Pa')
        ```
        '''
        self.symbol = symbol
        return self

    def __eq__(self, u):
        '''
        次元・倍分量まで等しいか確認する
        '''
        if len(u.table.keys()) != len(self.table.keys()) or self.e != u.e:
            return False

        for k, v in self.table.items():
            if not k in u.table or u.table[k] != v:
                return False

        return True

    def __ne__(self, u):
        return not self == u

    def is_same_dim(self, u):
        '''
        次元が等しいか確認する。倍量分量については確認しない
        '''
        if len(u.table.keys()) != len(self.table.keys()):
            return False

        for k, v in self.table.items():
            if not k in u.table or u.table[k] != v:
                return False

        return True

    def to_expr(self):
        prefix = {
            12: 'T',
            9: 'G',
            6: 'M',
            3: 'k',
            0: '',
            -3: 'm',
            -6: 'μ',
            -9: 'n',
            -12: 'p',
        }
        result = prefix[self.e]
        for k, v in self.table.items():
            if v != 0:
                result += k + (str(v) if (v != 1) else "")
        return result

    def get_scale(self):
        return self.e

    def scale_zero(self):
        self.e = 0
        return self

    def expect(self, *us):
        '''
        現れるべき単位を指定する
        ```
        u.expect(N**-1, (mili*Pa)('mPa'))
        ```
        '''
        _self = self.clone()
        for u in us:
            _self = _self/u
            if not u.symbol:
                raise f'ERROR: symbol not defined for {_self}'
            _self.table[u.symbol] = _self.table.get(u.symbol, 0) + 1

        return _self


kilo = 1e3
hecto = 1e2
centi = 1e1
mili = 1e-3
micro = 1e-6
nano = 1e-9

m = Unit('m')
kg = Unit('kg')
s = Unit('s')
A = Unit('A')

N = (kg * m * s**-2)('N')
Pa = (N * m**-2)('Pa')

C = (A*s)('C')
J = (N*m)('J')
V = (J/C)('V')
F = (C/V)('F')
W = (V*A)('W')
Wb = (V*s)('Wb')
T = (Wb/m**-2)('T')
H = (Wb/A)('H')
Omega = (V/A)('Ω')

if not isinpackage:
    print(((nano*m*s)/(mili*m)))
    print((nano*N*Pa*m).expect(N, (mili*Pa)('mPa')))
