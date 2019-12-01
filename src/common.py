import math

# よくわからないけど動く（さわるな危険）


def roundtex(n, d, exp=False):
    assert(d > 0)
    if n == 0:
        return f"0{('.'+'0'*(d-1)) if d!=1 else ''}"
    elif n >= 1:
        _d = math.floor(math.log10(n))
        s = str(round(n/10**_d, d-1))
        return f'{s}{"0"*(1+d-len(s))}' + (f'\\times 10^{{{_d}}}' if _d != 0 else '')
    else:
        _n = n
        _d = 0
        while True:
            _n *= 10
            _d += 1
            if math.floor(_n) % 10 != 0:
                s = str(round(_n, d-1) if d != 1 else round(_n))
                return f'{s}{"0"*(1+d-len(s)) if d!=1 else ""}' + (f'\\times 10^{{{-_d}}}' if _d != 0 else '')


isinpackage = not __name__ in ['common', '__main__']
if not isinpackage:
    assert(roundtex(1, 4) == r'1.000')
    assert(roundtex(0.99366103, 4) == r'9.937\times 10^{-1}')
    print('OK')
