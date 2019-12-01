import math
import sympy as sym
import sympy.physics.units as u
import common
u_m = sym.UnevaluatedExpr(u.m)
u_s = sym.UnevaluatedExpr(u.s)
u_kg = sym.UnevaluatedExpr(u.kg)
a = ""
b = ""

o = {
    'm': {'d': -1, 'e': -3},
    's': {'d': 1, 'e': 1},
}


class Unit:
    '''
    基本的な単位・複雑な単位（Pa）
    '''

    def update_table(self, target):
        for ak, av in self.table:
            if ak in target:
                self.table[ak] = {
                    'd': av['d']+target[ak]['d'],
                    'e': av['e']+target[ak]['e']
                }

    def __init__(self, table={}):
        self.table

    def __rmul__(self, e):
        u = Unit(self.table.copy())
        if isinstance(e, Unit):
            u.update_table(e.table)
            return u
        else:
            u.update_table({k: {'d': 0, 'e': math.log10(e)} for k, v in u.table})
            return u

    def __repr__(self):
        return f"<{self.symbol} e={self.e}>"

    def __pow__(self):
        pass

m = Unit('m')
s = Unit('s')
kg = Unit('kg')
N = kg * m * s**-2
Pa = N * m**-2
mm = m * 10e-3
nm = m * 10e-9
print(m, mm, nm)


class Value:
    '''
    数値と単位の演算
    '''

    def __init__(self, value, prec=6, units={}):
        self.value = value
        self.prec = prec
        self.units = units
        tex_units = ""
        if units:
            for i, j in units.item:
                if j["d"] != 0 and j["d"] != 1:
                    tex_units += str(i) + f"^{{{i["d"]}}}"
                elif j["d"] == 0:
                    tex_units += ""
                elif j["d"] == 1:
                    tex_units += str(i)
        self.tex = common(value) + " \, " + tex_units
    def __repr__(self):
        return self.tex
print(Value(10, 4, o))


class Calc:
    def __init__(self, value, prec=6, tex="", parentheses=False):
        self.value = value
        self.prec = prec
        if tex:
            self.tex =
            self.tex = sym.latex(value)
        self.parentheses = parentheses

    def __add__(self, other):
        if isinstance(other, Calc):
            value = self.value + other.value
            prec = min([self.prec, other.prec])
            tex = "%s + %s" % (self.tex, other.tex)
        else:
            value = self.value + other
            prec = self.prec
            tex = "%s + %s" % (self.tex, other)
        return Calc(value=value, prec=prec, tex=tex, parentheses=True)

    def __sub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            prec = min([self.prec, other.prec])
            tex = "%s - %s" % (self.tex, other.tex)
        else:
            value = self.value - other
            prec = self.prec
            tex = "%s - %s" % (self.tex, other)
        return Calc(value=value, prec=prec, tex=tex, parentheses=True)

    def __mul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            prec = min([self.prec, other.prec])
            if self.parentheses:
                if other.parentheses:
                    tex = r"\left(%s\right) \times \left(%s\right)" % (self.tex, other.tex)
                else:
                    tex = r"\left(%s\right) \times %s" % (self.tex, other.tex)
            else:
                if other.parentheses:
                    tex = r"%s \times \left(%s\right)" % (self.tex, other.tex)
                else:
                    tex = r"%s \times %s" % (self.tex, other.tex)
        else:
            value = self.value + other
            prec = self.prec
            if self.parentheses:
                tex = r"\left(%s\right) \times %s" % (self.tex, other)
            else:
                tex = r"%s \times %s" % (self.tex, other)
        return Calc(value=value, prec=prec, tex=tex, parentheses=False)

    def __truediv__(self, other):
        if isinstance(other, Calc):
            value = self.value / other.value
            prec = min([self.prec, other.prec])
            if self.parentheses:
                if other.parentheses:
                    tex = r"\frac{\left(%s\right)}{\left(%s\right)}" % (self.tex, other.tex)
                else:
                    tex = r"\frac{\left(%s\right)}{%s}" % (self.tex, other.tex)
            else:
                if other.parentheses:
                    tex = r"\frac{%s}{\left(%s\right)}" % (self.tex, other.tex)
                else:
                    tex = r"\frac{%s}{%s}" % (self.tex, other.tex)
        else:
            value = self.value / other
            prec = self.prec
            if self.parentheses:
                tex = r"\frac{\left(%s\right)}{%s}" % (self.tex, other)
            else:
                tex = r"\frac{%s}{%s}" % (self.tex, other)
        return Calc(value=value, prec=prec, tex=tex, parentheses=False)

        if isinstance(other, Calc):
            value = self.value**other.value
            prec = min([self.prec, other.prec])
            if self.parentheses:
                if other.parentheses:
                    tex = r"{\left(%s\right)}^{\left(%s\right)}" % (self.tex, other.tex)
                else:
                    tex = r"{\left(%s\right)}^{%s}" % (self.tex, other.tex)
            else:
                if other.parentheses:
                    tex = r"{%s}^{\left(%s\right)}" % (self.tex, other.tex)
                else:
                    tex = r"{%s}^{%s}" % (self.tex, other.tex)
        else:
            value = self.value**other
            prec = self.prec
            if self.parentheses:
                tex = r"{\left(%s\right)}^{%s}" % (self.tex, other)
            else:
                tex = r"{%s}^{%s}" % (self.tex, other)
        return Calc(value=value, prec=prec, tex=tex, parentheses=False)

    def __pow__(self, other):
        if isinstance(other, Calc):
            value = self.value**other.value
            prec = min([self.prec, other.prec])
            if self.parentheses:
                if other.parentheses:
                    tex = r"{\left(%s\right)}^{\left(%s\right)}" % (self.tex, other.tex)
                else:
                    tex = r"{\left(%s\right)}^{%s}" % (self.tex, other.tex)
            else:
                if other.parentheses:
                    tex = r"{%s}^{\left(%s\right)}" % (self.tex, other.tex)
                else:
                    tex = r"{%s}^{%s}" % (self.tex, other.tex)
        else:
            value = self.value + other
            prec = self.prec
            if self.parentheses:
                tex = r"{\left(%s\right)}^{%s}" % (self.tex, other)
            else:
                tex = r"{%s}^{%s}" % (self.tex, other)
        return Calc(value=value, prec=prec, tex=tex, parentheses=False)

    def __radd__(self, other):
        if isinstance(other, Calc):
            value = other.value + self.value
            prec = min([other.prec, self.prec])
            tex = "%s + %s" % (other.tex, self.tex)
        else:
            value = other + self.value
            prec = self.prec
            tex = "%s + %s" % (other, self.tex)
        return Calc(value=value, prec=prec, tex=tex, parentheses=True)

    def __rsub__(self, other):
        if isinstance(other, Calc):
            value = other.value - self.value
            prec = min([other.prec, self.prec])
            tex = "%s - %s" % (other.tex, self.tex)
        else:
            value = other - self.value
            prec = self.prec
            tex = "%s - %s" % (other, self.tex)
        return Calc(value=value, prec=prec, tex=tex, parentheses=True)

    def __rmul__(self, other):
        if isinstance(other, Calc):
            value = other.value * self.value
            prec = min([other.prec, self.prec])
            if self.parentheses:
                if other.parentheses:
                    tex = r"\left(%s\right) \times \left(%s\right)" % (other.tex, self.tex)
                else:
                    tex = r"\left(%s\right) \times %s" % (other.tex, self.tex)
            else:
                if other.parentheses:
                    tex = r"%s \times \left(%s\right)" % (other.tex, self.tex)
                else:
                    tex = r"%s \times %s" % (other.tex, self.tex)
        else:
            value = other * self.value
            prec = self.prec
            if self.parentheses:
                tex = r"\left(%s\right) \times %s" % (other, self.tex)
            else:
                tex = r"%s \times %s" % (other, self.tex)
        return Calc(value=value, prec=prec, tex=tex, parentheses=False)

    def __rtruediv__(self, other):
        if isinstance(other, Calc):
            value = other.value / self.value
            prec = min([self.prec, other.prec])
            if self.parentheses:
                if other.parentheses:
                    tex = r"\frac{\left(%s\right)}{\left(%s\right)}" % (other.tex, self.tex)
                else:
                    tex = r"\frac{\left(%s\right)}{%s}" % (other.tex, self.tex)
            else:
                if other.parentheses:
                    tex = r"\frac{%s}{\left(%s\right)}" % (other.tex, self.tex)
                else:
                    tex = r"\frac{%s}{%s}" % (other.tex, self.tex)
        else:
            value = other / self.value
            prec = self.prec
            if self.parentheses:
                tex = r"\frac{\left(%s\right)}{%s}" % (other, self.tex)
            else:
                tex = r"\frac{%s}{%s}" % (other, self.tex)
        return Calc(value=value, prec=prec, tex=tex, parentheses=False)

    def __repr__(self):
        return str(self.tex)

    def doit(self):
        return self.value.doit()

    def latex(self, variable=""):
        print(self.value)
        latex = r"""\begin{align*}
    %s &= %s \\
    &= %s
\end{align*}""" % (variable, self.tex, sym.latex(self.value.doit()))
        print(latex)


a = (Calc(20*u_m)+Calc(3*u_m)) * Calc(3)
a.latex('N')
