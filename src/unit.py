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

    # self.
    def __init__(self, e={}, symbol=''):
        '''
        ```py
        Unit('m')
        Unit({'m':{'d':1, 'e':0}})
        ```
        '''
        if isinstance(e, dict):
            self.table = e
            self.symbol = symbol
        elif isinstance(e, str):
            self.table = {e: {'d': 1, 'e': 0}}
            self.symbol = e

    def update_table(self, target, zero_dim=True):
        for tk, tv in target.items():
            v = self.table.get(tk, {})
            d = v.get('d', 0)+tv['d']
            e = v.get('e', 0)+tv['e']

            # if not zero_dim or d != 0:
            self.table[tk] = {'d': d, 'e': e}

    def __rmul__(self, e):
        return self.clone() * e

    def __mul__(self, e):
        u = self.clone()
        u.symbol = None
        if isinstance(e, Unit):
            u.update_table(e.table)
        else:
            u.update_table({k: {'d': 0, 'e': math.log10(e)} for k in u.table.keys()})
        return u

    def __pow__(self, e):
        u = Unit(self.table.copy())
        u.symbol = None
        for tk, tv in u.table.items():
            v = u.table.get(tk, {})
            u.table[tk] = {
                'd': v.get('d', 1)*e,
                'e': v.get('e', 0)*e,
            }
        return u

    def __truediv__(self, e):
        return self.clone() * e**-1

    def __repr__(self):
        if self.symbol:
            return f"<{self.symbol}>"
        else:
            return f"<{self.to_expr()}>"

    def is_same_dim(self, u):
        if len(u.table.keys()) != len(self.table.keys()):
            return False

        for k, v in self.table.items():
            if not k in u.table or u.table[k]['d'] != v['d']:
                return False

        return True

    def to_expr(self):
        obj = {
            3: 'k',
            0: '',
            -3: 'm',
            -6: 'μ',
            -9: 'n',
        }
        result = ''
        for k, v in self.table.items():
            if v['d'] != 0:
                result += obj[v['e']] + k + (str(v['d']) if (v['d'] != 1) else "")
        return result

    def clone(self):
        u = Unit(self.table.copy())
        u.symbol = self.symbol
        return u

    def set_symbol(self, symbol):
        self.symbol = symbol
        return self

    def __call__(self, symbol):
        return self.set_symbol(symbol)

    def get_scale(self):
        return functools.reduce(lambda i, v: i+v['e'], self.table.values(), 0)

    def scale_zero(self):
        for k, v in self.table.items():
            self.table[k]['e'] = 0

    def asunit(self, u):
        print(u.table)
        _self = self.clone()
        _u = u.clone()

        ru = _self / _u
        ru.table[u.symbol] = {'d': 1, 'e': 0}

        return ru

    def __eq__(self, u):
        if len(u.table.keys()) != len(self.table.keys()):
            return False

        for k, v in self.table.items():
            if not k in u.table or u.table[k]['d'] != v['d'] or u.table[k]['e'] != v['e']:
                return False

        return True

    def __ne__(self, u):
        return not self == u


mili = 1e-3
micro = 1e-6
nano = 1e-9

m = Unit('m')
s = Unit('s')
kg = Unit('kg')
N = (kg * m * s**-2)('N')
Pa = (N * m**-2)('Pa')
nm = nano*m

# isinpackage = not __name__ in ['unit', '__main__']
# if not isinpackage:
#     print(Pa)
#     print(nm)
#     print(m/m)
