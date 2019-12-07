# CalcTeX(開発中)

```py
lambda_ = Calc([Value(300, m), Value(400, m)])
# [300, 400]*m
300 * m
f = Calc([Value(170, Hz), Value(340, Hz)])

v = f * lambda_  # Calc
print(v.tex(['v_1', 'v_2'])[0])  # 'v_1 = ...'
print(v.value())
```