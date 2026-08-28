# factoriomodstest2 — репозиторий для разработки модов Factorio

## ✅ Первый мод готов: **Fish Furnace (Рыбная печка)**

> 📦 **Готовый архив для установки:**
> `mods/fish-furnace/releases/fish-furnace_1.0.3.zip`
> (скопируй в папку `%APPDATA%\Factorio\mods` → включи в игре → перезапуск)

| Что | Описание |
|---|---|
| 🐟 Крафт | **50 × сырая рыба** — вручную или в сборочной машине |
| 🔬 Технология | **Рыбная печка** — 1 красная колба в лаборатории (после Automation) |
| ⚙️ Механика | Как каменная печка, но **×4 скорость**, любое химическое топливо, 360 kW, 8 загрязнения |
| 🎨 Графика | **Полностью сгенерирована кодом** (Python + Pillow, ни одного AI-изображения): чешуя, моргающие рыбие глаза, зубы, плавники, **48 кадров пламени** (value-noise), свечение, свет на земле, тень, останки, отражение в воде |
| 🌍 Языки | **English + Русский** |
| 📄 Файлы | `mods/fish-furnace/` (исходники) + `releases/` (zip) + `art/fish-furnace/preview-*.png` |
| 🧪 Проверено | LuaJIT-смоук-тест `tests/smoke_test.py` — все прототипы, пути, локали валидны |

**Превью в игре:** `art/fish-furnace/preview-in-game.jpg` · **Спрайты:** `art/fish-furnace/preview-sprites.png` · **Анимация:** `art/fish-furnace/preview.gif`

---

## 📂 Структура репозитория

```
mods/fish-furnace/          ← первый мод (исходники)
│   ├── info.json / changelog.txt / data.lua / README.md
│   ├── prototypes/ (entity, item, recipe, technology)
│   ├── locale/en + locale/ru
│   ├── graphics/ (кодовые PNG-шиты)
│   ├── thumbnails/thumbnail.png
│   └── releases/fish-furnace_1.0.0.zip   ← ГОТОВЫЙ МОД
docs/                       ← исследования: отчёт по 2.0–2.0.76, ченджлоги, API
scripts/                    ← генераторы графики (Python/Pillow), thumbnail
tests/smoke_test.py         ← проверка прототипов (LuaJIT)
art/fish-furnace/           ← превью (gif, jpg)
```

## 🛠 Как перегенерировать графику/проверить

```bash
python3 scripts/generate_fish_furnace_graphics.py  # все PNG + preview.gif
python3 scripts/make_thumbnail.py                  # thumbnail.png
python3 tests/smoke_test.py                        # тест прототипов
```

## 📚 Память проекта (обязательно к прочтению перед следующим модом)

**`docs/моддинг-уроки-и-недочёты.md`** — все ошибки, допущенные в Fish Furnace (4
критических фикса: `direct` вместо TriggerEffectItem, несуществующий звук,
Different frame counts, scale-размер в 2 раз) + все правила и чек-лист перед
релизом. Кратко:

1. **Источник истины** — ванильный код (`wube/factorio-data`) + официальные
   доки `lua-api.factorio.com/2.0.76/`. Любое поле/тип/файл — сначала проверить.
2. **Экранный размер = файл × scale.** 2x-файлы → `scale = 0.25`.
3. **frame_count одинаковый во всех слоях анимации**; повторы — `repeat_count`.
4. **Пути к звукам/графике** — только существующие файлы (не выдумывать).
5. **`damaged_trigger_effect` и др.** — типы из TriggerEffectItem, НЕ direct.
6. **Тест обязателен**: `python3 tests/smoke_test.py` перед каждым коммитом.

## 🗂 Шаблон для следующего мода

- `templates/mod-template/` — готовая структура (info.json, data, control,
  settings, локали en/ru, graphics, sound, changelog, README).
- `python3 scripts/new_mod.py <имя> "<Заголовок>"` — создать мод из шаблона.
- `python3 scripts/build_mod.py mods/<имя>` — собрать `releases/<имя>_<версия>.zip`
  с правильной папкой внутри + проверка путей к ассетам.

## 📐 Чертежи: генерация кодом (готово к работе!)

Формат, JSON-схема 2.0 (качество, 16 направлений, wires, расписания,
параметризация), Lua API и все способы импорта — в
`docs/blueprints/ЧЕРТЕЖИ-FACTORIO-2.0-ПОЛНЫЙ-ГАЙД.md`.

- `scripts/blueprints/blueprint_lib.py` — кодек (encode/decode) + конструкторы;
- `scripts/blueprints/examples.py` + `blueprints/examples/` — демо-чертежи
  (JSON для импорта + строки 0eN...);
- `tests/test_blueprints.py` — тесты на реальных строках 2.0.

`python3 scripts/blueprints/examples.py` · `python3 tests/test_blueprints.py`

**Импорт в игру (2.0):** вставь JSON или строку `0eN...` в «Импорт строки»,
или перетащи `.json`-файл на окно игры.

## 📌 Статус версий на сегодня

- **Stable:** 2.0.77 · **Experimental:** 2.1.17 (ветка 2.1, 26.06.2026)
- Мод целит в **2.0.x** (`base >= 2.0.0`), Space Age не требуется
