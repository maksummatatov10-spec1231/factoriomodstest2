#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
export_scripts_to_json.py — собирает все скрипты проекта в папку «скрипты/»
в виде JSON-файлов с русскими именами.

Структура каждого JSON:
{
  "имя": "Название",
  "описание": "...",
  "язык": "Python",
  "исходный_путь": "scripts/...",
  "код": "<полный исходный код файла>"
}

Запуск: python3 scripts/export_scripts_to_json.py
(повторный запуск пересоздаёт все файлы — синхронизация с исходниками)
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "скрипты")

# (русское имя файла, заголовок, описание, относительный путь, язык)
SCRIPTS = [
    (
        "генератор-графики-рыбной-печки.json",
        "Генератор графики Рыбной печки",
        "Полностью программная генерация всех спрайтов мода fish-furnace: "
        "корпус с чешуёй и глазами, 48 кадров пламени, свечение, тень, "
        "останки, иконки, анимация-превью. Только Python + Pillow, без AI.",
        "scripts/generate_fish_furnace_graphics.py",
        "Python",
    ),
    (
        "генератор-миниатюры-мода.json",
        "Генератор миниатюры мода",
        "Создаёт thumbnail.png 512x512 для мода: тёмный градиентный фон, "
        "виньетка, свечение и печка по центру.",
        "scripts/make_thumbnail.py",
        "Python",
    ),
    (
        "кодек-чертежей-factorio-2.json",
        "Кодек чертежей Factorio 2.0",
        "Библиотека для кодирования/декодирования строк чертежей "
        "(0 + base64 + zlib + JSON) и конструкторы структур JSON 2.0: "
        "сущности, провода, сигналы, расписания, параметризация.",
        "scripts/blueprints/blueprint_lib.py",
        "Python",
    ),
    (
        "примеры-чертежей.json",
        "Примеры чертежей",
        "Демо-генераторы чертежей: плавка, логика с комбинаторами, книга "
        "чертежей. Создаёт JSON и строки 0eN... в папке blueprints/examples.",
        "scripts/blueprints/examples.py",
        "Python",
    ),
    (
        "чертёж-железные-шестерни-генератор.json",
        "Генератор чертежа: железные шестерни (AM3)",
        "Схема: сундук-запрос (75 плит) -> инсертер -> сборщик 3 ур. "
        "(рецепт iron-gear-wheel) -> инсертер -> сундук снабжения. "
        "Координаты, направления 2.0, фильтры с качеством.",
        "scripts/blueprints/iron_gear_cell.py",
        "Python",
    ),
    (
        "создать-мод-из-шаблона.json",
        "Создать мод из шаблона",
        "Команда new_mod: копирует templates/mod-template в mods/<имя> и "
        "подставляет имя, заголовок, описание, версию.",
        "scripts/new_mod.py",
        "Python",
    ),
    (
        "собрать-мод-в-zip.json",
        "Собрать мод в ZIP",
        "Проверяет info.json, обязательные файлы, пути к ассетам и собирает "
        "releases/<имя>_<версия>.zip с правильной папкой внутри.",
        "scripts/build_mod.py",
        "Python",
    ),
    (
        "смоук-тест-мода.json",
        "Смоук-тест мода",
        "Запускает прототипы мода в настоящем LuaJIT (lupa), проверяет типы "
        "TriggerEffectItem, frame_count, scale, пути к ассетам, локализацию, "
        "info.json.",
        "tests/smoke_test.py",
        "Python",
    ),
    (
        "тест-кодека-чертежей.json",
        "Тест кодека чертежей",
        "Round-trip на реальных строках чертежей 2.0, проверка качества, "
        "направлений, проводов, комбинаторов, книг.",
        "tests/test_blueprints.py",
        "Python",
    ),
    (
        "экспорт-скриптов-в-json.json",
        "Экспорт скриптов в JSON",
        "Этот самый скрипт: собирает все скрипты проекта в папку «скрипты/» "
        "в виде JSON-файлов с русскими именами.",
        "scripts/export_scripts_to_json.py",
        "Python",
    ),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    for fname, title, desc, rel, lang in SCRIPTS:
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            print(f"ПРОПУСК (нет файла): {rel}")
            continue
        code = open(path, encoding="utf-8").read()
        payload = {
            "имя": title,
            "описание": desc,
            "язык": lang,
            "исходный_путь": rel,
            "код": code,
        }
        out_path = os.path.join(OUT_DIR, fname)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"OK: {fname}  ({len(code)} символов кода)")
    print(f"\nГотово. Папка: {OUT_DIR}")


if __name__ == "__main__":
    main()
