from src import Value
from src.unit import nano, m, s, mili, N, Pa, L, K
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
a = Value(1, nano * s)
assert(a.totex(4) == r'1.000\mathrm{ns}')
assert(a.expect(s).totex(2) == r'1.0\times 10^{-9}\mathrm{s}')
a = Value(1, L)
assert(str(a.expect(m)) == r'<0.001 <m3>>')

print('OK')


minute = (60 * s)('min')
print(Value(120, s).expect(minute))  # 2min

# celcius = (273 + K)('℃')
# Value(300, K).expect(celcius)  # 27celcius

