# factoriomodstest2 — репозиторий для разработки модов Factorio

## ✅ Первый мод готов: **Fish Furnace (Рыбная печка)**

> 📦 **Готовый архив для установки:**
> `mods/fish-furnace/releases/fish-furnace_1.0.1.zip`
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

## 📌 Статус версий на сегодня

- **Stable:** 2.0.77 · **Experimental:** 2.1.17 (ветка 2.1, 26.06.2026)
- Мод целит в **2.0.x** (`base >= 2.0.0`), Space Age не требуется
