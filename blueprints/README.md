# 📐 Генерация чертежей Factorio 2.0 кодом

Здесь лежат чертежи, сгенерированные скриптами этого репозитория.
Каждый чертеж — папка с:
- `<имя>.json` — читаемый JSON (можно импортировать в игру **напрямую**
  через «Импорт строки» — вставь содержимое файла, **или перетащи файл**
  на окно игры; обе возможности добавлены в 2.0);
- `<имя>.txt` — классическая строка `0eN...` (вставь в «Импорт строки»);
- `<имя>.md` — краткое описание схемы.

## Быстрый старт

```bash
# перегенерировать демо-чертежи
python3 scripts/blueprints/examples.py

# декодировать строку в JSON
python3 scripts/blueprints/blueprint_lib.py decode "0eN..."

# закодировать JSON в строку
python3 scripts/blueprints/blueprint_lib.py encode blueprint/examples/smelter-demo.json

# тесты кодера (round-trip на реальных строках 2.0 + демо)
python3 tests/test_blueprints.py
```

## Уже сгенерировано

| Чертеж | Содержимое |
|---|---|
| `examples/smelter-demo` | печка + инсертер + лента (демо направлений 2.0) |
| `examples/logic-demo` | постоянные комбинаторы (2.0 sections) + decider + провода |
| `examples/demo-book` | книга из двух чертежей |

## Правила формата 2.0 (кратко)

- строка = `'0' + base64(zlib(JSON))`; в 2.0 игра принимает и **чистый JSON**;
- `direction` — **0..15** (1.1 был 0..7);
- `quality` — у сущностей/фильтров/сигналов; `recipe_quality` у сборщиков;
- провода — глобальный `wires: [[from,conn,to,conn],...]` (1=красный, 2=зелёный,
  3/4=выходы комбинатора, 5=медь, 6=правый полюс);
- расписания — `schedules[{locomotives, schedule:{records, interrupts}}]`;
- параметризация — `parameters[{type:'id'|'number',...}]`.

Подробно: `../docs/blueprints/ЧЕРТЕЖИ-FACTORIO-2.0-ПОЛНЫЙ-ГАЙД.md`
