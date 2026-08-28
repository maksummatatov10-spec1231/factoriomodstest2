#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
new_mod.py — создать новый мод из шаблона templates/mod-template.

Использование:
  python3 scripts/new_mod.py my-cool-mod "My Cool Mod" [--desc "Описание"]

Важно (уроки fish-furnace):
  * имя мода: только [a-z0-9-_];
  * factorio_version всегда "2.0" (пиратка 2.0.76);
  * графика/звуки — только свои или ванильные, пути проверять;
  * все типы прототипов сверять с lua-api.factorio.com/2.0.76/.
"""
import argparse
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "templates", "mod-template")
MODS = os.path.join(ROOT, "mods")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", help="имя мода (a-z0-9-)")
    ap.add_argument("title", help="заголовок (показывается в игре)")
    ap.add_argument("--desc", default="", help="описание")
    ap.add_argument("--author", default="maksummatatov10")
    ap.add_argument("--version", default="1.0.0")
    args = ap.parse_args()

    name = args.name.lower()
    if not re.fullmatch(r"[a-z0-9\-_]+", name):
        print("ОШИБКА: имя мода может содержать только a-z, цифры, - и _")
        sys.exit(1)

    dest = os.path.join(MODS, name)
    if os.path.exists(dest):
        print(f"ОШИБКА: mods/{name} уже существует")
        sys.exit(1)

    shutil.copytree(TEMPLATE, dest)
    # подстановка плейсхолдеров
    for root, dirs, files in os.walk(dest):
        for f in files:
            p = os.path.join(root, f)
            try:
                s = open(p, encoding="utf-8").read()
            except Exception:
                continue
            s = (s.replace("{{MOD_NAME}}", name)
                  .replace("{{MOD_TITLE}}", args.title)
                  .replace("{{MOD_DESCRIPTION}}", args.desc or f"{args.title} mod for Factorio 2.0")
                  .replace('"version": "1.0.0"', f'"version": "{args.version}"'))
            open(p, "w", encoding="utf-8").write(s)

    # переименовать пример (чтобы data.lua не ссылался на несуществующее — оставим как есть)
    print(f"✅ Создан мод: mods/{name}")
    print("   Правки перед работой:")
    print("   - prototypes/example.lua: замени на свои сущности/предметы")
    print("   - data.lua: подключи свои prototypes/*.lua")
    print("   - locale/en, locale/ru: заполни все секции")
    print("   - graphics/, sound/: добавь свои файлы (пути — только существующие!)")
    print("   - python3 scripts/build_mod.py mods/%s  # собрать zip" % name)


if __name__ == "__main__":
    main()
