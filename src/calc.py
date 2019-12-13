#%%
from src.common import roundtex
from src.value import Value
from numpy import ndarray
import numpy as np

#%%
lambda_ = Calc([Value(300, m), Value(400, m)])
# [300, 400]*m
# 300 * m
f = Calc([Value(170, Hz), Value(340, Hz)])
v = f * lambda_  # Calc
print(v.tex(['v_1', 'v_2'])[0])  # 'v_1 = ...'
print(v.value())


#%%
type(np.array(4))




#%%
class Calc:
    def __init__(self, x, parentheses=False, tex=""):
        import numpy as np
        if isinstance(x, (Value, int, float)):
            self.value = x
        elif isinstance(x, list):
            self.value = np.array(x)
        if tex:
            self.tex = tex
        else:
            try:
                self.tex = self.totex(self.value)
            except:
                self.tex = ""
        self.parentheses = parentheses

    def totex(self):
        if isinstance(self.value, Value):
            return Value.tex()
        elif isinstance(self.value, (int, float)):
            return str(int, float)
        elif isinstance(self.value, ndarray):
            if isinstance(self.value[0], Value):
                return np.array([i.tex() for i in self.value])
            elif isinstance(self.value[0], (int, float)):
                return np.array(str(i) for i in self.value)

    def __add__(self, other):
        if isinstance(other, Calc):
            value = self.value + other.value
            tex = "%s + %s" % (self.tex, other.tex)
        else:
            value = self.value + other
            tex = "%s + %s" % (self.tex, other)
        return Calc(x=value, tex=tex, parentheses=True)

    def __sub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            tex = "%s - %s" % (self.tex, other.tex)
        else:
            value = self.value - other
            tex = "%s - %s" % (self.tex, other)
        return Calc(x=value, tex=tex, parentheses=True)

    def __mul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\left( %s \right) \times \left( %s \right)" % (self.tex, other.tex)
                else:
                    tex = r"\left( %s \right) \times %s" % (self.tex, other.tex)
            else:
                if other.parentheses:
                    tex = r"%s \times \left( %s \right)" % (self.tex, other.tex)
                else:
                    tex = r"%s \times %s" % (self.tex, other.tex)
        else:
            value = self.value * other
            if self.parentheses:
                tex = r"\left( %s \right) \times %s" % (self.tex, other)
            else:
                tex = r"%s \times %s" % (self.tex, other)
        return Calc(x=value, tex=tex, parentheses=False)

    def __truediv__(self, other):
        if isinstance(other, Calc):
            value = self.value / other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\frac{\left( %s \right)}{\left( %s \right)}" % (self.tex, other.tex)
                else:
                    tex = r"\frac{\left( %s \right)}{%s}" % (self.tex, other.tex)
            else:
                if other.parentheses:
                    tex = r"\frac{%s}{\left( %s\right )}" % (self.tex, other.tex)
                else:
                    tex = r"\frac{%s}{%s}" % (self.tex, other.tex)
        else:
            value = self.value / other
            if self.parentheses:
                tex = r"\frac{\left( %s \right)}{%s}" % (self.tex, other)
            else:
                tex = r"\frac{%s}{%s}" % (self.tex, other)
        return Calc(x=value, tex=tex, parentheses=False)

    def __pow__(self, other):
        if isinstance(other, Calc):
            value = self.value**other.value
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
            if self.parentheses:
                if other == 0.5:
                    tex = r"\sqrt{%s}" % self.tex
                else:
                    tex = r"{\left(%s\right)}^{%s}" % (self.tex, other)
            else:
                tex = r"{%s}^{%s}" % (self.tex, other)
        return Calc(x=value, tex=tex, parentheses=False)

    def __radd__(self, other):
        if isinstance(other, Calc):
            value = other.value + self.value
            tex = "%s + %s" % (other.tex, self.tex)
        else:
            value = self.value + other
            tex = "%s + %s" % (other, self.tex)
        return Calc(x=value, tex=tex, parentheses=True)

    def __rsub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            tex = "%s - %s" % (other.tex, self.tex)
        else:
            value = other - self.value
            tex = "%s - %s" % (other, self.tex)
        return Calc(x=value, tex=tex, parentheses=True)

    def __rmul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\left( %s \right) \times \left( %s \right)" % (other.tex, self.tex)
                else:
                    tex = r"\left( %s \right) \times %s" % (other.tex, self.tex)
            else:
                if other.parentheses:
                    tex = r"%s \times \left( %s \right)" % (other.tex, self.tex)
                else:
                    tex = r"%s \times %s" % (other.tex, self.tex)
        else:
            value = self.value * other
            if self.parentheses:
                tex = r"\left( %s \right) \times %s" % (other, self.tex)
            else:
                tex = r"%s \times %s" % (other, self.tex)
        return Calc(x=value, tex=tex, parentheses=False)

    def __rtruediv__(self, other):
        if isinstance(other, Calc):
            value = other.value / self.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\frac{\left( %s \right)}{\left( %s \right)}" % (other.tex, self.tex)
                else:
                    tex = r"\frac{\left( %s \right)}{%s}" % (other.tex, self.tex)
            else:
                if other.parentheses:
                    tex = r"\frac{%s}{\left( %s\right )}" % (other.tex, self.tex)
                else:
                    tex = r"\frac{%s}{%s}" % (other.tex, self.tex)
        else:
            value = other / self.value
            if self.parentheses:
                tex = r"\frac{\left( %s \right)}{%s}" % (other, self.tex)
            else:
                tex = r"\frac{%s}{%s}" % (other, self.tex)
        return Calc(x=value, tex=tex, parentheses=False)

    def __repr__(self):
        return str(self.tex)

    def latex(self, variable=""):
        print(self.value)
        latex = r"""\begin{align*}
    %s &= %s \\
    &= %s
\end{align*}""" % (variable, self.tex, self.value.tex)
