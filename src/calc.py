#%%
from src.common import roundtex
from src.value import Value
from numpy import ndarray
import numpy as np
from src.unit import *

class Calc:
    def __init__(self, x, parentheses=False, tex=""):
        import numpy as np
        from numpy import ndarray
        if isinstance(x, Value):
            x = x
        elif isinstance(x, (int, float)):
            x = Value(x)
        elif isinstance(x, list):
            x = np.array([Value(i) if isinstance(i, (int, float)) else i for i in x])
        else:
            raise ValueError("error!")
        self.value = x
        if tex:
            self.tex = tex
        else:
            if isinstance(x, Value):
                self.tex = self.value.totex()
            elif isinstance(x, ndarray):
                self.tex = str(self.value)
            try:
                self.tex = str(self.value[0])
            except:
                self.tex = str(self.value)
            # try:
            #     self.tex = self.totex(self.value)
            # except:
            #     self.tex = ""
        self.parentheses = parentheses

    def totex(self):
        if isinstance(self.value, Value):
            return self.value.totex()
        elif isinstance(self.value, ndarray):
            return [i.totex() for i in self.value]

    def __add__(self, other):
        if isinstance(other, Calc):
            value = self.value + other.value
            tex = self.tex + " + " + other.tex
        else:
            value = self.value + other
            tex = self.tex + " + " + str(other)
        return Calc(x=value, tex=tex, parentheses=True)

    def __sub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            tex = self.tex + " - " + other.tex
        else:
            value = self.value - other
            tex = self.tex + " - " + str(other)
        return Calc(x=value, tex=tex, parentheses=True)

    def __mul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\left( " + self.tex + r" \right) \times \left( " + other.tex + r" \right)"
                else:
                    tex = r"\left( " + self.tex + " \right) \times " + other.tex
            else:
                if other.parentheses:
                    tex = self.tex + r" \times \left( " + other.tex + r" \right)"
                else:
                    tex = self.tex + r" \times " + other.tex
        else:
            value = self.value * other
            if self.parentheses:
                tex = r"\left( " + self.tex + r" \right) \times " + str(other)
            else:
                tex = self.tex + r" \times " + str(other)
        return Calc(x=value, tex=tex, parentheses=False)

    def __truediv__(self, other):
        if isinstance(other, Calc):
            value = self.value / other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\frac{\left( " + self.tex + r" \right)}{\left( " + other.tex + r" \right)}"
                else:
                    tex = r"\frac{\left( " + self.tex + r" \right)}{" + other.tex + r"}"
            else:
                if other.parentheses:
                    tex = r"\frac{" + self.tex + r"}{\left( " + other.tex + r" \right)}"
                else:
                    tex = r"\frac{" + self.tex + r"}{" + other.tex + r"}"
        else:
            value = self.value / other
            if self.parentheses:
                tex = r"\frac{\left( " + self.tex + r" \right)}{" + str(other) + r"}"
            else:
                tex = r"\frac{" + self.tex + r"}{" + str(other) + r"}"
        return Calc(x=value, tex=tex, parentheses=False)

    def __pow__(self, other):
        if isinstance(other, Calc):
            value = self.value**other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"{\left( " + self.tex + r"\right)}^{\left( " + other.tex + r"\right)}"
                else:
                    tex = r"{\left( " + self.tex + r"\right)}^{ " + other.tex + r"}"
            else:
                if other.parentheses:
                    tex = r"{" + self.tex + r"}^{\left( " + other.tex + r"\right)}"
                else:
                    tex = r"{" + self.tex + r"}^{ " + other.tex + r"}"
        else:
            value = self.value**other
            if self.parentheses:
                if other == 0.5:
                    tex = r"\sqrt{" + self.tex + r"}"
                else:
                    tex = r"{\left( " + self.tex + r"\right)}^{ " + str(other) + r"}"
            else:
                tex = r"{" + self.tex + r"}^{ " + str(other) + r"}"
        return Calc(x=value, tex=tex, parentheses=False)

    def __radd__(self, other):
        if isinstance(other, Calc):
            value = other.value + self.value
            tex = other.tex + " + " + self.tex
        else:
            value = self.value + other
            tex = str(other) + "%s + %s" + self.tex
        return Calc(x=value, tex=tex, parentheses=True)

    def __rsub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            tex = other.tex + " - " + self.tex
        else:
            value = other - self.value
            tex = str(other) + "%s - %s" + self.tex
        return Calc(x=value, tex=tex, parentheses=True)

    def __rmul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\left( " + other.tex + r" \right) \times \left( " + self.tex.tex + r" \right)"
                else:
                    tex = r"\left( " + other.tex + " \right) \times " + self.tex.tex
            else:
                if other.parentheses:
                    tex = other.tex + r" \times \left( " + self.tex.tex + r" \right)"
                else:
                    tex = other.tex + r" \times " + self.tex.tex
        else:
            value = self.value * other
            if self.parentheses:
                tex = r"\left( " + other + r" \right) \times " + self.tex
            else:
                tex = other + r" \times " + self.tex
        return Calc(x=value, tex=tex, parentheses=False)

    def __rtruediv__(self, other):
        if isinstance(other, Calc):
            value = self.value / other.value
            if self.parentheses:
                if other.parentheses:
                    tex = r"\frac{\left( " + other.tex + r" \right)}{\left( " + self.tex.tex + r" \right)}"
                else:
                    tex = r"\frac{\left( " + other.tex + r" \right)}{" + self.tex.tex + r"}"
            else:
                if other.parentheses:
                    tex = r"\frac{" + other.tex + r"}{\left( " + self.tex.tex + r" \right)}"
                else:
                    tex = r"\frac{" + other.tex + r"}{" + self.tex.tex + r"}"
        else:
            value = self.value / other
            if self.parentheses:
                tex = r"\frac{\left( " + str(other) + r" \right)}{" + self.tex + r"}"
            else:
                tex = r"\frac{" + str(other) + r"}{" + self.tex + r"}"
        return Calc(x=value, tex=tex, parentheses=False)

    def __repr__(self):
        return str(self.tex)

    def latex(self, variable=""):
        if isinstance(self.value, (Value, int, float)):
            result = self.value
        else:
            result = self.value[0]
        latex = r"""\begin{align*}
   %s &= %s \\
    &= %s
\end{align*}""" % (variable, self.tex, result)
        return latex
    def clear(self):
        self.tex = ""