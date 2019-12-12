from src import Value
from src.unit import nano, m, s, mili, N, Pa, L, K, celcius, arc_degree, arc_minute, arc_second, minute, h
from src import unit
from src.common import roundtex

# Common
assert(roundtex(0, 1) == r'0')
assert(roundtex(0, 4) == r'0.000')
assert(roundtex(1, 4) == r'1.000')
assert(roundtex(203, 2) == r'2.0\times 10^{2}')
assert(roundtex(0.99366103, 4) == r'9.937\times 10^{-1}')


# Unit
assert(str((nano * m * s) / (mili * m)) == r'<μs>')
assert(str(nano * N * Pa * m) == r'<nkg2ms-4>')
assert(str((nano * N * Pa * m ** -1).expect((mili * Pa)('mPa'), N).to_expr(tex=True)) == r'\mathrm{\mumPaNm^{-1}}')

# Value
assert(str(Value(1, mili*s).expect(s)) == r'<0.001 <s>>')
a = Value(1, nano * s)
assert(a.totex(4) == r'1.000\mathrm{ns}')
assert(a.expect(s).totex(2) == r'1.0\times 10^{-9}\mathrm{s}')
a = Value(1, L)
assert(str(a.expect(m)) == r'<0.001 <m3>>')

# SI併用単位
a = Value(300, K)
b = Value(27, celcius)
assert(str((a-b).expect(celcius)) == r'<-273.0 <℃>>')

a = Value(1, minute)
b = Value(50, s)
assert(str(a-b) == r'<10 <s>>')

a = Value(3600, s)
b = Value(0.5, h)
assert(str((a+b).expect(minute)) == r'<90.0 <min>>')

print('OK')


a = Value(60, arc_minute)
print(a.expect(arc_degree))

a = Value(0, unit.fahrenheit)
print(a.expect(K('K')))
