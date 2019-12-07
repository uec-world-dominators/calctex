from src import *


# Unit
assert(str((nano*m*s)/(mili*m)) == r'<s>')
assert(str(nano*N*Pa*m) == r'<nkg2ms-4>')
assert(str((nano*N*Pa*m**-1).expect((mili*Pa)('mPa'), N).to_expr(tex=True))
       == r'\mathrm{mPaNm^{-1}}')

# Value
a = Value(1, nano * s)
assert(a.totex(4) == r'1.000\mathrm{ns}')
assert(a.expect(s).totex(2) == r'1.0\times 10^{-9}\mathrm{s}')

print('OK')
