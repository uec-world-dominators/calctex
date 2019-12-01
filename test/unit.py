import math


class Unit:
    '''
    基本的な単位・複雑な単位（Pa）
    '''

    def update_table(self, target):
        self.table
        for ak, av in self.table:
            if ak in target:
                self.table[ak] = {
                    'd': av['d']+target[ak]['d'],
                    'e': av['e']+target[ak]['e']
                }

    def __init__(self, table={}):
        self.table = table

    # def __rmul__(self, e):
    #     u = Unit(self.table.copy())
    #     if isinstance(e, Unit):
    #         u.update_table(e.table)
    #         return u
    #     else:
    #         u.update_table({k: {'d': 0, 'e': math.log10(e)} for k, v in u.table})
    #         return u

    def __mul__(self, e):
        u = Unit(self.table.copy())
        if isinstance(e, Unit):
            u.update_table(e.table)
            return u
        else:
            u.update_table({kv[0]: {'d': 0, 'e': int(math.log10(e))} for kv in u.table})
            return u

    def __repr__(self):
        return f"<{self.symbol} e={self.e}>"

    def __pow__(self):
        pass


m = Unit({'m': {'d': 1, 'e': 1}})
s = Unit({'s': {'d': 1, 'e': 1}})
kg = Unit({'kg': {'d': 1, 'e': 1}})
H = kg*m
# N = kg * m * s**-2
# Pa = N * m**-2
mm = m * 10e-3
nm = m * 10e-9
print(m, mm, nm)
