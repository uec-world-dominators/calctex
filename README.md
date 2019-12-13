```
  .oooooo.             oooo            ooooooooooooo           ooooooo  ooooo 
 d8P'  `Y8b            `888            8'   888   `8            `8888    d8'  
888           .oooo.    888   .ooooo.       888       .ooooo.     Y888..8P    
888          `P  )88b   888  d88' `"Y8      888      d88' `88b     `8888'     
888           .oP"888   888  888            888      888ooo888    .8PY888.    
`88b    ooo  d8(  888   888  888   .o8      888      888    .o   d8'  `888b   
 `Y8bood8P'  `Y888""8o o888o `Y8bod8P'     o888o     `Y8bod8P' o888o  o88888o 
```

# CalcTeX(開発中)


![](https://github.com/uec-world-dominators/calctex/workflows/Python%20package%20CI/badge.svg)

```py
lambda_ = Calc([Value(300, m), Value(400, m)])
# [300, 400]*m
300 * m
f = Calc([Value(170, Hz), Value(340, Hz)])

v = f * lambda_  # Calc
print(v.tex(['v_1', 'v_2'])[0])  # 'v_1 = ...'
print(v.value())
```