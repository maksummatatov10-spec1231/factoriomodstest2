# -*- coding: utf-8 -*-
"""
Генератор чертежа: Assembling Machine 3 (зелёный сборщик) → железные шестерни.
Схема: requester chest → inserter → AM3 (iron-gear-wheel) → inserter → passive provider chest.

Формат: JSON 2.0 (quality, direction 0..15, wires, request_filters как объект).
Выход в blueprints/iron-gear-cell/: .json, .txt (строка 0eN...), .md (описание).

Прототипы подтверждены по официальному wube/factorio-data (тег 2.0.76):
  assembling-machine-3 (crafting_speed 1.25), iron-gear-wheel
  (2× iron-plate → 1× wheel, 0.5s), requester-chest, passive-provider-chest, inserter.
Референс по расчёту буфера: factrioprints.com — Assembler Quality Upcycling
(IRON GEAR: 5 plates/s на AM3 → 30s буфер = 150 plates → запрос 75).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blueprint_lib import (  # noqa: E402
    blueprint, entity, icon, signal, encode, validate, VERSION_2_0,
)

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "blueprints", "iron-gear-cell")
os.makedirs(OUT, exist_ok=True)

# ---- координаты (тайлы, X растёт на восток, Y на юг) ----
# requester chest   (0, 0)
# input  inserter   (1, 0)  direction east  (2)
# assembling-mach-3 (2, 0)  direction north (0)
# output inserter   (3, 0)  direction west  (6)
# provider chest    (4, 0)

REQUEST_FILTERS = {
    "request_from_buffers": True,
    "sections": [
        {
            "index": 1,
            "filters": [
                {"index": 1, "name": "iron-plate", "comparator": "=", "count": 75}
            ]
        }
    ],
}


def build():
    ents = [
        entity(1, "requester-chest", 0, 0, direction=0,
               request_filters=REQUEST_FILTERS),
        entity(2, "inserter", 1, 0, direction=2),          # east → в машину
        entity(3, "assembling-machine-3", 2, 0, direction=0,
               recipe="iron-gear-wheel", recipe_quality="normal"),
        entity(4, "inserter", 3, 0, direction=6),          # west → в сундук
        entity(5, "passive-provider-chest", 4, 0, direction=0),
    ]
    return blueprint(
        "Iron Gear Cell (AM3)",
        ents,
        icons=[
            icon(signal("assembling-machine-3"), 1),
            icon(signal("iron-gear-wheel"), 2),
            icon(signal("requester-chest"), 3),
            icon(signal("passive-provider-chest"), 4),
        ],
        description="AM3 iron gear wheel: requester (75 iron plates) -> AM3 -> passive provider. 2.0 format.",
        version=VERSION_2_0,
    )


def main():
    obj = build()
    errs = validate(obj)
    assert not errs, errs

    text = json.dumps(obj, ensure_ascii=False, indent=2)
    string = encode(obj)

    with open(os.path.join(OUT, "iron-gear-cell.json"), "w", encoding="utf-8") as f:
        f.write(text + "\n")
    with open(os.path.join(OUT, "iron-gear-cell.txt"), "w", encoding="utf-8") as f:
        f.write(string + "\n")

    # round-trip проверка
    from blueprint_lib import decode
    assert decode(string) == obj
    print("OK: round-trip + validate. Длина строки:", len(string))
    print("Файлы:", OUT)


if __name__ == "__main__":
    main()
