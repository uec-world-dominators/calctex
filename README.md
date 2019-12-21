```
  .oooooo.             oooo            ooooooooooooo           ooooooo  ooooo 
 d8P'  `Y8b            `888            8'   888   `8            `8888    d8'  
888           .oooo.    888   .ooooo.       888       .ooooo.     Y888..8P    
888          `P  )88b   888  d88' `"Y8      888      d88' `88b     `8888'     
888           .oP"888   888  888            888      888ooo888    .8PY888.    
`88b    ooo  d8(  888   888  888   .o8      888      888    .o   d8'  `888b   
 `Y8bood8P'  `Y888""8o o888o `Y8bod8P'     o888o     `Y8bod8P' o888o  o88888o 
```

# CalcTeX

![](https://github.com/uec-world-dominators/calctex/workflows/Python%20package%20CI/badge.svg)

## `Calc`

## `Value`
```py
from calctex.unit import N, m, Pa
f = 40 & N | 3     # 力   4.00 N     有効数字3桁
s = 2 & m**2 | 4  # 面積 2.000 m^2  有効数字4桁

p = f / s         # 圧力

print(p.tex())
# 2.00 \times 10\,\mathrm{kg \cdot m^{-1} \cdot s^{-2}}
print(p.expect(Pa).tex())
# 2.00 \times 10\,\mathrm{Pa}
```

## `Unit`
```py
from calctex.unit import *

print(N == kg*m*s**-2)
# True
print(Pa == N/m**2)
# True
```

## `roundtex`
```py
from calctex.common import roundtex

print(roundtex(100, significant=2))
# 1.0 \times 10^{2}
```