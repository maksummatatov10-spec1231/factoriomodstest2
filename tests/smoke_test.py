#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Смоук-тест мода fish-furnace в настоящем Lua-интерпретаторе (LuaJIT через lupa).
Эмулирует минимальную среду data-stage Factorio:
  - data.raw / data:extend()
  - util.by_pixel()
  - circuit_connector_definitions
Затем проверяет прототипы, пути к графике, локализацию, info.json.
"""
import json
import os
import re
import sys
from lupa import LuaRuntime

MOD = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "mods", "fish-furnace"))
ROOT = os.path.abspath(os.path.join(MOD, "..", ".."))

errors = []

# ---------- Lua runtime & environment ----------
lua = LuaRuntime(unpack_returned_tuples=True)

# собираем таблицу data.raw как обычную Lua-таблицу с методами
lua.execute("""
raw = {}
raw_extend = function(self, list)
  for _, p in ipairs(list) do
    local t, n = p.type, p.name
    if not t or not n then error('prototype without type/name') end
    raw[t] = raw[t] or {}
    raw[t][n] = p
  end
end
data = { raw = raw, extend = raw_extend }
util = { by_pixel = function(x, y) return { x = x/32, y = y/32 } end }
settings = { startup = {}, global = {} }
circuit_connector_definitions = { ["stone-furnace"] = { type = "dummy" } }
package = package or {}
package.preload = package.preload or {}
package.preload["util"] = function() return util end
""")

# конвертер Lua-таблиц в Python (прототипы ацикличны)
_LuaTable = type(lua.eval("{}"))
def py_convert(v):
    if isinstance(v, _LuaTable):
        pairs = []
        for k, val in v.items():
            pairs.append((py_convert(k), py_convert(val)))
        keys = [k for k, _ in pairs]
        keys_num = [k for k in keys if isinstance(k, int)]
        if keys_num and sorted(keys_num) == list(range(1, len(keys_num) + 1)) and len(keys_num) == len(pairs):
            return [val for _, val in sorted(pairs, key=lambda kv: kv[0])]
        return dict(pairs)
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return v

# ---------- выполнение файлов data-этапа ----------
for f in ["prototypes/entity.lua", "prototypes/item.lua",
          "prototypes/recipe.lua", "prototypes/technology.lua"]:
    path = os.path.join(MOD, f)
    code = open(path, encoding="utf-8").read()
    # require("prototypes.X") внутри файлов у нас нет (data.lua требует, но мы
    # запускаем по одному; суффикс не нужен — все файлы используют глобал data)
    try:
        lua.execute(code)
        print("  ok:", f)
    except Exception as e:
        msg = str(e)
        # убираем шум lupa
        print("  FAIL:", f, msg[:300])
        errors.append(f"{f}: {msg}")

# ---------- проверка прототипов ----------
def to_py(t):
    return lua.eval(t)

_raw_lua = lua.eval("raw")
raw_all = {}
for t in _raw_lua:
    tt = _raw_lua[t]
    raw_all[t] = {}
    for n in tt:
        raw_all[t][n] = py_convert(tt[n])

def get(t, n):
    tbl = lua.eval("raw")
    tt = tbl[t]
    if tt is None: return None
    return py_convert(tt[n])

for t, n in [("furnace", "fish-furnace"), ("item", "fish-furnace"),
             ("recipe", "fish-furnace"), ("technology", "fish-furnace"),
             ("corpse", "fish-furnace-remnants")]:
    v = get(t, n)
    if not v:
        errors.append(f"нет прототипа {t}:{n}")
    else:
        print(f"  есть {t}:{n}")

ent = get("furnace", "fish-furnace")
it = get("item", "fish-furnace")
rec = get("recipe", "fish-furnace")
tech = get("technology", "fish-furnace")

# Допустимые типы TriggerEffectItem (из официальной документации 2.0.76:
# lua-api.factorio.com/2.0.76/types/TriggerEffectItem.html). Типа "direct" НЕТ!
VALID_TRIGGER_TYPES = {
    "activate-impact", "camera-effect", "create-asteroid-chunk", "create-decoratives",
    "create-entity", "create-explosion", "create-fire", "create-smoke", "create-particle",
    "create-sticker", "create-trivial-smoke", "create-pollution", "damage-entity",
    "damage-tile", "destroy-cliffs", "destroy-decoratives", "footstep", "insert-item",
    "invoke-tile-effect", "nested", "play-sound", "push-back", "script", "set-tile",
    "show-explosion-on-chart"
}

if ent:
    if ent.get("crafting_speed") != 4: errors.append("crafting_speed != 4")
    if ent.get("energy_usage") != "360kW": errors.append("energy_usage != 360kW")
    if ent.get("corpse") != "fish-furnace-remnants": errors.append("corpse mismatch")
    if (ent.get("minable") or {}).get("result") != "fish-furnace": errors.append("minable.result")
    # КРИТИЧЕСКАЯ проверка: damaged_trigger_effect должен быть валидным TriggerEffectItem
    dte = ent.get("damaged_trigger_effect")
    if not dte:
        errors.append("damaged_trigger_effect отсутствует")
    else:
        if dte.get("type") not in VALID_TRIGGER_TYPES:
            errors.append(f"damaged_trigger_effect.type = {dte.get('type')!r} — невалидный TriggerEffectItem!")
    # звуки: в ваниле нет файла manual-repair.ogg — проверяем пути
    for snd_name in ("repair_sound", "mined_sound", "open_sound", "close_sound"):
        snd = ent.get(snd_name)
        if snd is None: continue
        def sound_files(x):
            out = []
            if isinstance(x, dict):
                if "filename" in x: out.append(x["filename"])
                for v in x.values():
                    if isinstance(v, (dict, list)): out += sound_files(v)
            elif isinstance(x, list):
                for v in x: out += sound_files(v)
            return out
        for path in sound_files(snd):
            # несуществующий файл = ошибка загрузки звука
            if "manual-repair.ogg" in path:
                errors.append(f"{snd_name} ссылается на несуществующий manual-repair.ogg!")
    gs = ent.get("graphics_set") or {}
    anim = gs.get("animation") or {}
    layers = anim.get("layers") or []
    if len(layers) != 2: errors.append("graphics_set.animation.layers != 2")
    # КРИТИЧЕСКИ: движок требует одинаковое итоговое число кадров во всех слоях
    # animation.layers (frame_count * repeat_count). Разное -> "Different frame counts".
    def total_frames(layer):
        return (layer.get("frame_count") or 1) * (layer.get("repeat_count") or 1)
    counts = [total_frames(l) for l in layers]
    if len(set(counts)) != 1:
        errors.append(f"разное число кадров в animation.layers: {counts} — нужен одинаковый frame_count*repeat_count!")
    wv = gs.get("working_visualisations") or []
    # а то же правило для каждой working visualisation
    for wi, w in enumerate(wv):
        wa = w.get("animation") or {}
        wlayers = wa.get("layers")
        if isinstance(wlayers, list) and wlayers:
            wc = [total_frames(l) for l in wlayers]
            if len(set(wc)) != 1:
                errors.append(f"working_visualisations[{wi}]: разное число кадров в слоях: {wc}")
    wv = gs.get("working_visualisations") or []
    if len(wv) != 2: errors.append("working_visualisations != 2")
    energy = ent.get("energy_source") or {}
    if energy.get("type") != "burner": errors.append("energy_source.type != burner")
    if energy.get("fuel_categories") != ["chemical"]:
        errors.append("fuel_categories != chemical")
if it:
    if it.get("place_result") != "fish-furnace": errors.append("place_result")
if rec:
    ing = rec.get("ingredients")
    if not (isinstance(ing, list) and len(ing) == 1 and
            ing[0].get("name") == "raw-fish" and ing[0].get("amount") == 50):
        errors.append("рецепт не 50 raw-fish")
if tech:
    fx = tech.get("effects") or []
    if not (isinstance(fx, list) and fx and fx[0].get("recipe") == "fish-furnace"):
        errors.append("tech effects")
    unit = tech.get("unit") or {}
    ings = unit.get("ingredients")
    if not (isinstance(ings, list) and ings and "automation-science-pack" in str(ings[0])):
        errors.append("tech unit ingredients")
    if unit.get("count") != 1: errors.append("tech count != 1")

# ---------- пути к ассетам ----------
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "filename" and isinstance(v, str):
                m = re.match(r"^__([\w-]+)__/(.+)$", v)
                if not m:
                    errors.append(f"путь без __mod__: {v}")
                    continue
                mod, rel = m.groups()
                if mod != "fish-furnace":
                    continue  # официальные ассеты в репозитории не хранятся
                p = os.path.join(MOD, rel)
                if not os.path.exists(p):
                    errors.append(f"нет файла: {v}")
            else:
                walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)

for t in ("furnace", "corpse", "item"):
    for n, p in (raw_all.get(t) or {}).items():
        walk(p)

# ---------- локализация ----------
for lang in ("en", "ru"):
    cfg = os.path.join(MOD, "locale", lang, "base.cfg")
    if not os.path.exists(cfg):
        errors.append(f"нет локали {lang}")
        continue
    txt = open(cfg, encoding="utf-8").read()
    for key in ("item-name", "item-description", "entity-name", "entity-description",
                "recipe-name", "technology-name", "technology-description"):
        if f"[{key}]" not in txt:
            errors.append(f"locale {lang}: нет [{key}]")
    if "fish-furnace=" not in txt:
        errors.append(f"locale {lang}: нет fish-furnace=")

# ---------- info.json ----------
info = json.load(open(os.path.join(MOD, "info.json")))
if info["name"] != "fish-furnace": errors.append("info.name")
if info["version"] != "1.0.1": errors.append("info.version")
if info.get("factorio_version") != "2.0": errors.append("info.factorio_version")
if "base >= 2.0.0" not in info.get("dependencies", []): errors.append("dependencies")

# ---------- итог ----------
print()
if errors:
    print("ОШИБКИ (%d):" % len(errors))
    for e in errors: print("  -", e)
    sys.exit(1)
print("SMOKE TEST (LuaJIT): ВСЁ OK")
