![img](examples/SolSet.png)

```python
import re
```


# Interval library in Python

Эта библиотека реализует общие [операции](https://ru.wikipedia.org/wiki/Интервальная_арифметика) над интервальными 
величинами, визуализацию множества решений, а также некоторые способы решения как линейных, так и нелинейных систем.

Подробности см. в полной документации по [API](https://intvalpy.readthedocs.io/ru/latest/index.html).

## Установка

Убедитесь, что у вас есть все общесистемные зависимости, затем установите сам модуль:
```
pip install intvalpy
```

## Примеры

### Визуализация множества решений

Мы можем вычислить список вершин выпуклого множества, описанного системой ``A * x >= b`` (в случае точечных данных) или 
``A * x = b`` (в интервальном случае), а также визуализировать это множество:

```python
import numpy as np

A1 = np.array([1,2,3])
```
![alt text](examples/SolSet.png "Solution Set")


Ссылки
-----

* [Домашняя страница](<https://github.com/Maestross/intvalpy>)
* [Онлайн документация](<https://intvalpy.readthedocs.io/ru/latest/#>)
* [Пакет на PyPI](<https://pypi.org/project/intvalpy/>)
* [Теория](<http://www.nsc.ru/interval/Library/InteBooks/SharyBook.pdf>)