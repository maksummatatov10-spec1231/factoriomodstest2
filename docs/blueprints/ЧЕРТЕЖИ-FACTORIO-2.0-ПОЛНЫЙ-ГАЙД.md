# Чертежи (Blueprints) Factorio 2.0 — абсолютно всё + генерация кодом

> Обновлено: 28.08.2026 · Целевая версия игры: **2.0.76 / 2.0.77** (и общая ветка 2.0.x)
> Источники: [wiki: Blueprint string format](https://wiki.factorio.com/Blueprint_string_format),
> [wiki: Blueprint](https://wiki.factorio.com/Blueprint),
> [Lua API 2.0.76](https://lua-api.factorio.com/2.0.76/),
> [redruin1/factorio-blueprint-schemas](https://github.com/redruin1/factorio-blueprint-schemas) (машиночитаемые JSON-схемы 2.0),
> Steam-обсуждение «Importing customized blueprints just got much easier», форумы Factorio.
> Всё проверено на реальных строках чертежей 2.0 (эталоны лежат в `tests/data/bp/`).

---

## 0. TL;DR (как я буду писать тебе чертежи)

1. **Чертеж = JSON-объект**, упакованный в строку: `'0' + base64(zlib(JSON))`
   (первый символ `0` — версия контейнера; zlib deflate уровень 9).
2. **Начиная с 2.0** игра принимает **и просто JSON** (minified или pretty) —
   вставляется в то же окно «Импорт строки», и **JSON-файл можно перетащить**
   прямо на окно игры (drag&drop, при windowed-режиме). Это самый удобный
   способ получить от меня чертеж: я даю тебе **либо строку `0eN...`, либо
   файл `.json`**.
3. **Изменения 2.0, критичные для генерации:** направления `0..15` (было 0..7),
   **качество** у сущностей/фильтров/сигналов, `recipe_quality` у сборщиков,
   глобальный список проводов `wires` (вместо per-entity `connections`),
   расписания поездов с прерываниями, `stock_connections` вагонов,
   параметризация (`parameters`, id/number), `mirror`, `mirror` жидкости.
4. Инструмент уже в репозитории: `scripts/blueprints/blueprint_lib.py`
   (encode/decode + конструкторы) и `scripts/blueprints/examples.py`
   (примеры: см. `blueprints/examples/*.json` и `*.txt`).

---

## 1. Как устроена строка чертежа

```
"0" + base64( zlib_compress_level_9( utf8( JSON ) ) )
```

| Шаг | Что |
|---|---|
| 1 | Чертеж сериализуется в **JSON** (минимальный, без пробелов) |
| 2 | JSON сжимается **zlib deflate, уровень 9** |
| 3 | Бинарь кодируется **base64** (стандартный алфавит) |
| 4 | Спереди добавляется **версия контейнера `'0'`** (все версии игры до 2.0 включительно) |

Декодирование (bash):
```bash
echo "$BP" | cut -c2- | base64 -d | pigz -d            # или zlib-flate -uncompress
echo "$BP" | cut -c2- | base64 -d | pigz -d | jq .     # pretty JSON
```

> **В 2.0** добавляется: игра принимает **сырой JSON** в поле «Импорт строки»
> и **файл .json перетаскиванием**. Проверено сообществом — работает и minified,
> и pretty. Следовательно, для обмена со мной JSON-файл даже удобнее строки:
> его можно редактировать вручную и импортировать сколько угодно раз.

---

## 2. Верхнеуровневая структура JSON

Каждый «blueprintable» — это **объект-обёртка** с ключом `blueprint`,
`blueprint_book`, `deconstruction_planner` или `upgrade_planner`.

### 2.1 Blueprint

```json
{
  "blueprint": {
    "item": "blueprint",
    "label": "Моя плавка",
    "label_color": {"r":0.2,"g":0.8,"b":0.3,"a":1},
    "description": "Описание (rich text поддерживается)",
    "icons": [
      {"index": 1, "signal": {"name": "stone-furnace"}},
      {"index": 2, "signal": {"name": "iron-plate", "quality": "uncommon"}}
    ],
    "entities": [ ... ],
    "tiles": [ {"name":"concrete","position":{"x":0,"y":0}}, ... ],
    "wires": [ [1, 1, 2, 1], [3, 2, 4, 2], [5, 5, 6, 5] ],
    "stock_connections": [ {"stock": 102}, ... ],
    "schedules": [ {"locomotives":[102], "schedule": {"records":[...], "interrupts":[...]}}, ... ],
    "parameters": [ {"type":"id","name":"Топливо","id":"parameter-0"}, ... ],
    "snap-to-grid": {"x":1,"y":1},
    "absolute-snapping": false,
    "position-relative-to-grid": {"x":0,"y":0},
    "version": 562949956501504
  }
}
```

| Поле | Тип | Что |
|---|---|---|
| `item` | string | **обязательно** `"blueprint"` |
| `label` | string | название (можно rich text: `[item=iron-plate]`) |
| `label_color` | Color | цвет подписи |
| `description` | string | описание (rich text поддерживается) |
| `icons` | до 4 × Icon | иконки чертежа |
| `entities` | array | сущности (см. §4) |
| `tiles` | array | тайлы `{name, position}` |
| `wires` | array | **провода в 2.0** (см. §5) |
| `stock_connections` | array | соединения подвижного состава |
| `schedules` | array | расписания поездов/платформ (см. §7) |
| `parameters` | array | параметризация (см. §8) |
| `snap-to-grid`, `absolute-snapping`, `position-relative-to-grid` | | привязка к сетке |
| `version` | uint64 | версия карты/игры (см. §11) |

### 2.2 Blueprint book

```json
{
  "blueprint_book": {
    "item": "blueprint-book",
    "label": "Книга",
    "blueprints": [
      {"index": 0, "blueprint": { ... }},
      {"index": 1, "blueprint": { ... }}
    ],
    "active_index": 0,
    "icons": [ ... ],
    "version": 562949956501504
  }
}
```

Внутри книги каждый элемент — `{"index": 0-based, "blueprint": {...}}`.

### 2.3 Deconstruction planner

```json
{
  "deconstruction_planner": {
    "item": "deconstruction-planner",
    "label": "Снести всё",
    "entity_filters": [{"name":"stone-furnace","index":1}],
    "tile_filters": [{"name":"concrete","index":1}],
    "entity_filter_mode": 0,
    "tile_filter_mode": 0,
    "tiles_only": false,
    "version": 562949956501504
  }
}
```
- `entity_filter_mode` / `tile_filter_mode`: `0` = whitelist, `1` = blacklist.
- `tiles_only`: true = деструктор работает только по тайлам (режим «Tiles only»).

### 2.4 Upgrade planner

```json
{
  "upgrade_planner": {
    "item": "upgrade-planner",
    "label": "Апгрейд",
    "settings": {
      "mapper": [
        {
          "index": 1,
          "from": {"name":"stone-furnace","type":"entity","quality":"normal"},
          "to":   {"name":"steel-furnace","type":"entity","quality":"normal"}
        }
      ]
    },
    "version": 562949956501504
  }
}
```
- `type` — `"entity"` или `"item"`; `quality` у `from`/`to` (2.0!)
- mapper также поддерживает установку **модулей** (пустой `from` = установить модуль, `to` = модуль + count) и **топлива** — как в GUI апгрейд-планера.

---

## 3. Иконки и сигналы

```json
{ "index": 1, "signal": { "name": "iron-plate" } }
{ "index": 2, "signal": { "name": "speed-module-3", "quality": "legendary" } }
{ "index": 3, "signal": { "type": "item", "name": "signal-red" } }
```

**SignalID (2.0):**
- `name` — имя прототипа (предмет, сигнал, сущность, жидкость…);
- `type` — категория сигнала; **в 2.0 опционально**, по умолчанию `"item"`.
  Возможные: `item`, `fluid`, `virtual`, `game`, `recipe`, `item-quality`...
- `quality` — качество сигнала/предмета (2.0!).
- Иконок в чертеже — **максимум 4**.

---

## 4. Сущности (entity) — полный формат 2.0

### 4.1 Обязательные поля

```json
{
  "entity_number": 1,
  "name": "stone-furnace",
  "position": {"x": 0, "y": 0}
}
```
- `entity_number` — **уникальный 1-based** индекс в чертеже;
- `name` — имя прототипа (несуществующее имя при импорте → сущность
  пропускается с уведомлением в консоли);
- `position` — центр сущности в тайлах (допустимы `.5`, `1.5`, также `1/256`-дроби у рельсов).

### 4.2 Общие опциональные поля (2.0)

| Поле | Тип | Описание |
|---|---|---|
| `direction` | uint **0–15** | направление. **В 2.0 значения удвоены** (1.1: 0–7). 0 = север, далее по часовой |
| `mirror` | bool | зеркалирование жидкостных портов (2.0) |
| `quality` | string | качество сущности (`normal`/`uncommon`/`rare`/`epic`/`legendary`) |
| `items` | array | **запросы при строительстве** (модули, топливо, предметы) — см. 4.3 |
| `tags` | object | произвольные теги (для читаемости/скриптов) |

Соединения **в 2.0 на уровне сущности не пишутся** — они в глобальном
`wires` (§5). (Схемы 2.0: entity.json содержит только direction/mirror/quality/items/tags.)

### 4.3 `items` — запросы предметов при строительстве (2.0!)

```json
"items": [
  {
    "id": {"name": "speed-module-3", "quality": "legendary"},
    "items": {
      "in_inventory": [{"inventory": 1, "stack": 0}, {"inventory": 1, "stack": 1}]
    }
  }
]
```
- `id.name` + опционально `id.quality` — что заказать;
- `items.in_inventory` — куда положить (inventory index машины и слот стека).
Пример: печка с углём → `{"id":{"name":"coal"},"items":{"in_inventory":[{"inventory":1,"stack":0}]}}`.
Это определяет **item-request-proxy**: в чертеже печка сама запросит у
строительных роботов уголь/модули.

### 4.4 Поля по типам сущностей (выборочно из схем 2.0)

| Сущность | Поля |
|---|---|
| `assembling-machine` | `recipe`, `recipe_quality` (2.0) |
| `constant-combinator` | `control_behavior.sections.sections` (2.0 sections!) |
| `decider-combinator`, `selector-combinator`, `arithmetic-combinator` | `control_behavior` (decider_conditions, selector_conditions...) |
| `train-stop` | `station`, `manual_trains_limit`, `priority` (2.0), `color` |
| `locomotive` / `cargo-wagon` / `fluid-wagon` / `artillery-wagon` | `color`, `orientation` (0..1), `enable_logistics_while_moving`; вагон — `inventory` |
| `inserter` | `override_stack_size`, `pickup_position`, `drop_position`, `spoil_priority` (2.0), `control_behavior` |
| `rail-signal` / `rail-chain-signal` | `control_behavior` (read/close/выходные сигналы) |
| `straight-rail` / `curved-rail-a/b` / `elevated-*` | нет особых полей; направление через `direction` |
| `rocket-silo` | `control_behavior` (read_items_mode...), `transitional_request_index`, `use_transitional_requests` |
| `power-switch` | `switch_state` |
| `container`/`logistic-*` | `bar`, `request_filters`, `request_from_buffers` |
| `splitter` | `input_priority`, `output_priority`, `filter` (см. фильтр с качеством), `control_behavior` |
| `loader` | `type` (`input`/`output`), `filters`, `control_behavior` |
| `programmable-speaker` | `parameters` (volume/global/polyphony), `alert_parameters` |
| `asteroid-collector` | `chunk-filter`, `result_inventory`, `control_behavior` |
| `space-platform-hub` | `control_behavior`, `request_missing_construction_materials` |
| `cargo-landing-pad` | `control_behavior` |

**Фильтр с качеством (2.0!) — сплиттер/инсертер:**
```json
"filter": {"name": "iron-plate", "quality": "uncommon", "comparator": "="}
```
`comparator` — `=`, `!=`, `>`, `>=`, `<`, `<=`.

**request_filters логистических сундуков:**
```json
"request_filters": [
  {"index": 1, "name": "iron-plate", "quality": "normal", "comparator": "=", "count": 100},
  {"index": 2, "name": "copper-plate", "quality": "any", "comparator": "=", "count": 100}
]
```

**2.0 постоянный комбинатор (sections):**
```json
"control_behavior": {
  "sections": {
    "sections": [
      {"index": 1, "filters": [{"index": 1, "name": "iron-plate", "quality": "normal",
                                "comparator": "=", "count": 10}], "group": "Iron"},
      {"index": 2, "filters": [{"index": 1, "name": "copper-plate", "count": 5}]}
    ]
  }
}
```

---

## 5. Провода (`wires`) — новое в 2.0

Вместо `connections`/`neighbours` внутри сущности — **единый массив**:

```json
"wires": [
  [1, 1, 2, 1],   // сущность 1 — красный провод — сущность 2
  [1, 2, 2, 2],   // сущность 1 — зелёный провод — сущность 2
  [3, 5, 4, 5]    // сущность 3 — медный провод — сущность 4
]
```

Формат: `[from_entity_number, from_wire_connector_id, to_entity_number, to_wire_connector_id]`

**wire_connector_id (2.0, `defines.wire_connector_id`):**

| id | Значение |
|---|---|
| 1 | circuit red (и красный вход комбинатора) |
| 2 | circuit green (и зелёный вход комбинатора) |
| 3 | circuit red output комбинатора |
| 4 | circuit green output комбинатора |
| 5 | copper (провод питания / левый полюс power switch) |
| 6 | правый полюс power switch |

Проверено на эталоне: `[[2,1,3,1]]` соединяет два аккумулятора красным проводом.

---

## 6. Тайлы

```json
"tiles": [ {"name": "concrete", "position": {"x": 0, "y": 0}} ]
```

---

## 7. Расписания (train / platform) — новый формат 2.0

```json
"schedules": [
  {
    "locomotives": [102],
    "schedule": {
      "records": [
        {
          "station": "Рудник",
          "wait_conditions": [
            {"type": "full", "compare_type": "and"},
            {"type": "time", "compare_type": "or", "ticks": 6000}
          ]
        }
      ],
      "interrupts": [
        {
          "name": "Дозаправка",
          "conditions": [{"type": "fuel_item_count_any", "compare_type": "and",
                          "condition": {"first_signal": {"name":"coal"},
                                        "comparator": "<", "constant": 10}}],
          "targets": [{"station": "Заправка",
                       "wait_conditions": [{"type": "full", "compare_type": "and"}]}],
          "inside_interrupt": true
        }
      ]
    }
  }
]
```

- `locomotives` — entity_number локомотивов, к которым относится расписание;
- `schedule.records` — остановки: `station` + `wait_conditions`;
- `schedule.interrupts` — **прерывания (2.0!)**: `name`, `conditions`, `targets`,
  `inside_interrupt`;
- типы условий: `time`, `inactivity`, `full`, `empty`, `not_empty`, `item_count`,
  `circuit`, `robots_inactive`, `fluid_count`, `fuel_item_count_all/any`,
  `fuel_full`, `passenger_present`, `at_station`, `destination_full_or_no_path`,
  `not_at_station`;
- `compare_type`: `and` / `or`;
- условия с сигналами: `condition` = CircuitCondition.

**Space platform schedules** — аналогично (`space-platform-schedule`,
`space-platform-schedule-stop`, `space-platform-wait-condition`,
`space-platform-interrupt-condition`).

---

## 8. Параметризация чертежей (2.0)

Даёт возможность при **установке чертежа** выбирать сигнал/предмет/число.
В JSON:

```json
"parameters": [
  {"type": "id", "name": "Топливо", "id": "parameter-0"},
  {"type": "number", "name": "Количество", "id": "parameter-1",
   "minimum": 0, "maximum": 1000, "default": 50}
]
```

Плейсхолдеры в полях сущностей:
- "recipe": "parameter-0" / "recipe_quality": "normal"
- "name": "parameter-0" в комбинаторах-фильтрах
- сигналы: `{"name": "parameter-0"}`

При программной установке (моды):
```lua
player.cursor_record.build_blueprint(
  parameters = { ["parameter-0"] = "beacon", ["parameter-1"] = "50" },
  ...
)
```

---

## 9. Соединения подвижного состава

```json
"stock_connections": [ {"stock": 102} ]
```
`stock` = entity_number вагона/локомотива, связь которого с соседом
сохранена явно (нужно для поездов в чертеже; при обычной сборке соединения
вагонов определяются автоматически по позиции).

---

## 10. Как импортировать в игру (3 способа — все работают в 2.0)

1. **Строка:** открыть игру → панель снизу → иконка **«Импорт строки»**
   (Import string) → вставить `0eN...` → Импорт.
2. **JSON прямо в поле (2.0!):** тот же «Импорт строки» → вставить JSON
   (minified или pretty) → Импорт.
3. **Drag&drop (2.0!):** сохранить JSON в файл `.json` → перетащить файл
   на окно игры (окно не в полном экране для надёжности).

Совет: для длинных чертежей, которые буду генерировать, удобнее дать тебе
**файл JSON** (красивый, читаемый) — импортируется напрямую, и его можно
подправить руками. Строку `0eN...` даю как запасной вариант.

---

## 11. Значение `version`

`version` — uint64, кодирующий версию игры/карты. Для 2.0 в реальных
чертежах встречается `562949956501504` (0x000200000002F000) — оно
воспроизводится в эталонах и работает при импорте. Библиотека ставит его
по умолчанию; менять не нужно, пока не потребуется строгая совместимость
с конкретным патчем.

---

## 12. Официальный Lua API (2.0.76) — работа с чертежами в игре/модах

### LuaItemStack / LuaItemCommon (главное)

| Метод | Что делает |
|---|---|
| `stack.export_stack()` | строка чертежа из предмета (blueprint, book, planner, item-with-tags) |
| `stack.import_stack(data)` | импорт строки (или JSON в 2.0) в предмет; **возвращает int32** |
| `item.clear_blueprint()` | очистить чертеж |
| `item.is_blueprint_setup()` | настроен ли чертеж |
| `item.create_blueprint{surface, force, area, always_include_tiles?, include_entities?, include_modules?, include_station_names?, include_trains?, include_fuel?}` | создать из выделенной области |
| `item.build_blueprint{surface=..., force=..., position=..., direction?, build_mode?, skip_fog_of_war?, by_player?, raise_built?}` | построить чертеж (возвращает массив призраков/сущностей) |
| `item.get_blueprint_entities()` / `set_blueprint_entities(entities)` | список/замена сущностей чертежа |
| `item.get_blueprint_tiles()` / `set_blueprint_tiles(tiles)` | тайлы |
| `item.get_blueprint_entity_count()` | число сущностей |
| `item.get/set_blueprint_entity_tag(s)` | теги |
| `item.get/set_entity_filter`, `get/set_tile_filter` | фильтры деструктора |
| `item.deconstruct_area{}`, `cancel_deconstruct_area{}` | применить деструктор |

### Прочее

- **Библиотека чертежей (2.0):** `player.blueprints` и `game.blueprints`
  (LuaBlueprintLibrary + `LuaRecord` для книг/записей), методы add/remove
  записей. `LuaRecord::is_preview`, `blueprint_description` и т.д.
- **Параметризация при построении:** `cursor_record.build_blueprint(parameters = {...})`.
- **Импорт «на лету» для мода** (классика без фич библиотеки):
  ```lua
  local bp_entity = surface.create_entity{name='item-on-ground', position=pos, stack='blueprint'}
  bp_entity.stack.import_stack(bp_string)
  bp_entity.stack.build_blueprint{surface=surface, force=force, position=pos,
                                  force_build=true, skip_fog_of_war=true}
  bp_entity.destroy()
  ```
- **Консоль для игрока:** `/c game.player.insert{name='blueprint', count=1}` +
  импорт через API выше, либо просто инструкция из §10.

---

## 13. Инструменты сообщества

| Инструмент | Что |
|---|---|
| **redruin1/factorio-blueprint-schemas** | официально-подобные JSON-схемы всех версий (в т.ч. 2.0, 83 типа сущностей) + валидация через `jsonschema`; HTML-документация: `https://redruin1.github.io/factorio-blueprint-schemas/html/2.0.0/blueprintable.html` |
| **factorio-blueprint (Rust)** | crate с кодеком (decode/encode, base64+zlib, префикс 0) |
| **factorio.blue** | популярный онлайн редактор/хостинг чертежей (поддерживает 2.0) |
| **Blueprint string decoder** | любой однострочник: `cut -c2- | base64 -d | zlib-flate -uncompress` |
| **Steam-дискуссия (Drag&drop JSON)** | подтверждение: в 2.0 игра принимает JSON файлы/строки напрямую |

---

## 14. Наш рабочий процесс (генерация твоих чертежей)

1. **Ты говоришь, что нужно** (например: «маленькая плавка меди 60/с», «секция
   зелёной науки», «депо с двумя поездами и прерыванием»).
2. Я описываю сущности **кодом**: `entity()`, `wire()`, `train_stop_entity()`,
   `combinator_sections()`, `request_filters()`... → собираю `blueprint(...)`
   → `encode()`.
3. Кладу результат в `blueprints/<название>/`:
   - `<название>.json` — pretty JSON (импортируй перетаскиванием или вставкой);
   - `<название>.txt` — строка `0eN...` (вставь в «Импорт строки»);
   - `<название>.md` — краткая схема/инструкция что где стоит.
4. Валидация: `tests/test_blueprints.py` (структура, entity_number, wires,
   round-trip) + при возможности проверка на реальном эталоне 2.0.

### Уже готовые демо (сгенерированы и проверены кодом)

- `blueprints/examples/smelter-demo.json/.txt` — печка + инсертер + лента;
- `blueprints/examples/logic-demo.json/.txt` — постоянники (2.0 sections) +
  decider + красный/зелёный провода;
- `blueprints/examples/demo-book.json/.txt` — книга из двух чертежей.

### Как пользоваться кодеком

```bash
python3 scripts/blueprints/blueprint_lib.py decode "0eN..."       # строка -> JSON
python3 scripts/blueprints/blueprint_lib.py encode file.json      # JSON -> строка
python3 scripts/blueprints/blueprint_lib.py encode file.json --pretty  # JSON as-is для импорта
python3 scripts/blueprints/examples.py                            # перегенерировать демо
python3 tests/test_blueprints.py                                  # тесты
```

---

## 15. Чек-лист валидного JSON чертежа 2.0

- [ ] обёртка `{"blueprint": {...}}` (или book/planner);
- [ ] `item` = `blueprint` / `blueprint-book` / ...;
- [ ] `entity_number` уникальны, 1-based;
- [ ] у каждой сущности: `name`, `position`;
- [ ] `direction` (если есть) — **0..15**;
- [ ] `quality` (если есть) — одно из: normal/uncommon/rare/epic/legendary;
- [ ] `wires` ссылаются только на существующие entity_number, формат `[a,conn,b,conn]`;
- [ ] `icons` ≤ 4; `version` задан;
- [ ] `schedules.locomotives` — существующие entity_number;
- [ ] у `request_filters`/`filters` поля: `index` (1-based), `name`, `quality?`, `count?`;
- [ ] `tags` — только строки/числа/bool/объекты.

---

*Полная база: `docs/blueprints/ЧЕРТЕЖИ-FACTORIO-2.0-ПОЛНЫЙ-ГАЙД.md`,
кодек и примеры в `scripts/blueprints/`, эталоны в `tests/data/bp/`.
Эти схемы (redruin1) — самый точный машиночитаемый источник формата 2.0;
вики-страница помечена «needs update for 2.0», поэтому сверяюсь с ней
осторожно и отдаю приоритет схемам + реальным строкам.*
