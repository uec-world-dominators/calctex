import math


def toexp(e):
    '''
    累乗
    '''
    return f'\\times 10^{{{e}}}' if e else ''


def round_at(value, significant):
    '''
    指定桁数で丸める
    '''
    return str(round(value, (significant - 1) or None))


def zero_padding(significant, main):
    '''
    有効数字までゼロ埋め
    '''
    return "0" * (significant - len(main))


def dot(significant, main):
    '''
    「.」の付加
    '''
    return "." * (significant != 1 and len(main) == 1)


def roundtex(value, significant=1):
    '''
    有効数字を考慮したTeX形式に変換
    '''
    assert(significant > 0)
    digits = math.floor(math.log10(value) + (value < 0)) if value else 0
    main = round_at(value * 10 ** -digits, significant)
    return main + dot(significant, main) + zero_padding(significant, main) + toexp(digits)
