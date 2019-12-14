import functools
import math
import copy


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
        self.priorities = []
        self.rules = []
        self.rules_history = ''
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
        u.priorities = self.priorities.copy()
        u.e = self.e
        u.rules = copy.deepcopy(self.rules)
        u.rules_history = self.rules_history
        return u

    def info(self):
        return f"""
        symbol: {self.symbol}
        priorities: {self.priorities}
        e: {self.e}
        table: {self.table}
        rules: {self.rules_history}
        """

    def __ror__(self, e):
        from .value import Value
        return Value(e, self)

    def __add__(self, e):
        u = self.clone()
        u.symbol = None
        if isinstance(e, Unit):
            raise "error"
        else:
            u.rules_history += f"(+{e})"
            u.rules.append((lambda x: x - e, lambda y: y + e))
            return u

    def __mul__(self, e):
        u = self.clone()
        u.symbol = None
        if isinstance(e, Unit):
            u.e += e.e
            for key, value in e.table.items():
                u.table[key] = u.table.get(key, 0) + e.table[key]
            u.rules_history += e.rules_history
            u.rules.extend(e.rules)
            return u
        else:
            u.rules_history += f"(*{e})"
            u.rules.append((lambda x: x / e, lambda y: y * e))
            return u

    def __pow__(self, e):
        u = self.clone()
        u.symbol = None
        u.e *= e
        for k in u.table.keys():
            u.table[k] *= e
        return u

    def __radd__(self, e):
        return self + e

    def __rsub__(self, e):
        return self * (-1) + e

    def __sub__(self, e):
        return self + (-1) * e

    def __rmul__(self, e):
        return self.clone() * e

    def __truediv__(self, e):
        return self.clone() * e**-1

    def __rtruediv__(self, e):
        return self.clone()**-1 * e

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
        _self = self.clone()
        _self.symbol = symbol
        return _self

    def __eq__(self, u):
        '''
        次元・倍分量まで等しいか確認する
        '''
        if len(u.table.keys()) != len(self.table.keys()) or self.e != u.e:
            return False

        for k, v in self.table.items():
            if k not in u.table or u.table[k] != v:
                return False

        if self.rules_history != u.rules_history:
            return False

        return True

    def __ne__(self, u):
        return not self == u

    def trans_value(self, value):
        '''
        基本単位から併用単位に変換する
        '''
        for rule in self.rules:
            value = rule[1](value)
        return value

    def inv_trans_value(self, value):
        '''
        併用単位から基本単位に変換する
        '''
        for rule in reversed(self.rules):
            value = rule[0](value)
        return value

    def is_same_dim(self, u):
        '''
        次元が等しいか確認する。倍量分量については確認しない
        '''
        if len(u.table.keys()) != len(self.table.keys()):
            return False

        for k, v in self.table.items():
            if k not in u.table or u.table[k] != v:
                return False

        return True

    def is_zero_dim(self):
        '''
        零次元か？scale、transは考慮しない
        '''
        return len(self.table) == 0

    def to_expr(self, tex=False):
        '''
        線形変換については考慮しない（Valueの責任）
        '''
        prefix = {
            12: 'T',
            9: 'G',
            6: 'M',
            3: 'k',
            0: '',
            -3: 'm',
            -6: '\\mu' if tex else 'μ',
            -9: 'n',
            -12: 'p',
        }
        symbols = []

        _self = self.clone()
        for symbol in _self.priorities:
            if symbol in _self.table:
                symbols.append((symbol, _self.table[symbol]))
                _self.table[symbol] = 0

        units = []
        for k, dim in [*symbols, *_self.table.items()]:
            if dim != 0:
                if tex:
                    units.append(k + (f"^{{{str(dim)}}}" if (dim != 1) else ""))
                else:
                    units.append(k + (str(dim) if (dim != 1) else ""))
        result = prefix[_self.e] + ('\\cdot' if tex else '').join(units)
        return f"\\mathrm{{{result}}}" if tex else result

    def get_scale(self):
        return self.e

    def scale_zero(self):
        self.e = 0
        return self

    def inverse_scale(self):
        self.e *= -1
        return self

    def set_scale(self, e):
        self.e = e
        return self

    def expect(self, *us):
        '''
        現れるべき単位・スケールを指定する
        ```
        u.expect(N**-1, (mili*Pa)('mPa'))
        ```
        '''
        _self = self.clone()
        rules = []
        rules_history = ''
        _self.priorities = []
        for u in us:
            _self = _self / u
            rules.extend(u.rules)
            rules_history += u.rules_history
            if not u.is_zero_dim():
                if not u.symbol:
                    raise f'ERROR: symbol not defined for {_self}'
                _self.table[u.symbol] = _self.table.get(u.symbol, 0) + 1
                _self.priorities.append(u.symbol)
        _self.rules = rules
        _self.rules_history = rules_history
        return _self

    def tex(self):
        return self.to_expr(tex=True)

    @staticmethod
    def sum_scale(us):
        return functools.reduce(lambda i, u: i + u.e, us, 0)


# Scale
zerodim = Unit({})
kilo = zerodim.clone().set_scale(3)('k')
hecto = zerodim.clone().set_scale(2)('h')
centi = zerodim.clone().set_scale(-2)('c')
mili = zerodim.clone().set_scale(-3)('m')
micro = zerodim.clone().set_scale(-6)('μ')
nano = zerodim.clone().set_scale(-9)('n')

# SI Basic Units
m = Unit('m')
kg = Unit('kg')
s = Unit('s')
A = Unit('A')
K = Unit('K')
mol = Unit('mol')
cd = Unit('cd')

rad = Unit('rad')

# Units
N = (kg * m * s**-2)('N')
Pa = (N * m**-2)('Pa')
C = (A * s)('C')
J = (N * m)('J')
V = (J / C)('V')
F = (C / V)('F')
W = (V * A)('W')
Wb = (V * s)('Wb')
T = (Wb / m ** -2)('T')
H = (Wb / A)('H')
Omega = (V / A)('Ω')
Hz = (s ** -1)('Hz')
L = (kilo * (centi * m)**3)('L')

# SI併用単位
celcius = (K - 273)('℃')
fahrenheit = (9 / 5.0 * K - 459.67)('°F')
minute = (s / 60.0)('min')
h = (minute / 60.0)('hour')
d = (h / 24.0)('d')
arc_degree = ((180 / math.pi) * rad)('°')
arc_minute = (arc_degree * 60.0)('′')
arc_second = (arc_minute * 60.0)('″')
eV = (1.602176634e-19 * J)('eV')
