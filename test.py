import numpy as np
import math
from calctex.calc import Calc
from calctex.helper import decimal_point, multi, c
from calctex.helper import from_strs
from calctex.view import to_markdown_table, to_tex_table
from calctex.common import roundtex
from calctex import constants
from calctex import unit
from calctex import Value
from calctex.unit.basic import *
assert(('m_' in locals()) == True)
assert(('Pa_' in locals()) == False)


# Common
assert(roundtex(10, 2) == r'1.0 \times 10')
assert(roundtex(0, 1) == r'0')
assert(roundtex(3, 1) == r'3')
assert(roundtex(0, 4) == r'0.000')
assert(roundtex(1, 4) == r'1.000')
assert(roundtex(0.1, 4) == r'1.000 \times 10^{-1}')
assert(roundtex(203, 2) == r'2.0 \times 10^{2}')
assert(roundtex(0.99366103, 4) == r'9.937 \times 10^{-1}')

# Unit
assert(str(unit.fahrenheit_) == r'<°F>')
assert(str((unit.nano_ * unit.m_ * unit.s_) / (unit.mili_ * unit.m_)) == r'<μs>')
assert(str(unit.nano_ * unit.N_ * unit.Pa_ * unit.m_) == r'<nkg2ms-4>')
assert(str((unit.nano_ * unit.N_ * unit.Pa_ * unit.m_ ** -1)
           .expect((unit.mili_ * unit.Pa_)('mPa'), unit.N_).to_expr(tex=True)) == r'\mathrm{\mumPa \cdot N \cdot m^{-1}}')

# Value
assert(str(Value(1, unit.mili_ * unit.s_).expect(unit.s_)) == r'<0.001 <s>>')
a = Value(1, unit.nano_ * unit.s_)
assert(a.tex(4) == r'1.000 \,\mathrm{ns}')
assert(a.expect(unit.s_).tex(2) == r'1.0 \times 10^{-9} \,\mathrm{s}')
assert(str(Value(1, unit.L_).expect(unit.m_)) == r'<0.001 <m3>>')

# SI併用坘佝
assert(str(Value(1, unit.minute_) - Value(50, unit.s_)) == r'<10.0 <s>>')
assert(str((Value(3600, unit.s_) + Value(0.5, unit.h_)).expect(unit.minute_)) == r'<90.0 <min>>')
assert(str((Value(300, unit.K_) - Value(27, unit.celcius_)).expect(unit.celcius_)) == r'<-273 <℃>>')
assert(str(Value(0, unit.fahrenheit_).expect(unit.K_)) == r'<255.37222222222223 <K>>')
assert(str(Value(60, unit.arc_minute_).expect(unit.arc_degree_) == r'<1.0 <°>>'))
assert(str(Value(1.0, unit.L_).expect(unit.m_)) == r'<0.001 <m3>>')

# スケール㝮入㝣㝟坘佝㝧expect
assert(str(Value(1.0, unit.m_).expect((unit.mili_ * unit.m_)('mm'))) == r'<1000.0 <mm>>')
assert(str(Value(1.0, unit.L_).expect(unit.L_)) == r'<1.0 <L>>')

# Tex
assert(unit.m_.tex() == r'\mathrm{m}')
assert(Value(1, unit.m_).tex(unit=False) == r'1')
assert(Value(1, unit.m_).tex() == r'1 \,\mathrm{m}')
assert(Value(1, unit.m_).tex(significant=3) == r'1.00 \,\mathrm{m}')

# View
assert(to_markdown_table([[1, 2], [2, 3]], ['a', 'b']) == '''|a   |b   |\n|----|----|\n|1   |2   |\n|2   |3   |''')
assert(to_tex_table(np.array([[1, 2], [2, 3]]), ['a', 'b']) == '''a & b \\\\\n1 & 2 \\\\\n2 & 3 \\\\''')
assert(to_tex_table(np.array([[1, 2], [2, 3]])) == '''1 & 2 \\\\\n2 & 3 \\\\''')
assert(list(map(lambda e: e.tex(), from_strs(['1.2', '12', '0.12']))) == ['1.2', '1.2 \\times 10', '1.20 \\times 10^{-1}'])
assert(to_markdown_table([[1, 2, 3], [4, 5, 6]], ['a', 'b'], transpose=True, row_header=[1, 2, 3])=='''|    |a   |b   |
|----|----|----|
|1   |1   |4   |
|2   |2   |5   |
|3   |3   |6   |''')

# Calc
assert(str(c(45, unit.m_, sig_figs=2)) == r'4.5 \times 10 \,\mathrm{m}')
a = c(['1', '2.3', '4'], unit.m_, symbol='d')
b = c(40, unit.m_, 4, symbol='H')
y = c(1, unit.m_, symbol='y')
pi = c(math.pi, symbol='\\pi')
assert((pi * (a + b)).symbol() == r'\pi \, \left( d + H \right)')
assert((y * (a + b)).tex()[0] ==
       '\\begin{align*}\n    &= 1 \,\mathrm{m} \\times \left( 1 \,\mathrm{m} + 4.000 \\times 10 \,\mathrm{m} \\right) \\\\\n    &= 4 \\times 10 \,\mathrm{m^{2}}\n\end{align*}')
assert(str('3.4' & unit.m_) == r'<3.4 <m>>')

print('OK')

