# {{MOD_TITLE}} ({{MOD_NAME}})

Мод для Factorio 2.0.x.

## Установка
1. Скопируй `releases/{{MOD_NAME}}_1.0.0.zip` в папку модов
   (`%APPDATA%\Factorio\mods` / `~/.factorio/mods`).
2. Включи в игре → перезапуск.

## Разработка
- `python3 scripts/new_mod.py {{MOD_NAME}} "{{MOD_TITLE}}"` — создать мод из шаблона
- `python3 scripts/build_mod.py mods/{{MOD_NAME}}` — собрать zip в releases/
- `python3 tests/smoke_test.py` — проверить прототипы (после адаптации теста)
