# %%
from .common import roundtex
from .value import Value
from numpy import ndarray
import numpy as np
from .unit import *


class Calc:
    def __init__(self, x, parentheses=False, raw="", symbol=""):
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
        if isinstance(raw, ndarray) or raw:
            self.raw = raw
        else:
            if isinstance(x, Value):
                self.raw = self.value.tex()
            elif isinstance(x, ndarray):
                self.raw = np.array(self.raw(), dtype="object")
        self.parentheses = parentheses
        self._symbol = symbol or (self.value.tex() if isinstance(self.value, Value) else '<no symbol>')

    def raw(self):
        if isinstance(self.value, Value):
            return self.value.tex()
        elif isinstance(self.value, ndarray):
            return [i.tex() for i in self.value]

    def __add__(self, other):
        if isinstance(other, Calc):
            value = np.add(self.value, other.value)
            raw = self.raw + " + " + other.raw
            symbol = self._symbol + " + " + other._symbol
        else:
            value = np.add(self.value, other)
            raw = self.raw + " + " + str(other)
            symbol = self._symbol + " + " + str(other)
        return Calc(x=value, raw=raw, parentheses=True, symbol=symbol)

    def __sub__(self, other):
        if isinstance(other, Calc):
            value = np.subtract(self.value, other.value)
            raw = self.raw + " - " + other.raw
            symbol = self._symbol + " - " + other._symbol
        else:
            value = np.subtract(self.value, other)
            symbol = self._symbol + " - " + str(other)
        return Calc(x=value, raw=raw, parentheses=True, symbol=symbol)

    def __mul__(self, other):
        if isinstance(other, Calc):
            value = np.multiply(self.value, other.value)
            if self.parentheses:
                if other.parentheses:
                    raw = r"\left( " + self.raw + r" \right) \times \left( " + other.raw + r" \right)"
                    symbol = r"\left( " + self._symbol + r" \right) \, \left( " + other._symbol + r" \right)"
                else:
                    raw = r"\left( " + self.raw + r" \right) \times " + other.raw
                    symbol = r"\left( " + self._symbol + r" \right) \, " + other._symbol
            else:
                if other.parentheses:
                    raw = self.raw + r" \times \left( " + other.raw + r" \right)"
                    symbol = self._symbol + r" \, \left( " + other._symbol + r" \right)"
                else:
                    raw = self.raw + r" \times " + other.raw
                    symbol = self._symbol + r" \, " + other._symbol
        else:
            value = np.multiply(self.value, other)
            if self.parentheses:
                raw = r"\left( " + self.raw + r" \right) \times " + str(other)
                symbol = r"\left( " + self._symbol + r" \right) \, " + str(other)
            else:
                raw = self.raw + r" \times " + str(other)
                symbol = self._symbol + r" \, " + str(other)
        return Calc(x=value, raw=raw, parentheses=False, symbol=symbol)

    def __truediv__(self, other):
        if isinstance(other, Calc):
            value = np.true_divide(self.value, other.value)
            if self.parentheses:
                if other.parentheses:
                    raw = r"\frac{\left( " + self.raw + r" \right)}{\left( " + other.raw + r" \right)}"
                    symbol = r"\frac{\left( " + self._symbol + r" \right)}{\left( " + other._symbol + r" \right)}"
                else:
                    raw = r"\frac{\left( " + self.raw + r" \right)}{" + other.raw + r"}"
                    symbol = r"\frac{\left( " + self._symbol + r" \right)}{" + other._symbol + r"}"
            else:
                if other.parentheses:
                    raw = r"\frac{" + self.raw + r"}{\left( " + other.raw + r" \right)}"
                    symbol = r"\frac{" + self._symbol + r"}{\left( " + other._symbol + r" \right)}"
                else:
                    raw = r"\frac{" + self.raw + r"}{" + other.raw + r"}"
                    symbol = r"\frac{" + self._symbol + r"}{" + other._symbol + r"}"
        else:
            value = np.true_divide(self.value, other)
            if self.parentheses:
                raw = r"\frac{\left( " + self.raw + r" \right)}{" + str(other) + r"}"
                symbol = r"\frac{\left( " + self._symbol + r" \right)}{" + str(other) + r"}"
            else:
                raw = r"\frac{" + self.raw + r"}{" + str(other) + r"}"
                symbol = r"\frac{" + self._symbol + r"}{" + str(other) + r"}"
        return Calc(x=value, raw=raw, parentheses=False, symbol=symbol)

    def __pow__(self, other):
        if isinstance(other, Calc):
            value = np.power(self.value, other.value)
            if self.parentheses:
                if other.parentheses:
                    raw = r"{\left( " + self.raw + r"\right)}^{\left( " + other.raw + r"\right)}"
                    symbol = r"{\left( " + self._symbol + r"\right)}^{\left( " + other._symbol + r"\right)}"
                else:
                    raw = r"{\left( " + self.raw + r"\right)}^{ " + other.raw + r"}"
                    symbol = r"{\left( " + self._symbol + r"\right)}^{ " + other._symbol + r"}"
            else:
                if other.parentheses:
                    raw = r"{" + self.raw + r"}^{\left( " + other.raw + r"\right)}"
                    symbol = r"{" + self._symbol + r"}^{\left( " + other._symbol + r"\right)}"
                else:
                    raw = r"{" + self.raw + r"}^{" + other.raw + r"}"
                    symbol = r"{" + self._symbol + r"}^{" + other._symbol + r"}"
        else:
            value = np.power(self.value, other)
            if self.parentheses:
                if other == 0.5:
                    raw = r"\sqrt{" + self.raw + r"}"
                    symbol = r"\sqrt{" + self._symbol + r"}"
                else:
                    raw = r"{\left( " + self.raw + r"\right)}^{ " + str(other) + r"}"
                    symbol = r"{\left( " + self._symbol + r"\right)}^{ " + str(other) + r"}"
            else:
                raw = r"{" + self.raw + r"}^{ " + str(other) + r"}"
                symbol = r"{" + self._symbol + r"}^{ " + str(other) + r"}"
        return Calc(x=value, raw=raw, parentheses=False, symbol=symbol)

    def __radd__(self, other):
        if isinstance(other, Calc):
            value = np.add(other.value, self.value)
            raw = other.raw + " + " + self.raw
            symbol = other._symbol + " + " + self._symbol
        else:
            value = np.add(self.value, other)
            raw = str(other) + " + " + self.raw
            symbol = str(other) + " + " + self._symbol
        return Calc(x=value, raw=raw, parentheses=True, symbol=symbol)

    def __rsub__(self, other):
        if isinstance(other, Calc):
            value = np.subtract(self.value, other.value)
            raw = other.raw + " - " + self.raw
            symbol = other._symbol + " - " + self._symbol
        else:
            value = np.subtract(other, self.value)
            raw = str(other) + " - " + self.raw
            symbol = str(other) + " - " + self._symbol
        return Calc(x=value, raw=raw, parentheses=True)

    def __rmul__(self, other):
        if isinstance(other, Calc):
            value = np.multiply(self.value, other.value)
            if self.parentheses:
                if other.parentheses:
                    raw = r"\left( " + other.raw + r" \right) \times \left( " + self.raw + r" \right)"
                    symbol = r"\left( " + other._symbol + r" \right) \, \left( " + self._symbol + r" \right)"
                else:
                    raw = r"\left( " + other.raw + r" \right) \times " + self.raw
                    symbol = r"\left( " + other._symbol + r" \right) \, " + self._symbol
            else:
                if other.parentheses:
                    raw = other.raw + r" \times \left( " + self.raw + r" \right)"
                    symbol = other._symbol + r" \, \left( " + self._symbol + r" \right)"
                else:
                    raw = other.raw + r" \times " + self.raw
                    symbol = other._symbol + r" \, " + self._symbol
        else:
            value = np.multiply(self.value, other)
            if self.parentheses:
                raw = r"\left( " + other + r" \right) \times " + self.raw
                symbol = r"\left( " + other + r" \right) \, " + self._symbol
            else:
                raw = other + r" \times " + self.raw
                symbol = other + r" \, " + self._symbol
        return Calc(x=value, raw=raw, parentheses=False, symbol=symbol)

    def __rtruediv__(self, other):
        if isinstance(other, Calc):
            value = np.true_divide(other.value, self.value)
            if self.parentheses:
                if other.parentheses:
                    raw = r"\frac{\left( " + other.raw + r" \right)}{\left( " + self.raw + r" \right)}"
                    symbol = r"\frac{\left( " + other._symbol + r" \right)}{\left( " + self._symbol + r" \right)}"
                else:
                    raw = r"\frac{\left( " + other.raw + r" \right)}{" + self.raw + r"}"
                    symbol = r"\frac{\left( " + other._symbol + r" \right)}{" + self._symbol + r"}"
            else:
                if other.parentheses:
                    raw = r"\frac{" + other.raw + r"}{\left( " + self.raw + r" \right)}"
                    symbol = r"\frac{" + other._symbol + r"}{\left( " + self._symbol + r" \right)}"
                else:
                    raw = r"\frac{" + other.raw + r"}{" + self.raw + r"}"
                    symbol = r"\frac{" + other._symbol + r"}{" + self._symbol + r"}"
        else:
            value = np.true_divide(other, self.value)
            if self.parentheses:
                raw = r"\frac{\left( " + str(other) + r" \right)}{" + self.raw + r"}"
                symbol = r"\frac{\left( " + str(other) + r" \right)}{" + self._symbol + r"}"
            else:
                raw = r"\frac{" + str(other) + r"}{" + self.raw + r"}"
                symbol = r"\frac{" + str(other) + r"}{" + self._symbol + r"}"
        return Calc(x=value, raw=raw, parentheses=False, symbol=symbol)

    def __repr__(self):
        return str(self.raw)

    def md(self):
        def _format_md(raw, result):
            return f"$$\n    {raw} \n    = {result}\n$$\n"
        if isinstance(self.value, Value):
            return _format_md(self.raw, self.value.tex())
        else:
            return [_format_md(raw, value.tex()) for raw, value
                    in zip(self.raw, self.value)]

    def result(self):
        return self.value

    def tex(self, variable="", output="all"):
        if isinstance(self.value, (Value, int, float)):
            result = self.value
            tex = r"""\begin{align*}
   %s &= %s \\
    &= %s
\end{align*}""" % (variable, self.raw, result.tex())
            return tex
        else:
            if output == "first":
                result = self.value[0]
                tex = r"""\begin{align*}
   %s &= %s \\
    &= %s
\end{align*}""" % (variable, self.raw[0], result.tex())
                return tex
            if output == "all":
                result = [i for i in self.value]
                tex = [r"""\begin{align*}
   %s &= %s \\
    &= %s
\end{align*}""" % (variable, i, j.tex()) for i, j in zip(self.raw, result)]
                return tex

    def clear(self):
        self.raw = ""

    def __call__(self, symbol):
        self.symbol = symbol
        return self

    def symbol(self):
        return self._symbol
