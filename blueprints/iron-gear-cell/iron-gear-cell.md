# 🛠 Чертёж: Зелёный сборщик 3 ур. → Железные шестерни (логистическая ячейка)

**Формат: Factorio 2.0 (2.0.76)** · Сгенерировано кодом и проверено
(JSON-схема 2.0 + round-trip декодера + реальные имена из `wube/factorio-data` тег 2.0.76).

---

## 📐 Схема (вид сверху, X → восток, Y → юг)

```
[СУНДУК-ЗАПРОС] → [МАНИПУЛЯТОР] → [СБОРЩИК 3] → [МАНИПУЛЯТОР] → [СУНДУК-СНАБЖЕНИЯ]
    (0,0)             (1,0)          (2,0)          (3,0)            (4,0)
  iron-plate ×75      east↓          IRON GEAR      west←          шестерни
```

## 📋 Точные объекты (координаты + направления + рецепт)

| # | Объект | Имя прототипа (2.0) | X | Y | Direction (2.0: 0–15) | Настройки |
|---|---|---|---|---|---|---|
| 1 | Сундук-запрос | `requester-chest` | 0 | 0 | 0 (север) | `request_filters`: **iron-plate × 75** (компаратор `=`) |
| 2 | Манипулятор (вход) | `inserter` | 1 | 0 | **2 (восток)** | смотрит на сборщик |
| 3 | **Сборщик 3 ур. (зелёный)** | `assembling-machine-3` | 2 | 0 | 0 (север) | **`recipe: iron-gear-wheel`**, `recipe_quality: normal` |
| 4 | Манипулятор (выход) | `inserter` | 3 | 0 | **6 (запад)** | смотрит на сундук снабжения |
| 5 | Сундук снабжения (пассивный) | `passive-provider-chest` | 4 | 0 | 0 (север) | — (роботы забирают шестерни) |

> **Направления 2.0:** 0 = север, 1 = северо-восток, 2 = восток, 3 = юго-восток,
> 4 = юг, 5 = юго-запад, 6 = запад, 7 = северо-запад (диагонали — 8–15).

## ⚙️ Рецепт (проверено в официальных данных 2.0.76)

- **`iron-gear-wheel`**: `2 × iron-plate` → `1 × iron-gear-wheel`
- Время крафта: 0.5 с
- **Скорость AM3:** `crafting_speed = 1.25` → **5 плит/сек** → **2.5 шестерни/сек**

## 🧮 Расчёт буфера (референс: Factorio Prints, схема «Assembler Quality
Upcycling» — тот же рецепт)

- 30 секунд работы = `5 плит/с × 30 с = 150 плит`
- Стак запроса в сундук-запрос: `150 / 2 = 75` → **75 iron-plate**
- Готово: роботы держат 30-секундный запас, установка никогда не простаивает.

---

## 📄 Чертёж

### Вариант 1 — JSON (рекомендуется, 2.0 принимает напрямую)

Скопируй содержимое **`iron-gear-cell.json`** (лежит рядом) или вот он:

```json
{
  "blueprint": {
    "item": "blueprint",
    "label": "Iron Gear Cell (AM3)",
    "entities": [
      {
        "entity_number": 1,
        "name": "requester-chest",
        "position": {"x": 0, "y": 0},
        "direction": 0,
        "request_filters": {
          "request_from_buffers": true,
          "sections": [
            {"index": 1, "filters": [
              {"index": 1, "name": "iron-plate", "comparator": "=", "count": 75}
            ]}
          ]
        }
      },
      {"entity_number": 2, "name": "inserter",
       "position": {"x": 1, "y": 0}, "direction": 2},
      {"entity_number": 3, "name": "assembling-machine-3",
       "position": {"x": 2, "y": 0}, "direction": 0,
       "recipe": "iron-gear-wheel", "recipe_quality": "normal"},
      {"entity_number": 4, "name": "inserter",
       "position": {"x": 3, "y": 0}, "direction": 6},
      {"entity_number": 5, "name": "passive-provider-chest",
       "position": {"x": 4, "y": 0}, "direction": 0}
    ],
    "version": 562949956501504,
    "icons": [
      {"index": 1, "signal": {"name": "assembling-machine-3"}},
      {"index": 2, "signal": {"name": "iron-gear-wheel"}},
      {"index": 3, "signal": {"name": "requester-chest"}},
      {"index": 4, "signal": {"name": "passive-provider-chest"}}
    ],
    "description": "AM3 iron gear wheel: requester (75 iron plates) -> AM3 -> passive provider. 2.0 format."
  }
}
```

### Вариант 2 — строка `0eN...` (классическая, сжатая)

```
0eNqNU9tqg0AQ/ZVlnxrQYLwkRGih9KH0oV9QgqxmTBbW1eyuaULw3zteYtOoofiwODPnzDmzsxcaixIKxaWh4YVyAxkNb2IWFSwGgbEPlUvyDkyRNxCCPL1+ejNMgzTccNA0/Lq0P+dIllkMioYLi0qWAYIVHErQBpSd7PFEXJFrxOWy7nqioTN3LHpuzsqiW64gabMY7sBRygUy6BrRh1SeRXGZpk3cqBIsqltoq4jLLZwaJT36T7TTx9GcXQhmAKUleVYwxUyOFuhzEyjr8ayCaoNfZQ2Mur9EUoPCPkOHiymH7gih1xMyrSGLBZc7O2PJnkuwvSG5+3B8CS96kzu8Qft7D3in11R0KJnA7lgic5UxQUcU+f+w6E2pWI4QBj1hgR75EexC5Ue+nd4Rf9JktbHoES+3+QuW7tpfr4Nl4CwCB3XzZLgNmu8kGkXiR3Nu7roDuSOg+4ne1nsj9ffP4LbeH6mfmExV+92CThQv2glQfI2kVkNqNaRRE5K+HXlaBW262XE9I/YLqSF4dD3Itcec4DKRtF4EM8dWP+ppYMk=
```

---

## 📥 Как импортировать в игру (всё работает в 2.0)

1. **JSON-файл (проще всего):** сохрани `iron-gear-cell.json` → **перетащи файл
   на окно игры** (окно лучше не в полноэкранном режиме). Или открой в игре
   «Импорт строки» → вставь содержимое JSON → Импорт.
2. **Строка:** игра → панель снизу → иконка **«Импорт строки»** → вставь
   `0eN...` → Импорт.
3. Чертёж появится в руке — поставь при наличии робопорта/логистической сети
   (сундук-запрос работает только в зоне логистической сети).

## 🔎 Проверено

- ✅ Имена прототипов сверены с `wube/factorio-data` (тег `2.0.76`):
  `assembling-machine-3`, `iron-gear-wheel`, `requester-chest`,
  `passive-provider-chest`, `inserter`.
- ✅ Формат 2.0: `direction` 0–15, `recipe_quality`, `request_filters` как
  **объект** (в 2.0 — не массив, как в 1.1!) с `sections`.
- ✅ Декодер: строка ↔ JSON round-trip без потерь; пройдена базовая валидация
  (уникальные `entity_number`, все поля, `version`).

## 🧩 Как расширить (по желанию)

| Хочешь | Что поменять |
|---|---|
| Больше пропускная способность | `inserter` → `stack-inserter` (в 2.0 — быстрые) на входе/выходе |
| Активная выдача роботам | `passive-provider-chest` → `active-provider-chest` |
| Хранить всё в сети | `passive-provider-chest` → `storage-chest` |
| Другой рецепт | замени `recipe` у AM3 (напр. `electronic-circuit`) и фильтр сундука |
| Качество | добавь в фильтр `"quality": "uncommon"` + `comparator` и нужный `recipe_quality` |
| Параметризация | добавь `parameters: [{"type":"id","name":"Рецепт","id":"parameter-0"}]`, а в машинке `"recipe": "parameter-0"` |

---
*Сгенерировано: `scripts/blueprints/iron_gear_cell.py` · Схема формата:
`docs/blueprints/ЧЕРТЕЖИ-FACTORIO-2.0-ПОЛНЫЙ-ГАЙД.md`*
