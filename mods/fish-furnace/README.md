# 🐟 Fish Furnace (Рыбная печка)

**Мод для Factorio 2.0 (Space Age совместим).**

## Что это

Рыбная печка — печка **из 50 рыб**, работающая как каменная, но **в 4 раза быстрее**.
Сжигает любое химическое топливо (уголь, дерево, твёрдое топливо и т.д.).

- 🔧 Крафт: **50 × сырая рыба** (`raw-fish`) — вручную или в сборочной машине
- 🔬 Технология: **Рыбная печка** — 1 красная колба в лаборатории (`automation` — доступна рано)
- 🖼 Вся графика сгенерирована **программно** (никакого AI): чешуя, рыбий глаз (моргает!), зубы, плавники, 48 кадров пламени на основе value-noise, аддитивное свечение, тень, останки, отражение в воде
- 🌍 Локализация: **English + Русский**
- ⚡ Оптимизировано: 1 файл-лист корпуса (2 кадра), сжатый PNG

## Установка

1. Скопируй `releases/fish-furnace_1.0.0.zip` в папку модов:
   - Windows: `%APPDATA%\Factorio\mods`
   - Linux: `~/.factorio/mods`
   - macOS: `~/Library/Application Support/factorio/mods`
2. Запусти игру → Mods → включи **Fish Furnace** → подтверди перезапуск
3. Играй: исследуй технологию «Рыбная печка» → крафти 50 рыб → ставь печку

> Версия игры: **2.0.x** (base >= 2.0.0). Space Age не обязателен.

## Параметры (как каменная печка, но x4)

| Параметр | Каменная печка | Рыбная печка |
|---|---|---|
| Скорость крафта | 1 | **4** |
| Потребление | 90 kW | 360 kW |
| Загрязнение | 2/мин | 8/мин |
| Топливо | chemical | chemical |
| Здоровье | 200 | 200 |
| Останки | stone-furnace-remnants | fish-furnace-remnants |

## Структура

```
fish-furnace/
├── info.json            # метаданные (name, version, 2.0, deps)
├── changelog.txt
├── data.lua
├── prototypes/
│   ├── entity.lua       # furnace + corpse
│   ├── item.lua
│   ├── recipe.lua
│   └── technology.lua
├── locale/{en,ru}/base.cfg
├── graphics/            # сгенерировано scripts/generate_fish_furnace_graphics.py
├── thumbnails/thumbnail.png
└── releases/
    └── fish-furnace_1.0.0.zip   ← ГОТОВЫЙ АРХИВ ДЛЯ УСТАНОВКИ
```

## Регенерация графики

```bash
python3 scripts/generate_fish_furnace_graphics.py   # все PNG + preview.gif
python3 scripts/make_thumbnail.py                   # thumbnail.png
python3 tests/smoke_test.py                         # проверка прототипов (LuaJIT)
```

## Лицензия

MIT (код и графика).
