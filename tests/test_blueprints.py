# -*- coding: utf-8 -*-
"""
Тесты кодера чертежей: round-trip на реальных строках 2.0 + примеры +
базовая валидация структуры.

Реальные эталонные строки: tests/data/bp/*.bp (взяты из
github.com/redruin1/factorio-blueprint-schemas — официальная проверка 2.0).
"""
import base64
import json
import os
import sys
import zlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "scripts", "blueprints"))
from blueprint_lib import (  # noqa: E402
    decode, encode, validate, entity, wire, blueprint, blueprint_book,
    combinator_sections, VERSION_2_0,
)

DATA = os.path.join(os.path.dirname(__file__), "data", "bp")


def test_decode_real_strings():
    for fn in sorted(os.listdir(DATA)):
        if not fn.endswith(".bp"):
            continue
        s = open(os.path.join(DATA, fn)).read().strip()
        obj = decode(s)
        assert "blueprint" in obj or "blueprint_book" in obj, fn
        bp = obj.get("blueprint", {})
        assert bp.get("item") == "blueprint", fn
        assert bp.get("version"), fn
        assert bp.get("entities"), f"{fn}: нет сущностей"


def test_roundtrip():
    for fn in sorted(os.listdir(DATA)):
        if not fn.endswith(".bp"):
            continue
        s = open(os.path.join(DATA, fn)).read().strip()
        obj = decode(s)
        s2 = encode(obj)
        assert s2.startswith("0"), "нет префикса версии"
        assert decode(s2) == obj, f"round-trip не совпал: {fn}"


def test_wire_format():
    # wires из эталона: [from_id, conn, to_id, conn]
    s = open(os.path.join(DATA, "test_accumulators.bp")).read().strip()
    obj = decode(s)
    w = obj["blueprint"]["wires"][0]
    assert len(w) == 4 and isinstance(w[0], int)


def test_quality_and_direction():
    s = open(os.path.join(DATA, "test_accumulators.bp")).read().strip()
    obj = decode(s)
    bp = obj["blueprint"]
    ents = {e["entity_number"]: e for e in bp["entities"]}
    e2 = ents[2]
    assert e2.get("quality") == "legendary", "2.0: quality у сущности"


def test_make_blueprint():
    b = blueprint(
        "Test",
        [entity(1, "stone-furnace", 0, 0),
         entity(2, "burner-inserter", 1, 0, direction="west")],
        wires=[wire(1, "copper", 2, "copper")],
        icons=[{"index": 1, "signal": {"name": "stone-furnace"}}],
        version=VERSION_2_0,
    )
    assert b["blueprint"]["entities"][0].get("direction") is None
    e2 = b["blueprint"]["entities"][1]
    assert e2["direction"] == 6  # west в 2.0 (0..15)
    assert validate(b) == []


def test_book():
    b1 = blueprint("A", [entity(1, "stone-furnace", 0, 0)], version=VERSION_2_0)
    book = blueprint_book("Book", [b1], version=VERSION_2_0)
    assert book["blueprint_book"]["blueprints"][0]["index"] == 0
    assert validate(book) == []


def test_combinator_sections():
    cb = combinator_sections([[{"name": "iron-plate", "count": 1}]])
    sec = cb["sections"]["sections"][0]
    assert sec["index"] == 1
    assert sec["filters"][0]["name"] == "iron-plate"
    assert sec["filters"][0]["index"] == 1


def test_direction_values():
    from blueprint_lib import DIRECTIONS
    assert DIRECTIONS["north"] == 0
    assert DIRECTIONS["east"] == 2
    assert DIRECTIONS["south"] == 4
    assert DIRECTIONS["west"] == 6


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("OK ", name)
            except Exception as e:
                failed += 1
                print("FAIL", name, "->", e)
    sys.exit(1 if failed else 0)
