# -*- coding: utf-8 -*-
"""
Демо-примеры генерации чертежей Factorio 2.0 через blueprint_lib.
Запуск: python3 scripts/blueprints/examples.py
Результат: blueprints/examples/<имя>.json (pretty) + <имя>.txt (строка чертежа)
и печать строк в консоль.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from blueprint_lib import (  # noqa: E402
    blueprint, blueprint_book, entity, wire, icon, signal, condition,
    combinator_sections, request_filters, train_schedule, train_stop_entity,
    encode, to_json,
)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "blueprints", "examples")
os.makedirs(OUT, exist_ok=True)


# ---------------------------------------------------------------- пример 1
def example_smelter():
    """Мини-плавка: печка + инсертер + лента (direction 2.0!)."""
    ents = [
        entity(1, "stone-furnace", 0, 0),
        entity(2, "burner-inserter", 1, 0, direction="west"),
        entity(3, "transport-belt", 2, 0, direction="east"),
        entity(4, "transport-belt", 3, 0, direction="east"),
        entity(5, "transport-belt", 4, 0, direction="east"),
    ]
    return blueprint(
        "Smelter 1 (fish-furnace demo)",
        ents,
        icons=[icon(signal("stone-furnace"), 1), icon(signal("iron-plate"), 2)],
        version=562949956501504,
    )


# ---------------------------------------------------------------- пример 2
def example_logic():
    """2.0-логика: постоянные комбинаторы (sections) + decider + провода."""
    ents = [
        entity(1, "constant-combinator", 0, 0,
               control_behavior=combinator_sections([
                   [{"name": "iron-plate", "quality": "normal",
                     "comparator": "=", "count": 10}],
                   [{"name": "copper-plate", "quality": "normal",
                     "comparator": "=", "count": 5}],
               ], groups=["Iron", "Copper"])),
        entity(2, "decider-combinator", 2, 0, direction="east",
               control_behavior={
                   "decider_conditions": {
                       "conditions": [condition(first_signal=signal("iron-plate"),
                                                comparator=">", constant=5)],
                       "red_output_signal": signal("green-wire"),
                       "blue_output_signal": signal("red-wire"),
                       "copy_count_from_input": True,
                   }
               }),
    ]
    ws = [
        wire(1, "red", 2, "red"),         # 2.0: wire_connector_id 1 = circuit red (input)
        wire(1, "green", 2, "green"),
    ]
    return blueprint(
        "Logic demo (2.0)",
        ents,
        wires=ws,
        icons=[icon(signal("constant-combinator"), 1)],
        version=562949956501504,
    )


# ---------------------------------------------------------------- пример 3
def example_book():
    """Книга с двумя чертежами."""
    b1 = example_smelter()
    b2 = blueprint(
        "Empty chest",
        [entity(1, "logistic-chest-storage", 0, 0),
         entity(2, "wooden-chest", 3, 1, direction="south")],
        icons=[icon(signal("logistic-chest-storage"), 1)],
        version=562949956501504,
    )
    return blueprint_book(
        "Demo book",
        [b1, b2],
        icons=[icon(signal("blueprint-book"), 1)],
        version=562949956501504,
    )


def main():
    examples = [
        ("smelter-demo", example_smelter()),
        ("logic-demo", example_logic()),
        ("demo-book", example_book()),
    ]
    for name, obj in examples:
        json_path = os.path.join(OUT, name + ".json")
        txt_path = os.path.join(OUT, name + ".txt")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(to_json(obj))
        string = encode(obj)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(string + "\n")
        print(f"== {name}")
        print(f"   JSON : {json_path}")
        print(f"   string: {string[:70]}...")
    print("Готово.")


if __name__ == "__main__":
    main()
