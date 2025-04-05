# Minetest Analysis Tools

Набор инструментов для анализа и визуализации данных миров Minetest. Включает анализ структуры мира, метаданных и визуализацию статистики.

## Возможности

### 1. Анализ структуры мира (`world_analyzer.py`)
- Анализ распределения блоков в мире
- Визуализация тепловой карты мира
- Статистика подземных/наземных блоков
- Расчет размера мира и количества блоков

### 2. Анализ метаданных (`metadata_analyzer.py`)
- Анализ конфигурации мира
- Визуализация зависимостей модов
- Анализ игрового времени
- Создание отчетов в формате Markdown

## Установка

```bash
# Клонирование репозитория
git clone https://github.com/yourusername/minetest-tools.git
cd minetest-tools

# Установка зависимостей
pip install numpy matplotlib networkx seaborn
```

## Использование

### Анализ мира

```python
from world_analyzer import MinetestWorldAnalyzer

analyzer = MinetestWorldAnalyzer("path/to/world")
stats = analyzer.analyze_world()
analyzer.visualize_world(stats)
```

### Анализ метаданных

```python
from metadata_analyzer import MinetestMetadataAnalyzer

analyzer = MinetestMetadataAnalyzer("path/to/world")
report = analyzer.create_world_report()
analyzer.visualize_mod_dependencies(analyzer.parse_world_mt())
```

## Математические формулы и алгоритмы

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

## Визуализация

### 1. Тепловая карта мира
- Использует matplotlib для создания 2D визуализации плотности блоков
- Цветовая схема 'hot' для отображения концентрации блоков
- Оси X и Z представляют координаты чанков

### 2. Круговая диаграмма распределения
- Отображает соотношение подземных и наземных блоков
- Использует автоматическое вычисление процентов
- Включает легенду и метки

### 3. Граф зависимостей модов
- Использует networkx для визуализации связей между модами
- Узлы представляют моды
- Рёбра показывают зависимости
- Применяется spring layout для оптимального расположения

## Структура проекта

```
minetest_tools/
├── world_analyzer.py    # Анализ структуры мира
├── metadata_analyzer.py # Анализ метаданных
└── README.md           # Документация
```

## Требования

- Python 3.7+
- numpy
- matplotlib
- networkx
- configparser

## Лицензия

MIT

## Автор

Ваше имя 
