# -*- coding: utf-8 -*-
"""
factorio_blueprint_lib — кодирование/декодирование чертежей Factorio 2.0
и конструктор JSON-структур чертежей. Только стандартная библиотека Python.

Формат строки чертежа (официально, wiki.factorio.com/Blueprint_string_format):
    '0' + base64( zlib( json ) )
    - первый байт/символ — версия контейнера, сейчас всегда '0';
    - zlib deflate, уровень сжатия 9;
    - base64 (стандартный алфавит).
    Начиная с 2.0 игра принимает и «сырой» JSON (minified или pretty) как
    строку импорта, и JSON-файл перетаскиванием на окно игры.

Особенности JSON для 2.0 (отличаются от 1.1!):
    - direction: 0..15 (в 1.1 было 0..7 — значения удвоены);
    - quality: у entity / filters / signals ("normal","uncommon",...);
    - recipe_quality у assembling-machine;
    - wires: единый список соединений [[from_id, from_conn, to_id, to_conn], ...]
      вместо per-entity "connections" (wire_connector_id: 1=красный, 2=зелёный,
      3=выход комбинатора красный, 4=выход зелёный, 5=медь/полюс, 6=правый полюс);
    - schedules: расписания поездов + прерывания (interrupts) и платформ;
    - stock_connections: соединения вагонов;
    - parameters: параметризация чертежа (id-parameter / number-parameter).

Проверено на реальных строках 2.0 (scattershot.bp, test_accumulators.bp из
https://github.com/redruin1/factorio-blueprint-schemas).
"""
import base64
import json
import zlib

# Версия игры, «зашитая» в реальные чертежи 2.0 (0x000200000002F000).
VERSION_2_0 = 562949956501504

# Определения направлений 2.0 (0..15, по часовой от севера)
DIRECTIONS = {
    "north": 0, "northeast": 1, "east": 2, "southeast": 3,
    "south": 4, "southwest": 5, "west": 6, "northwest": 7,
    "north_2": 8, "northeast_2": 9, "east_2": 10, "southeast_2": 11,
    "south_2": 12, "southwest_2": 13, "west_2": 14, "northwest_2": 15,
}

# wire_connector_id (defines.wire_connector_id для 2.0)
WIRE = {
    "red": 1,          # circuit red (и red input комбинатора)
    "green": 2,        # circuit green (и green input комбинатора)
    "output_red": 3,   # circuit red output комбинатора
    "output_green": 4, # circuit green output комбинатора
    "copper": 5,       # power wire / левый полюс переключателя
    "switch_right": 6, # правый полюс power switch
}


# ------------------------------------------------------------------ кодек
def decode(string):
    """Строка чертежа -> dict (JSON).
    Принимает: '0'+base64+zlib или сразу JSON (строка/file content).
    """
    s = string.strip()
    if s.startswith("{"):
        return json.loads(s)
    if not s.startswith("0"):
        raise ValueError("Неизвестная версия строки чертежа: должна начинаться с '0'")
    raw = base64.b64decode(s[1:])
    return json.loads(zlib.decompress(raw).decode("utf-8"))


def encode(obj, pretty=False, compress=True):
    """dict (JSON чертежа) -> строка чертежа.

    pretty=True -> компакт-несжатый JSON (игра 2.0 принимает JSON напрямую!),
    compress=True (по умолчанию) -> классическая строка '0'+base64+zlib.
    """
    text = json.dumps(obj, ensure_ascii=False,
                      separators=(",", ":") if not pretty else None)
    if not compress:
        return text
    payload = zlib.compress(text.encode("utf-8"), 9)
    return "0" + base64.b64encode(payload).decode("ascii")


def to_json(obj, pretty=False):
    return json.dumps(obj, ensure_ascii=False, indent=2 if pretty else None,
                      separators=None if pretty else (",", ":"))


def from_json(text):
    return json.loads(text)


# ------------------------------------------------------------------ helpers
def _check_name(name):
    assert isinstance(name, str) and name.strip(), "Пустое имя прототипа!"


def signal(name, signal_type="item", quality_name=None):
    """SignalID. В 2.0 'type' опционален (по умолчанию item)."""
    out = {"name": name}
    if signal_type != "item":
        out["type"] = signal_type
    if quality_name:
        out["quality"] = quality_name
    return out


def icon(sig, index):
    return {"index": index, "signal": sig}


def quality(name):
    """Качество ('normal' | 'uncommon' | 'rare' | 'epic' | 'legendary')."""
    assert name in ("normal", "uncommon", "rare", "epic", "legendary"), name
    return name


def entity(number, name, x, y, direction=None, quality_name=None, mirror=None,
           **fields):
    """Базовая сущность чертежа с полями 2.0.

    number  — entity_number (1-based, уникальный в чертеже);
    name    — имя прототипа (например 'stone-furnace', 'assembling-machine-2');
    x, y    — позиция (тайлы, могут быть дробными: 0.5, 1.5, ...);
    direction — 0..15 (2.0!), можно передавать и имя из DIRECTIONS;
    quality_name — качество сущности (2.0);
    mirror  — зеркалирование fluid-боксов (2.0);
    **fields — любые доп. поля (recipe, station, inventory, control_behavior...).
    """
    _check_name(name)
    e = {"entity_number": int(number), "name": name,
         "position": {"x": float(x), "y": float(y)}}
    if direction is not None:
        if isinstance(direction, str):
            direction = DIRECTIONS[direction]
        e["direction"] = int(direction)
    if quality_name:
        e["quality"] = quality(quality_name)
    if mirror is not None:
        e["mirror"] = bool(mirror)
    for k, v in fields.items():
        e[k] = v
    return e


def wire(a_id, a_conn, b_id, b_conn):
    """Соединение проводов 2.0: [entity_number, wire_connector_id, ...].
    a_conn/b_conn — ключ WIRE ('red','green','output_red','copper',...) или число."""
    return [int(a_id), WIRE[a_conn] if isinstance(a_conn, str) else int(a_conn),
            int(b_id), WIRE[b_conn] if isinstance(b_conn, str) else int(b_conn)]


def condition(first_signal=None, comparator="=", constant=None, second_signal=None):
    """CircuitCondition (у 2.0 поля: first_signal, comparator, constant, second_signal)."""
    c = {}
    if first_signal is not None:
        c["first_signal"] = first_signal
    c["comparator"] = comparator
    if second_signal is not None:
        c["second_signal"] = second_signal
    if constant is not None:
        c["constant"] = constant
    return c


def combinator_sections(filters_by_section, groups=None):
    """control_behavior постоянного комбинатора в формате 2.0 (sections).

    filters_by_section: список списков фильтров; каждый фильтр
        {name, quality?, comparator?, count?} (или {"signal": ..., ...}).
    groups: список имён групп (опционально).
    """
    sections = []
    for i, flt_list in enumerate(filters_by_section, 1):
        flts = []
        for j, f in enumerate(flt_list, 1):
            item = {"index": j, "name": f["name"]}
            if "quality" in f:
                item["quality"] = quality(f["quality"])
            if "comparator" in f:
                item["comparator"] = f["comparator"]
            if "count" in f:
                item["count"] = f["count"]
            flts.append(item)
        sec = {"index": i, "filters": flts}
        if groups and groups[i - 1] is not None:
            sec["group"] = groups[i - 1]
        sections.append(sec)
    return {"sections": {"sections": sections}}


def request_filters(items):
    """request_filters (логистические завпросы/фильтры) — список
    {index, name, quality?, comparator?, count?}."""
    out = []
    for i, f in enumerate(items, 1):
        item = {"index": i, "name": f["name"]}
        if f.get("quality"):
            item["quality"] = quality(f["quality"])
        if f.get("comparator"):
            item["comparator"] = f["comparator"]
        if "count" in f:
            item["count"] = f["count"]
        out.append(item)
    return out


def train_schedule(records, interrupts=None):
    """records: [{station, wait_conditions:[{...}]}]; interrupts опционально."""
    sch = {"records": records}
    if interrupts:
        sch["interrupts"] = interrupts
    return sch


def train_stop_entity(number, x, y, station=None, color=None,
                      manual_trains_limit=None, priority=None, **kw):
    """Train stop сущность с полями 2.0 (station, manual_trains_limit, priority).
    color: dict {r,g,b,a}."""
    fields = {}
    if station is not None:
        fields["station"] = station
    if color is not None:
        fields["color"] = color
    if manual_trains_limit is not None:
        fields["manual_trains_limit"] = manual_trains_limit
    if priority is not None:
        fields["priority"] = priority
    fields.update(kw)
    return entity(number, "train-stop", x, y, **fields)


def blueprint(label, entities, tiles=None, icons=None, wires=None,
              schedules=None, stock_connections=None, parameters=None,
              description=None, label_color=None, snap_to_grid=None,
              absolute_snapping=None, version=VERSION_2_0):
    """Собирает объект {'blueprint': {...}}.

    entities — список dict от entity();
    tiles — [{name, position}];
    icons — список dict от icon(signal, index) (до 4);
    wires — список от wire() (2.0!);
    schedules — список {locomotives:[ids], schedule:{records,interrupts}};
    parameters — [{type:'id', name, id, ...}] / [{type:'number', name, ...}].
    """
    bp = {
        "item": "blueprint",
        "label": label,
        "entities": entities,
        "version": version,
    }
    if tiles:
        bp["tiles"] = tiles
    if icons:
        bp["icons"] = icons
    if wires:
        bp["wires"] = wires
    if schedules:
        bp["schedules"] = schedules
    if stock_connections:
        bp["stock_connections"] = stock_connections
    if parameters:
        bp["parameters"] = parameters
    if description:
        bp["description"] = description
    if label_color:
        bp["label_color"] = label_color
    if snap_to_grid:
        bp["snap-to-grid"] = snap_to_grid
    if absolute_snapping is not None:
        bp["absolute-snapping"] = absolute_snapping
    return {"blueprint": bp}


def blueprint_book(label, blueprints, active_index=0, icons=None,
                   description=None, version=VERSION_2_0):
    """blueprints: список объектов {'blueprint': {...}}."""
    items = [{"index": i, **b} for i, b in enumerate(blueprints)]
    bb = {
        "item": "blueprint-book",
        "label": label,
        "blueprints": items,
        "active_index": active_index,
        "version": version,
    }
    if icons:
        bb["icons"] = icons
    if description:
        bb["description"] = description
    return {"blueprint_book": bb}


def deconstruction_planner(label="", entity_filters=None, tile_filters=None,
                           entity_filter_mode=0, tile_filter_mode=0,
                           tiles_only=False, version=VERSION_2_0):
    """Деструктор. filter_mode: 0=whitelist, 1=blacklist.
    entity_filters/tile_filters: [{name, index}]."""
    dp = {
        "item": "deconstruction-planner",
        "label": label,
        "entity_filters": entity_filters or [],
        "tile_filters": tile_filters or [],
        "entity_filter_mode": entity_filter_mode,
        "tile_filter_mode": tile_filter_mode,
        "tiles_only": tiles_only,
        "version": version,
    }
    return {"deconstruction_planner": dp}


def upgrade_planner(mapper, label="", version=VERSION_2_0):
    """upgrade_planner: mapper = [{index, from:{name,type,quality?}, to:{name,type,quality}}]."""
    up = {
        "item": "upgrade-planner",
        "label": label,
        "settings": {"mapper": mapper},
        "version": version,
    }
    return {"upgrade_planner": up}


def number_parameter(name, number_name="parameter-0", minimum=0, maximum=2**32 - 1,
                     default=1):
    """number-parameter (параметризация 2.0)."""
    return {
        "type": "number",
        "name": number_name,
        "label": name,
        "minimum": minimum,
        "maximum": maximum,
        "default": default,
    }


def id_parameter(name, id_name="parameter-0"):
    """id-parameter (параметризация 2.0): заменяет имя сигнала/рецепта/предмета."""
    return {"type": "id", "name": id_name, "id": id_name, "label": name} if False else \
        {"type": "id", "name": name, "id": id_name}


# ------------------------------------------------------------------ валидация
def validate(obj):
    """Базовые проверки структуры (не заменяют официальные схемы!)."""
    errs = []
    if isinstance(obj, dict) and ("blueprint" in obj or "blueprint_book" in obj):
        bp = obj.get("blueprint") or obj.get("blueprint_book")
        ents = bp.get("entities") or []
        seen = set()
        for e in ents:
            n = e.get("entity_number")
            if n in seen:
                errs.append(f"дубликат entity_number {n}")
            seen.add(n)
            if "name" not in e or "position" not in e:
                errs.append(f"entity {n}: нет name/position")
        wires = bp.get("wires") or []
        for w in wires:
            if len(w) != 4:
                errs.append(f"wire неправильного формата: {w}")
            for en in (w[0], w[2]):
                if en not in seen:
                    errs.append(f"wire ссылается на несуществующую сущность {en}")
        if not bp.get("version"):
            errs.append("нет version")
    else:
        errs.append("не объект blueprint/blueprint_book")
    return errs


# ------------------------------------------------------------------ CLI
def _cli():
    import argparse
    import sys
    ap = argparse.ArgumentParser(description="Factorio 2.0 blueprint codec")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("decode", help="строка чертежа -> JSON")
    p.add_argument("string", help="строка (или файл .json для JSON)")

    p = sub.add_parser("encode", help="JSON -> строка чертежа")
    p.add_argument("json", help="JSON-файл")
    p.add_argument("--pretty", action="store_true",
                   help="выдать JSON (без сжатия) вместо строки 0+base64")

    args = ap.parse_args()
    if args.cmd == "decode":
        data = open(args.string).read() if args.string.endswith((".json", ".txt")) \
            else args.string
        obj = decode(data)
        print(json.dumps(obj, ensure_ascii=False, indent=2))
    else:
        obj = json.load(open(args.json, encoding="utf-8"))
        print(encode(obj, pretty=args.pretty))


if __name__ == "__main__":
    _cli()
