#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_mod.py — собрать мод в zip с правильной структурой + базовые проверки.

Использование:
  python3 scripts/build_mod.py mods/<name>

Что делает:
  * проверяет info.json (name/version/factorio_version="2.0");
  * проверяет обязательные файлы (data.lua, locale en/ru);
  * собирает releases/<name>_<version>.zip c папкой <name>_<version>/ внутри
    (без этого мод НЕ загрузится!);
  * выводит список файлов, которых не хватает.

Правила из docs/моддинг-уроки-и-недочёты.md:
  * zip содержит ПАПКУ name_version/ (не файлы в корне);
  * версия синхронна: info.json + changelog + README.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    if len(sys.argv) < 2:
        print("Использование: python3 scripts/build_mod.py mods/<name>")
        sys.exit(1)
    mod_path = os.path.abspath(sys.argv[1])
    if not os.path.isdir(mod_path):
        print("ОШИБКА: папка мода не найдена:", mod_path)
        sys.exit(1)

    info_path = os.path.join(mod_path, "info.json")
    if not os.path.exists(info_path):
        print("ОШИБКА: нет info.json")
        sys.exit(1)
    info = json.load(open(info_path, encoding="utf-8"))
    name = info["name"]
    version = info["version"]
    if info.get("factorio_version") != "2.0":
        print("⚠️  factorio_version != 2.0 (пиратка 2.0.76 — проверь!)")

    # обязательные файлы
    missing = []
    for rel in ("data.lua", "locale/en/base.cfg", "locale/ru/base.cfg", "info.json"):
        if not os.path.exists(os.path.join(mod_path, rel)):
            missing.append(rel)
    if missing:
        print("❌ Не хватает обязательных файлов:", missing)
        sys.exit(1)

    # пути к ассетам внутри прототипов
    asset_missing = []
    import re as _re
    for root, dirs, files in os.walk(os.path.join(mod_path, "prototypes")):
        for f in files:
            if not f.endswith(".lua"):
                continue
            txt = open(os.path.join(root, f), encoding="utf-8").read()
            for m in _re.finditer(r'filename\s*=\s*"__([\w-]+)__/(.+?)"', txt):
                mod, rel = m.group(1), m.group(2)
                if mod != name:
                    continue  # ванильные не проверяем
                p = os.path.join(mod_path, rel)
                if not os.path.exists(p):
                    asset_missing.append(f"{mod}__/{rel}")

    out_dir = os.path.join(mod_path, "releases")
    os.makedirs(out_dir, exist_ok=True)
    zip_path = os.path.join(out_dir, f"{name}_{version}.zip")
    folder = f"{name}_{version}"
    with tempfile.TemporaryDirectory() as td:
        staging = os.path.join(td, folder)
        # копируем всё, кроме releases
        shutil.copytree(mod_path, staging,
                        ignore=shutil.ignore_patterns("releases", ".git", "__pycache__"))
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for root, dirs, files in os.walk(staging):
                for f in files:
                    full = os.path.join(root, f)
                    arc = os.path.join(folder, os.path.relpath(full, staging))
                    z.write(full, arc)

    print(f"✅ Собрано: {zip_path}  ({os.path.getsize(zip_path)//1024} KB)")
    print(f"   Внутри папка: {folder}/")
    if asset_missing:
        print("❌ НЕ СУЩЕСТВУЮТ файлы (из prototypes):")
        for a in asset_missing:
            print("   -", a)
        sys.exit(1)
    print("   Проверка путей к ассетам: OK")


if __name__ == "__main__":
    main()
