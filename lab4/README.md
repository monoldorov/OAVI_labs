# Лабораторная работа №4. Выделение контуров на изображении

## Оператор Кайяли, вариант 14

---

## Задачи работы

1. Выполнить преобразование цветного изображения в полутоновое.
2. Рассчитать градиенты изображения по осям (G_x) и (G_y).
3. Получить итоговую градиентную матрицу (G).
4. Выполнить бинаризацию градиентного изображения.

---

## Теоретическая часть

### 1. Контуры на изображении

Контуром называют область изображения, в которой происходит резкое изменение яркости. Обычно такие области соответствуют границам объектов.

Для выделения контуров часто используют методы, основанные на вычислении производных яркости изображения.

### 2. Градиент изображения

Градиент изображения — это вектор, характеризующий изменение яркости по двум направлениям:

```text
G = (Gx, Gy)
```

где:

* `Gx` — изменение яркости по горизонтали;
* `Gy` — изменение яркости по вертикали.

Модуль градиента показывает силу изменения яркости. В общем случае он может вычисляться так:

```text
G = sqrt(Gx^2 + Gy^2)
```

В данной лабораторной используется упрощённая формула:

```text
G = |Gx| + |Gy|
```

Такой способ проще вычислительно и хорошо подходит для выделения контуров.

### 3. Оператор Кайяли 3×3

В лабораторной работе используется оператор Кайяли с двумя ядрами свёртки.

Ядро `Gx`:

| 6  | 0 | -6 |
| -- | - | -- |
| 0  | 0 | 0  |
| -6 | 0 | 6  |

Ядро `Gy`:

| -6 | 0 | 6  |
| -- | - | -- |
| 0  | 0 | 0  |
| 6  | 0 | -6 |

После применения этих ядер к полутоновому изображению получаются две матрицы: `Gx` и `Gy`.

### 4. Формула варианта 14

По условию варианта 14 итоговый градиент вычисляется так:

```text
G = |Gx| + |Gy|
```

Это означает, что для каждого пикселя берётся модуль горизонтального отклика, модуль вертикального отклика, после чего они суммируются.

### 5. Бинаризация

После получения итоговой градиентной матрицы выполняется бинаризация по порогу `T`.

Правило бинаризации:

* если значение пикселя больше порога `T`, то пиксель становится белым;
* иначе пиксель становится чёрным.

В работе использовался порог:

```text
T = 40
```

---

## Структура входных данных

### Цветные изображения

Цветные изображения брались из папки:

[`input/pictures_color_src/`](input/pictures_color_src/)

Файлы:

![Исходное цветное изображение cartoon](input/pictures_color_src/cartoon.png)

![Исходное цветное изображение map](input/pictures_color_src/map.png)

![Исходное цветное изображение photo](input/pictures_color_src/photo.png)

![Исходное цветное изображение text](input/pictures_color_src/text.png)

![Исходное цветное изображение x-ray](input/pictures_color_src/x-ray.png)

---

### Полутоновые изображения

Полутоновые изображения брались из папки:

[`input/pictures_semitone_src/`](input/pictures_semitone_src/)

Файлы:

![Исходное полутоновое изображение cartoon](input/pictures_semitone_src/cartoon_semitone.png)

![Исходное полутоновое изображение map](input/pictures_semitone_src/map_semitone.png)

![Исходное полутоновое изображение photo](input/pictures_semitone_src/photo_semitone.png)

![Исходное полутоновое изображение text](input/pictures_semitone_src/text_semitone.png)

![Исходное полутоновое изображение x-ray](input/pictures_semitone_src/x-ray_semitone.png)

---

## Описание обработки

### 1. results_color_gray / results_semitone_gray

#### Откуда брались данные

* [`input/pictures_color_src/`](input/pictures_color_src/) — цветные изображения переводились в полутоновое представление;
* [`input/pictures_semitone_src/`](input/pictures_semitone_src/) — уже полутоновые изображения использовались как есть.

#### Что получилось

Полутоновые версии всех изображений, приведённые к диапазону яркости `0–255`.

#### Папки с результатами

* [`output/results_color_gray/`](output/results_color_gray/)
* [`output/results_semitone_gray/`](output/results_semitone_gray/)

#### Цветные изображения после перевода в grayscale

![cartoon gray](output/results_color_gray/cartoon_kayyali_gray.png)

![map gray](output/results_color_gray/map_kayyali_gray.png)

![photo gray](output/results_color_gray/photo_kayyali_gray.png)

![text gray](output/results_color_gray/text_kayyali_gray.png)

![x-ray gray](output/results_color_gray/x-ray_kayyali_gray.png)

#### Полутоновые изображения после подготовки

![cartoon semitone gray](output/results_semitone_gray/cartoon_semitone_kayyali_gray.png)

![map semitone gray](output/results_semitone_gray/map_semitone_kayyali_gray.png)

![photo semitone gray](output/results_semitone_gray/photo_semitone_kayyali_gray.png)

![text semitone gray](output/results_semitone_gray/text_semitone_kayyali_gray.png)

![x-ray semitone gray](output/results_semitone_gray/x-ray_semitone_kayyali_gray.png)

#### Вывод

Преобразование в полутон корректно подготавливает данные для градиентного анализа, устраняя цветовую компоненту и оставляя только яркость.

---

### 2. results_color_gx / results_semitone_gx

#### Откуда брались данные

Использовались полутоновые изображения из папок `results_*_gray`.

#### Что получилось

Получены матрицы градиента (G_x), вычисленные свёрткой с ядром Кайяли по оси X.

Визуально результат выглядит как рельефное изображение с акцентом на вертикальные границы.

#### Папки с результатами

* [`output/results_color_gx/`](output/results_color_gx/)
* [`output/results_semitone_gx/`](output/results_semitone_gx/)

#### Результаты для цветных изображений

![cartoon Gx](output/results_color_gx/cartoon_kayyali_gx.png)

![map Gx](output/results_color_gx/map_kayyali_gx.png)

![photo Gx](output/results_color_gx/photo_kayyali_gx.png)

![text Gx](output/results_color_gx/text_kayyali_gx.png)

![x-ray Gx](output/results_color_gx/x-ray_kayyali_gx.png)

#### Результаты для полутоновых изображений

![cartoon semitone Gx](output/results_semitone_gx/cartoon_semitone_kayyali_gx.png)

![map semitone Gx](output/results_semitone_gx/map_semitone_kayyali_gx.png)

![photo semitone Gx](output/results_semitone_gx/photo_semitone_kayyali_gx.png)

![text semitone Gx](output/results_semitone_gx/text_semitone_kayyali_gx.png)

![x-ray semitone Gx](output/results_semitone_gx/x-ray_semitone_kayyali_gx.png)

#### Вывод

Оператор Кайяли по (G_x) корректно выявляет изменения яркости по горизонтали, что приводит к выделению вертикальных контуров.

---

### 3. results_color_gy / results_semitone_gy

#### Откуда брались данные

Использовались полутоновые изображения из папок `results_*_gray`.

#### Что получилось

Получены матрицы градиента (G_y), вычисленные свёрткой с ядром Кайяли по оси Y.

Визуально результат даёт акцент на горизонтальные границы.

#### Папки с результатами

* [`output/results_color_gy/`](output/results_color_gy/)
* [`output/results_semitone_gy/`](output/results_semitone_gy/)

#### Результаты для цветных изображений

![cartoon Gy](output/results_color_gy/cartoon_kayyali_gy.png)

![map Gy](output/results_color_gy/map_kayyali_gy.png)

![photo Gy](output/results_color_gy/photo_kayyali_gy.png)

![text Gy](output/results_color_gy/text_kayyali_gy.png)

![x-ray Gy](output/results_color_gy/x-ray_kayyali_gy.png)

#### Результаты для полутоновых изображений

![cartoon semitone Gy](output/results_semitone_gy/cartoon_semitone_kayyali_gy.png)

![map semitone Gy](output/results_semitone_gy/map_semitone_kayyali_gy.png)

![photo semitone Gy](output/results_semitone_gy/photo_semitone_kayyali_gy.png)

![text semitone Gy](output/results_semitone_gy/text_semitone_kayyali_gy.png)

![x-ray semitone Gy](output/results_semitone_gy/x-ray_semitone_kayyali_gy.png)

#### Вывод

Оператор Кайяли по (G_y) выявляет изменения яркости по вертикали, что дополняет информацию о контурах, полученную из (G_x).

---

### 4. results_color_gradient / results_semitone_gradient

#### Откуда брались данные

Использовались матрицы (G_x) и (G_y).

#### Что получилось

Получена итоговая градиентная матрица:

```text
G = |Gx| + |Gy|
```

Значения нормализованы в диапазон `0–255`.

Яркие области соответствуют сильным границам.

#### Папки с результатами

* [`output/results_color_gradient/`](output/results_color_gradient/)
* [`output/results_semitone_gradient/`](output/results_semitone_gradient/)

#### Результаты для цветных изображений


![cartoon gradient](output/results_color_gradient/cartoon_kayyali_gradient.png)

![map gradient](output/results_color_gradient/map_kayyali_gradient.png)

![photo gradient](output/results_color_gradient/photo_kayyali_gradient.png)

![text gradient](output/results_color_gradient/text_kayyali_gradient.png)

![x-ray gradient](output/results_color_gradient/x-ray_kayyali_gradient.png)

#### Результаты для полутоновых изображений

![cartoon semitone gradient](output/results_semitone_gradient/cartoon_semitone_kayyali_gradient.png)

![map semitone gradient](output/results_semitone_gradient/map_semitone_kayyali_gradient.png)

![photo semitone gradient](output/results_semitone_gradient/photo_semitone_kayyali_gradient.png)

![text semitone gradient](output/results_semitone_gradient/text_semitone_kayyali_gradient.png)

![x-ray semitone gradient](output/results_semitone_gradient/x-ray_semitone_kayyali_gradient.png)

#### Вывод

Суммирование модулей (G_x) и (G_y) объединяет информацию о границах по двум направлениям и формирует полную карту контуров.

---

### 5. results_color_binary / results_semitone_binary

#### Откуда брались данные

Использовалась итоговая градиентная матрица (G).

#### Что получилось

Получены бинарные изображения контуров после пороговой обработки при `T = 40`.

Сильные границы отображаются белым цветом, фон — чёрным.

#### Папки с результатами

* [`output/results_color_binary/`](output/results_color_binary/)
* [`output/results_semitone_binary/`](output/results_semitone_binary/)

#### Результаты для цветных изображений

![cartoon binary](output/results_color_binary/cartoon_kayyali_binary_t40.png)

![map binary](output/results_color_binary/map_kayyali_binary_t40.png)

![photo binary](output/results_color_binary/photo_kayyali_binary_t40.png)

![text binary](output/results_color_binary/text_kayyali_binary_t40.png)

![x-ray binary](output/results_color_binary/x-ray_kayyali_binary_t40.png)

#### Результаты для полутоновых изображений

![cartoon semitone binary](output/results_semitone_binary/cartoon_semitone_kayyali_binary_t40.png)

![map semitone binary](output/results_semitone_binary/map_semitone_kayyali_binary_t40.png)

![photo semitone binary](output/results_semitone_binary/photo_semitone_kayyali_binary_t40.png)

![text semitone binary](output/results_semitone_binary/text_semitone_kayyali_binary_t40.png)

![x-ray semitone binary](output/results_semitone_binary/x-ray_semitone_kayyali_binary_t40.png)

#### Вывод

Бинаризация позволяет выделить контуры объектов, однако результат чувствителен к порогу: при низком пороге появляются шумы, при высоком — теряются слабые границы.

---

## Общий вывод по работе

В лабораторной работе реализован градиентный метод выделения контуров с использованием оператора Кайяли 3×3, что соответствует варианту 14.

Последовательность обработки:

```text
gray → Gx → Gy → G → binary
```

корректно выполняет задачу выделения границ объектов на изображении.

Полученные результаты показывают, что:

* оператор Кайяли эффективно выявляет резкие перепады яркости;
* комбинация ( |G_x| + |G_y| ) даёт полную картину контуров;
* качество итогового изображения сильно зависит от выбранного порога бинаризации.

Метод пригоден для задач анализа изображений, где требуется выделение границ объектов.
