import math
import functools


class Unit:
    '''
    基本的な単位・複雑な単位（Pa）
    # 使い方
    ```
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

    def __init__(self, e={}):
        '''
        Unit('m')
        Unit({'m':{'d':1, 'e':0}})
        '''
        if isinstance(e, dict):
            self.table = e
        elif isinstance(e, str):
            self.table = {e: {'d': 1, 'e': 0}}

    def update_table(self, target):
        for tk, tv in target.items():
            v = self.table.get(tk, {})
            self.table[tk] = {
                'd': v.get('d', 0)+tv['d'],
                'e': v.get('e', 0)+tv['e'],
            }

    def __mul__(self, e):
        u = Unit(self.table.copy())
        if isinstance(e, Unit):
            u.update_table(e.table)
            return u
        else:
            u.update_table({kv[0]: {'d': 0, 'e': math.log10(e)} for kv in u.table})
            return u

    def __pow__(self, e):
        u = Unit(self.table.copy())
        for tk, tv in u.table.items():
            v = u.table.get(tk, {})
            u.table[tk] = {
                'd': v.get('d', 1)*e,
                'e': v.get('e', 0)*e,
            }
        return u

    def __repr__(self):
        return '<'+', '.join(map(lambda kv: f"{kv[0]} dim={kv[1]['d']} e=10**{kv[1]['e']}", self.table.items()))+'>'




isinpackage = not __name__ in ['common', '__main__']
if not isinpackage:
    m = Unit('m')
    s = Unit('s')
    kg = Unit('kg')
    N = kg * m * s**-2
    Pa = N * m**-2
    mm = m * 1e-3
    nm = m * 1e-9
    print(N, Pa, m, mm, nm)
