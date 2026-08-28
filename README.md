# factoriomodstest2 — репозиторий для разработки модов Factorio

Пока репозиторий содержит **исследовательскую базу** (готовимся к созданию модов):

## 📂 Что здесь

| Путь | Что это |
|---|---|
| `docs/ГЛАВНЫЙ_ОТЧЁТ_Factorio_2.0_и_моддинг.md` | 🎯 **Главный отчёт**: всё про обновления 2.0 → 2.0.76 (хронология всех 70 публичных версий, все системы), полный разбор моддинга, API-изменений, графики/анимаций/3D-пайплайна, звука, локализации, публикации + план, как я буду делать моды |
| `docs/changelogs/полный-официальный-ченджлог-2.0.7-2.0.76.md` | Дословные официальные ченджлоги всех версий (из `wube/factorio-data/changelog.txt`) |
| `docs/changelogs/modding-scripting-API-изменения-2.0.md` | По-версионная выжимка ВСЕХ изменений Modding/Scripting API — шпаргалка при обновлении модов |
| `docs/ссылки-и-инструменты.md` | Быстрый список всех ссылок и инструментов (официальные + коммьюнити) |

## 🗺 План (после согласования идеи мода)

```
mods/<имя-мода>/
├── info.json · changelog.txt · settings.lua
├── data.lua · data-updates.lua · data-final-fixes.lua · control.lua
├── prototypes/ · locale/{en,ru}/ · graphics/ · sound/ · migrations/
└── thumbnails/thumbnail.png
art/ (Blender-исходники, рендер-скрипты) · scripts/ (spriter-пайплайн) · tests/ · .github/workflows/
```

## 📌 Статус версий на 28.08.2026

- **Stable:** 2.0.77 · **Experimental:** 2.1.17 (ветка 2.1 с 26.06.2026, FFF-444)
- Запрошенный диапазон 2.0 → 2.0.76 полностью покрыт отчётом (2.0.0–2.0.6 — закрытые тестовые сборки, публичный ченджлог начинается с 2.0.7).

## 🔗 Ссылки

Официальные: [factorio.com](https://factorio.com) · [блог/FFF](https://factorio.com/blog) · [вики](https://wiki.factorio.com) · [API Lua](https://lua-api.factorio.com/latest/) · [инструменты моддера (данные игры)](https://github.com/wube/factorio-data) · [Mod Portal](https://mods.factorio.com) · [форумы](https://forums.factorio.com)
