# Лабораторная работа №8. Текстурный анализ и контрастирование. Вариант 14

**Вариант:** `14`
**Матрица:** `GLRLM`
**Признаки:** `SRE`, `LRE`
**Метод:** `логарифмическое преобразование яркости`

---

## Теоретическая часть

В работе рассматриваются:

* **контрастирование изображений** (лекция 8а);
* **структурный анализ текстур** (лекция 8б).

### Контрастирование (8а)

Используется **логарифмическое преобразование яркости**, которое нелинейно изменяет распределение яркости относительно среднего значения.

Обработка выполняется через **HSL**, изменяется только канал **L**, что позволяет сохранить цвет изображения.

### Структурный анализ (8б)

Изображение рассматривается как структура повторяющихся элементов.
Используется **GLRLM** — матрица длин серий одинаковой яркости.

Признаки:

* **SRE** — преобладание коротких серий;
* **LRE** — преобладание длинных серий.

---

## Практическая часть

Реализован автоматический конвейер:

* перевод изображения в HSL и выделение яркости;
* логарифмическое преобразование;
* построение гистограмм;
* построение GLRLM;
* вычисление SRE и LRE;
* сравнение результатов до и после.

---

## Что реализуется в файлах

[`run.py`](run.py) — запуск всей лабораторной.

Исходный код находится в папке:

[`src/lab8_variant14/`](src/lab8_variant14/)

Файлы программы:

* [`src/lab8_variant14/config.py`](src/lab8_variant14/config.py) — параметры и пути проекта;
* [`src/lab8_variant14/io_utils.py`](src/lab8_variant14/io_utils.py) — работа с файлами и изображениями;
* [`src/lab8_variant14/hsl.py`](src/lab8_variant14/hsl.py) — перевод RGB ↔ HSL;
* [`src/lab8_variant14/contrast.py`](src/lab8_variant14/contrast.py) — логарифмическое преобразование яркости;
* [`src/lab8_variant14/histogram.py`](src/lab8_variant14/histogram.py) — расчёт гистограмм;
* [`src/lab8_variant14/glrlm.py`](src/lab8_variant14/glrlm.py) — построение GLRLM и признаки SRE/LRE;
* [`src/lab8_variant14/visualization.py`](src/lab8_variant14/visualization.py) — сохранение гистограмм и матриц;
* [`src/lab8_variant14/pipeline.py`](src/lab8_variant14/pipeline.py) — основной конвейер обработки;
* [`src/lab8_variant14/__init__.py`](src/lab8_variant14/__init__.py) — файл инициализации пакета.

---

## Структура входных данных

Исходные изображения брались из папки:

[`input/images/`](input/images/)

Файлы:

* [`book.png`](input/images/book.png)
* [`cartoon.png`](input/images/cartoon.png)
* [`hsl_photo.png`](input/images/hsl_photo.png)
* [`text.png`](input/images/text.png)
* [`wall.png`](input/images/wall.png)

### Исходные изображения

|  № | Изображение | Файл                                          | Просмотр                                  |
| -: | ----------- | --------------------------------------------- | ----------------------------------------- |
|  1 | book        | [`book.png`](input/images/book.png)           | ![book](input/images/book.png)            |
|  2 | cartoon     | [`cartoon.png`](input/images/cartoon.png)     | ![cartoon](input/images/cartoon.png)      |
|  3 | hsl_photo   | [`hsl_photo.png`](input/images/hsl_photo.png) | ![hsl\_photo](input/images/hsl_photo.png) |
|  4 | text        | [`text.png`](input/images/text.png)           | ![text](input/images/text.png)            |
|  5 | wall        | [`wall.png`](input/images/wall.png)           | ![wall](input/images/wall.png)            |

---

## Структура результатов

Все результаты сохраняются в папку:

[`output/`](output/)

Основные подпапки:

* [`output/gray/`](output/gray/) — полутоновые изображения;
* [`output/contrast_gray/`](output/contrast_gray/) — контрастированные изображения в оттенках серого;
* [`output/color_contrast/`](output/color_contrast/) — цветные изображения после контрастирования канала L;
* [`output/hist_before/`](output/hist_before/) — гистограммы до преобразования;
* [`output/hist_after/`](output/hist_after/) — гистограммы после преобразования;
* [`output/matrix_before/`](output/matrix_before/) — GLRLM до преобразования;
* [`output/matrix_after/`](output/matrix_after/) — GLRLM после преобразования;
* [`output/tables/`](output/tables/) — таблицы с численными результатами.

---

## Описание обработки по частям лабораторной

### Часть 1. Расчёт GLRLM и признаков

Строится GLRLM и вычисляются SRE и LRE.

Результаты:

* [`output/matrix_before/`](output/matrix_before/)
* [`output/matrix_after/`](output/matrix_after/)
* [`output/tables/features_comparison.csv`](output/tables/features_comparison.csv)

**Вывод: получены текстурные характеристики изображений.**

---

### Часть 2. Визуализация матриц

Матрицы GLRLM сохраняются в виде изображений с лог-нормализацией.

#### Матрицы GLRLM до преобразования

Папка:

[`output/matrix_before/`](output/matrix_before/)

Файлы:

* [`book_glrlm_before.png`](output/matrix_before/book_glrlm_before.png)
* [`cartoon_glrlm_before.png`](output/matrix_before/cartoon_glrlm_before.png)
* [`hsl_photo_glrlm_before.png`](output/matrix_before/hsl_photo_glrlm_before.png)
* [`text_glrlm_before.png`](output/matrix_before/text_glrlm_before.png)
* [`wall_glrlm_before.png`](output/matrix_before/wall_glrlm_before.png)

| Изображение | GLRLM до преобразования                                                     |
| ----------- | --------------------------------------------------------------------------- |
| book        | ![book GLRLM before](output/matrix_before/book_glrlm_before.png)            |
| cartoon     | ![cartoon GLRLM before](output/matrix_before/cartoon_glrlm_before.png)      |
| hsl_photo   | ![hsl\_photo GLRLM before](output/matrix_before/hsl_photo_glrlm_before.png) |
| text        | ![text GLRLM before](output/matrix_before/text_glrlm_before.png)            |
| wall        | ![wall GLRLM before](output/matrix_before/wall_glrlm_before.png)            |

#### Матрицы GLRLM после преобразования

Папка:

[`output/matrix_after/`](output/matrix_after/)

Файлы:

* [`book_glrlm_after.png`](output/matrix_after/book_glrlm_after.png)
* [`cartoon_glrlm_after.png`](output/matrix_after/cartoon_glrlm_after.png)
* [`hsl_photo_glrlm_after.png`](output/matrix_after/hsl_photo_glrlm_after.png)
* [`text_glrlm_after.png`](output/matrix_after/text_glrlm_after.png)
* [`wall_glrlm_after.png`](output/matrix_after/wall_glrlm_after.png)

| Изображение | GLRLM после преобразования                                               |
| ----------- | ------------------------------------------------------------------------ |
| book        | ![book GLRLM after](output/matrix_after/book_glrlm_after.png)            |
| cartoon     | ![cartoon GLRLM after](output/matrix_after/cartoon_glrlm_after.png)      |
| hsl_photo   | ![hsl\_photo GLRLM after](output/matrix_after/hsl_photo_glrlm_after.png) |
| text        | ![text GLRLM after](output/matrix_after/text_glrlm_after.png)            |
| wall        | ![wall GLRLM after](output/matrix_after/wall_glrlm_after.png)            |

**Вывод: матрицы пригодны для визуального анализа.**

---

### Часть 3. Преобразование яркости

К каналу L применяется логарифмическое преобразование, затем собирается цветное изображение.

Результаты:

* [`output/gray/`](output/gray/)
* [`output/contrast_gray/`](output/contrast_gray/)
* [`output/color_contrast/`](output/color_contrast/)

#### Полутоновые изображения

Папка:

[`output/gray/`](output/gray/)

Файлы:

* [`book_gray.png`](output/gray/book_gray.png)
* [`cartoon_gray.png`](output/gray/cartoon_gray.png)
* [`hsl_photo_gray.png`](output/gray/hsl_photo_gray.png)
* [`text_gray.png`](output/gray/text_gray.png)
* [`wall_gray.png`](output/gray/wall_gray.png)

| Изображение | Gray                                               |
| ----------- | -------------------------------------------------- |
| book        | ![book gray](output/gray/book_gray.png)            |
| cartoon     | ![cartoon gray](output/gray/cartoon_gray.png)      |
| hsl_photo   | ![hsl\_photo gray](output/gray/hsl_photo_gray.png) |
| text        | ![text gray](output/gray/text_gray.png)            |
| wall        | ![wall gray](output/gray/wall_gray.png)            |

#### Контрастированные полутоновые изображения

Папка:

[`output/contrast_gray/`](output/contrast_gray/)

Файлы:

* [`book_contrast_gray.png`](output/contrast_gray/book_contrast_gray.png)
* [`cartoon_contrast_gray.png`](output/contrast_gray/cartoon_contrast_gray.png)
* [`hsl_photo_contrast_gray.png`](output/contrast_gray/hsl_photo_contrast_gray.png)
* [`text_contrast_gray.png`](output/contrast_gray/text_contrast_gray.png)
* [`wall_contrast_gray.png`](output/contrast_gray/wall_contrast_gray.png)

| Изображение | Contrast gray                                                                 |
| ----------- | ----------------------------------------------------------------------------- |
| book        | ![book contrast gray](output/contrast_gray/book_contrast_gray.png)            |
| cartoon     | ![cartoon contrast gray](output/contrast_gray/cartoon_contrast_gray.png)      |
| hsl_photo   | ![hsl\_photo contrast gray](output/contrast_gray/hsl_photo_contrast_gray.png) |
| text        | ![text contrast gray](output/contrast_gray/text_contrast_gray.png)            |
| wall        | ![wall contrast gray](output/contrast_gray/wall_contrast_gray.png)            |

#### Цветные изображения после контрастирования

Папка:

[`output/color_contrast/`](output/color_contrast/)

Файлы:

* [`book_color_contrast.png`](output/color_contrast/book_color_contrast.png)
* [`cartoon_color_contrast.png`](output/color_contrast/cartoon_color_contrast.png)
* [`hsl_photo_color_contrast.png`](output/color_contrast/hsl_photo_color_contrast.png)
* [`text_color_contrast.png`](output/color_contrast/text_color_contrast.png)
* [`wall_color_contrast.png`](output/color_contrast/wall_color_contrast.png)

| Изображение | Color contrast                                                                   |
| ----------- | -------------------------------------------------------------------------------- |
| book        | ![book color contrast](output/color_contrast/book_color_contrast.png)            |
| cartoon     | ![cartoon color contrast](output/color_contrast/cartoon_color_contrast.png)      |
| hsl_photo   | ![hsl\_photo color contrast](output/color_contrast/hsl_photo_color_contrast.png) |
| text        | ![text color contrast](output/color_contrast/text_color_contrast.png)            |
| wall        | ![wall color contrast](output/color_contrast/wall_color_contrast.png)            |

**Вывод: выполнено контрастирование без изменения цветовых каналов.**

---

### Часть 4. Гистограммы

Строятся гистограммы яркости до и после преобразования.

Результаты:

* [`output/hist_before/`](output/hist_before/)
* [`output/hist_after/`](output/hist_after/)

#### Гистограммы до преобразования

Папка:

[`output/hist_before/`](output/hist_before/)

Файлы:

* [`book_hist_before.png`](output/hist_before/book_hist_before.png)
* [`cartoon_hist_before.png`](output/hist_before/cartoon_hist_before.png)
* [`hsl_photo_hist_before.png`](output/hist_before/hsl_photo_hist_before.png)
* [`text_hist_before.png`](output/hist_before/text_hist_before.png)
* [`wall_hist_before.png`](output/hist_before/wall_hist_before.png)

| Изображение | Гистограмма до                                                          |
| ----------- | ----------------------------------------------------------------------- |
| book        | ![book hist before](output/hist_before/book_hist_before.png)            |
| cartoon     | ![cartoon hist before](output/hist_before/cartoon_hist_before.png)      |
| hsl_photo   | ![hsl\_photo hist before](output/hist_before/hsl_photo_hist_before.png) |
| text        | ![text hist before](output/hist_before/text_hist_before.png)            |
| wall        | ![wall hist before](output/hist_before/wall_hist_before.png)            |

#### Гистограммы после преобразования

Папка:

[`output/hist_after/`](output/hist_after/)

Файлы:

* [`book_hist_after.png`](output/hist_after/book_hist_after.png)
* [`cartoon_hist_after.png`](output/hist_after/cartoon_hist_after.png)
* [`hsl_photo_hist_after.png`](output/hist_after/hsl_photo_hist_after.png)
* [`text_hist_after.png`](output/hist_after/text_hist_after.png)
* [`wall_hist_after.png`](output/hist_after/wall_hist_after.png)

| Изображение | Гистограмма после                                                    |
| ----------- | -------------------------------------------------------------------- |
| book        | ![book hist after](output/hist_after/book_hist_after.png)            |
| cartoon     | ![cartoon hist after](output/hist_after/cartoon_hist_after.png)      |
| hsl_photo   | ![hsl\_photo hist after](output/hist_after/hsl_photo_hist_after.png) |
| text        | ![text hist after](output/hist_after/text_hist_after.png)            |
| wall        | ![wall hist after](output/hist_after/wall_hist_after.png)            |

**Вывод: показано изменение распределения яркости.**

---

### Часть 5. Сравнение признаков

Сравниваются SRE и LRE до и после обработки.

Результат сохраняется в файл:

[`output/tables/features_comparison.csv`](output/tables/features_comparison.csv)

Папка с таблицами:

[`output/tables/`](output/tables/)

**Вывод: изменения текстуры оценены количественно.**

---

### Часть 6. Демонстрация результатов

Сохраняются:

* исходные и полутоновые изображения;
* контрастированные изображения;
* гистограммы;
* матрицы GLRLM;
* таблица сравнения признаков.

---

## Сводная таблица результатов по файлам

| Исходное изображение                          | Gray                                                   | Contrast gray                                                                     | Color contrast                                                                       | Hist before                                                                 | Hist after                                                               | GLRLM before                                                                    | GLRLM after                                                                  |
| --------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`book.png`](input/images/book.png)           | [`book_gray.png`](output/gray/book_gray.png)           | [`book_contrast_gray.png`](output/contrast_gray/book_contrast_gray.png)           | [`book_color_contrast.png`](output/color_contrast/book_color_contrast.png)           | [`book_hist_before.png`](output/hist_before/book_hist_before.png)           | [`book_hist_after.png`](output/hist_after/book_hist_after.png)           | [`book_glrlm_before.png`](output/matrix_before/book_glrlm_before.png)           | [`book_glrlm_after.png`](output/matrix_after/book_glrlm_after.png)           |
| [`cartoon.png`](input/images/cartoon.png)     | [`cartoon_gray.png`](output/gray/cartoon_gray.png)     | [`cartoon_contrast_gray.png`](output/contrast_gray/cartoon_contrast_gray.png)     | [`cartoon_color_contrast.png`](output/color_contrast/cartoon_color_contrast.png)     | [`cartoon_hist_before.png`](output/hist_before/cartoon_hist_before.png)     | [`cartoon_hist_after.png`](output/hist_after/cartoon_hist_after.png)     | [`cartoon_glrlm_before.png`](output/matrix_before/cartoon_glrlm_before.png)     | [`cartoon_glrlm_after.png`](output/matrix_after/cartoon_glrlm_after.png)     |
| [`hsl_photo.png`](input/images/hsl_photo.png) | [`hsl_photo_gray.png`](output/gray/hsl_photo_gray.png) | [`hsl_photo_contrast_gray.png`](output/contrast_gray/hsl_photo_contrast_gray.png) | [`hsl_photo_color_contrast.png`](output/color_contrast/hsl_photo_color_contrast.png) | [`hsl_photo_hist_before.png`](output/hist_before/hsl_photo_hist_before.png) | [`hsl_photo_hist_after.png`](output/hist_after/hsl_photo_hist_after.png) | [`hsl_photo_glrlm_before.png`](output/matrix_before/hsl_photo_glrlm_before.png) | [`hsl_photo_glrlm_after.png`](output/matrix_after/hsl_photo_glrlm_after.png) |
| [`text.png`](input/images/text.png)           | [`text_gray.png`](output/gray/text_gray.png)           | [`text_contrast_gray.png`](output/contrast_gray/text_contrast_gray.png)           | [`text_color_contrast.png`](output/color_contrast/text_color_contrast.png)           | [`text_hist_before.png`](output/hist_before/text_hist_before.png)           | [`text_hist_after.png`](output/hist_after/text_hist_after.png)           | [`text_glrlm_before.png`](output/matrix_before/text_glrlm_before.png)           | [`text_glrlm_after.png`](output/matrix_after/text_glrlm_after.png)           |
| [`wall.png`](input/images/wall.png)           | [`wall_gray.png`](output/gray/wall_gray.png)           | [`wall_contrast_gray.png`](output/contrast_gray/wall_contrast_gray.png)           | [`wall_color_contrast.png`](output/color_contrast/wall_color_contrast.png)           | [`wall_hist_before.png`](output/hist_before/wall_hist_before.png)           | [`wall_hist_after.png`](output/hist_after/wall_hist_after.png)           | [`wall_glrlm_before.png`](output/matrix_before/wall_glrlm_before.png)           | [`wall_glrlm_after.png`](output/matrix_after/wall_glrlm_after.png)           |

---

## Общий вывод

В работе был реализован текстурный анализ изображений на основе **GLRLM** и выполнено **логарифмическое контрастирование** яркости для варианта 14.

Для каждого изображения выделялся канал яркости **L** из модели **HSL**, строились гистограммы до и после преобразования, вычислялись матрицы длин серий и признаки **SRE** и **LRE**.

В результате удалось получить как визуальное сравнение исходных и обработанных изображений, так и численную оценку изменения текстурных характеристик.

Таким образом, в лабораторной были использованы идеи из лекции 8а по контрастированию и из лекции 8б по структурному анализу изображения.
