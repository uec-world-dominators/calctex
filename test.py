from src import Value
from src import unit
from src.common import roundtex


# Common
assert(roundtex(0, 1) == r'0')
assert(roundtex(0, 4) == r'0.000')
assert(roundtex(1, 4) == r'1.000')
assert(roundtex(203, 2) == r'2.0\times 10^{2}')
assert(roundtex(0.99366103, 4) == r'9.937\times 10^{-1}')

# Unit
assert(str((unit.nano * unit.m * unit.s) / (unit.mili * unit.m)) == r'<μs>')
assert(str(unit.nano * unit.N * unit.Pa * unit.m) == r'<nkg2ms-4>')
assert(str((unit.nano * unit.N * unit.Pa * unit.m ** -1)
           .expect((unit.mili * unit.Pa)('mPa'), unit.N).to_expr(tex=True)) == r'\mathrm{\mumPa\cdotN\cdotm^{-1}}')

# Value
assert(str(Value(1, unit.mili * unit.s).expect(unit.s)) == r'<0.001 <s>>')
a = Value(1, unit.nano * unit.s)
assert(a.tex(4) == r'1.000\,\mathrm{ns}')
assert(a.expect(unit.s).tex(2) == r'1.0\times 10^{-9}\,\mathrm{s}')
assert(str(Value(1, unit.L).expect(unit.m)) == r'<0.001 <m3>>')

# SI併用単位
assert(str(Value(1, unit.minute) - Value(50, unit.s)) == r'<10.0 <s>>')
assert(str((Value(3600, unit.s) + Value(0.5, unit.h)).expect(unit.minute)) == r'<90.0 <min>>')
assert(str((Value(300, unit.K) - Value(27, unit.celcius)).expect(unit.celcius)) == r'<-273 <℃>>')
assert(str(Value(0, unit.fahrenheit).expect(unit.K)) == r'<255.37222222222223 <K>>')
assert(str(Value(60, unit.arc_minute).expect(unit.arc_degree) == r'<1.0 <°>>'))
assert(str(Value(1.0, unit.L).expect(unit.m)) == r'<0.001 <m3>>')

print('OK')
