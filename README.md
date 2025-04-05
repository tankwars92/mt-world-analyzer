
### 1. Декодирование позиции блока

Позиция блока в Minetest хранится как хэш. Алгоритм декодирования:

```math
x = unsigned\_to\_signed(pos \bmod 4096, 2048)
pos_1 = (pos - x) \div 4096
y = unsigned\_to\_signed(pos_1 \bmod 4096, 2048)
pos_2 = (pos_1 - y) \div 4096
z = unsigned\_to\_signed(pos_2 \bmod 4096, 2048)
```

где `unsigned_to_signed(i, max_positive)`:
```math
f(i, max\_positive) = \begin{cases} 
i & \text{если } i < max\_positive \\
i - 2 \times max\_positive & \text{иначе}
\end{cases}
```

### 2. Статистика мира

#### Плотность блоков
```math
density_{chunk} = \frac{blocks_{chunk}}{16 \times 16 \times 16}
```

#### Процент подземных блоков
```math
underground\_ratio = \frac{blocks_{underground}}{blocks_{total}} \times 100\%
```

#### Размер мира в мегабайтах
```math
size_{MB} = \frac{size_{bytes}}{1024 \times 1024}
```

### 3. Расчет игрового времени

#### Время в минутах
```math
time_{minutes} = \frac{game\_time}{20 \times 60}
```

#### Время дня в часах
```math
time_{hours} = \frac{time\_of\_day}{24000} \times 24
```
