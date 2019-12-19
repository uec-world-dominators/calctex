#%%
from src.common import roundtex
from src.value import Value
from numpy import ndarray
import numpy as np
from src.unit import *

class Calc:
    def __init__(self, x, parentheses=False, raw=""):
        import numpy as np
        from numpy import ndarray
        if isinstance(x, (Value, ndarray)):
            x = x
        elif isinstance(x, (int, float)):
            x = Value(x)
        elif isinstance(x, list):
            x = np.array([Value(i) if isinstance(i, (int, float)) else i for i in x])
        else:
            raise ValueError("error!")
        self.value = x
        if raw:
            self.raw = raw
        else:
            if isinstance(x, Value):
                self.raw = self.value.tex()
            elif isinstance(x, ndarray):
                self.raw = np.array(self.raw())
        self.parentheses = parentheses

    def raw(self):
        if isinstance(self.value, Value):
            return self.value.tex()
        elif isinstance(self.value, ndarray):
            return [i.tex() for i in self.value]

    def __add__(self, other):
        if isinstance(other, Calc):
            value = self.value + other.value
            raw = self.raw + " + " + other.raw
        else:
            value = self.value + other
            raw = self.raw + " + " + str(other)
        return Calc(x=value, raw=raw, parentheses=True)

    def __sub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            raw = self.raw + " - " + other.raw
        else:
            value = self.value - other
            raw = self.raw + " - " + str(other)
        return Calc(x=value, raw=raw, parentheses=True)

    def __mul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            if self.parentheses:
                if other.parentheses:
                    raw = r"\left( " + self.raw + r" \right) \times \left( " + other.raw + r" \right)"
                else:
                    raw = r"\left( " + self.raw + r" \right) \times " + other.raw
            else:
                if other.parentheses:
                    raw = self.raw + r" \times \left( " + other.raw + r" \right)"
                else:
                    raw = self.raw + r" \times " + other.raw
        else:
            value = self.value * other
            if self.parentheses:
                raw = r"\left( " + self.raw + r" \right) \times " + str(other)
            else:
                raw = self.raw + r" \times " + str(other)
        return Calc(x=value, raw=raw, parentheses=False)

    def __truediv__(self, other):
        if isinstance(other, Calc):
            value = self.value / other.value
            if self.parentheses:
                if other.parentheses:
                    raw = r"\frac{\left( " + self.raw + r" \right)}{\left( " + other.raw + r" \right)}"
                else:
                    raw = r"\frac{\left( " + self.raw + r" \right)}{" + other.raw + r"}"
            else:
                if other.parentheses:
                    raw = r"\frac{" + self.raw + r"}{\left( " + other.raw + r" \right)}"
                else:
                    raw = r"\frac{" + self.raw + r"}{" + other.raw + r"}"
        else:
            value = self.value / other
            if self.parentheses:
                raw = r"\frac{\left( " + self.raw + r" \right)}{" + str(other) + r"}"
            else:
                raw = r"\frac{" + self.raw + r"}{" + str(other) + r"}"
        return Calc(x=value, raw=raw, parentheses=False)

    def __pow__(self, other):
        if isinstance(other, Calc):
            value = self.value**other.value
            if self.parentheses:
                if other.parentheses:
                    raw = r"{\left( " + self.raw + r"\right)}^{\left( " + other.raw + r"\right)}"
                else:
                    raw = r"{\left( " + self.raw + r"\right)}^{ " + other.raw + r"}"
            else:
                if other.parentheses:
                    raw = r"{" + self.raw + r"}^{\left( " + other.raw + r"\right)}"
                else:
                    raw = r"{" + self.raw + r"}^{" + other.raw + r"}"
        else:
            value = self.value**other
            if self.parentheses:
                if other == 0.5:
                    raw = r"\sqrt{" + self.raw + r"}"
                else:
                    raw = r"{\left( " + self.raw + r"\right)}^{ " + str(other) + r"}"
            else:
                raw = r"{" + self.raw + r"}^{ " + str(other) + r"}"
        return Calc(x=value, raw=raw, parentheses=False)

    def __radd__(self, other):
        if isinstance(other, Calc):
            value = other.value + self.value
            raw = other.raw + " + " + self.raw
        else:
            value = self.value + other
            raw = str(other) + "%s + %s" + self.raw
        return Calc(x=value, raw=raw, parentheses=True)

    def __rsub__(self, other):
        if isinstance(other, Calc):
            value = self.value - other.value
            raw = other.raw + " - " + self.raw
        else:
            value = other - self.value
            raw = str(other) + "%s - %s" + self.raw
        return Calc(x=value, raw=raw, parentheses=True)

    def __rmul__(self, other):
        if isinstance(other, Calc):
            value = self.value * other.value
            if self.parentheses:
                if other.parentheses:
                    raw = r"\left( " + other.raw + r" \right) \times \left( " + self.raw + r" \right)"
                else:
                    raw = r"\left( " + other.raw + " \right) \times " + self.raw
            else:
                if other.parentheses:
                    raw = other.raw + r" \times \left( " + self.raw + r" \right)"
                else:
                    raw = other.raw + r" \times " + self.raw
        else:
            value = self.value * other
            if self.parentheses:
                raw = r"\left( " + other + r" \right) \times " + self.raw
            else:
                raw = other + r" \times " + self.raw
        return Calc(x=value, raw=raw, parentheses=False)

    def __rtruediv__(self, other):
        if isinstance(other, Calc):
            value = self.value / other.value
            if self.parentheses:
                if other.parentheses:
                    raw = r"\frac{\left( " + other.raw + r" \right)}{\left( " + self.raw + r" \right)}"
                else:
                    raw = r"\frac{\left( " + other.raw + r" \right)}{" + self.raw + r"}"
            else:
                if other.parentheses:
                    raw = r"\frac{" + other.raw + r"}{\left( " + self.raw + r" \right)}"
                else:
                    raw = r"\frac{" + other.raw + r"}{" + self.raw + r"}"
        else:
            value = self.value / other
            if self.parentheses:
                raw = r"\frac{\left( " + str(other) + r" \right)}{" + self.raw + r"}"
            else:
                raw = r"\frac{" + str(other) + r"}{" + self.raw + r"}"
        return Calc(x=value, raw=raw, parentheses=False)

    def __repr__(self):
        return str(self.raw)

    def tex(self, variable=""):
        if isinstance(self.value, (Value, int, float)):
            result = self.value
        else:
            result = self.value[0]
        tex = r"""\begin{align*}
   %s &= %s \\
    &= %s
\end{align*}""" % (variable, self.raw, result.tex())
        return tex

    def clear(self):
        self.raw = ""