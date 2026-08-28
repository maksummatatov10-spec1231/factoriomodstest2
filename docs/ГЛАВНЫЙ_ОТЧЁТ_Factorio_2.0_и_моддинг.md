# Factorio 2.0 → 2.0.76: абсолютно полный обзор + всё для моддинга, графики и 3D-пайплайна

> **Отчёт подготовлен:** 28.08.2026
> **Статус версий на сегодня:** Стабильная ветка — **2.0.77**; Экспериментальная — **2.1.17** (ветка 2.1, FFF-444).
> **Источники:** официальные (factorio.com, forums.factorio.com, wiki.factorio.com, lua-api.factorio.com, github.com/wube/factorio-data, Steam News, Mod Portal, блог Wube/Friday Facts) + неофициальные (Reddit r/factorio, GitHub-гайды коммьюнити, patched.gg / patchtracker.gg, NamuWiki, The Foundry, Discord).
> Всё, что ниже, проверено по первоисточникам; полные дословные ченджлоги лежат рядом: `docs/changelogs/`.

---

## 0. TL;DR (самое главное)

1. **Factorio 2.0** — бесплатное обновление базовой игры, вышло **21 октября 2024** одновременно с платным дополнением **Factorio: Space Age** ($35). Ветка 2.0.x прожила ~1.5 года: **77 сборок** (2.0.0 → 2.0.76), из них **70 публичных** (2.0.7 → 2.0.76, первая публичная — 2.0.7 от 20–21.10.2024, последняя в запрошенном диапазоне — 2.0.76 от 25.02.2026, стала стабильной 19.03.2026).
2. **2.0.7 — это и есть «релиз 2.0»**: версии 2.0.0–2.0.6 были закрытыми сборками для тестеров (публичных ченджлогов нет). Практически весь новый контент и весь новый API вошли именно в 2.0.7; дальше шли в основном багфиксы, оптимизации и точечные добавки в API (вплоть до 2.0.77).
3. **2.0 включает 4 «официальных мода» в составе игры**: `base`, `quality`, `elevated-rails`, `space-age` (а с ветки 2.1 ещё отдельный `recycler`). Это значит: моды строятся на тех же механизмах, что и сами официальные моды, и всё их исходники лежат в открытом репозитории **wube/factorio-data** — лучший учебник для моддера.
4. **Ключевые новинки 2.0:** система Качества (Quality) с 5 уровнями, новые/повышенные рельсы + эстакадные рельсы, Space Age (4 новые планеты: Vulcanus, Fulgora, Gleba, Aquilo + Shattered Planet; космические платформы, ракеты, астероиды, спутники и орбитальная логистика), новая система жидкостей, «смышлёные» роботы, удалённый вид (remote view), переработанные комбинаторы и цепь, прерывания расписаний поездов, Factoriopedia, новые враги (demolisher, пентаподы), генерация террейна с нуля и многое другое.
5. **Важно для моддинга:** язык — **Lua** (Lua 5.1-подобный, с загрузкой `mods` в 2 этапа: data + control). В 2.0 произошёл большой «рефакторинг» API: `global` → **`storage`**, добавлены глобалы `prototypes` и `helpers`, `defines.direction` стал **16 направлений** (было 8), цепь перешла на `wire_connector_id`, статистика/объекты переименованы и т.д. Готовый гайд по портированию 1.1 → 2.0: **github.com/tburrows13/factorio-2.0-mod-porting-guide**.
6. **Про 3D и анимации:** движок Factorio **не поддерживает 3D-модели в рантайме** — всё, что в игре, это **2D PNG-спрайты (спрайт-шиты) и анимации из кадров**. 3D используется **только офлайн**: Wube моделирует объекты в Blender и рендерит из них спрайты под все направления/кадры. Так же поступают и моддеры. Об этом — большой раздел ниже (инструменты Spritify, blender-factorio-utils, factorio-spritter и т.д.).
7. **Что дальше:** 2.0.77 — стабильная ветка (с 23.06.2026), параллельно с 26.06.2026 идёт **ветка 2.1** (экспериментал, сейчас 2.1.17): новая графика/аудио-системы, SDL3, новые требования к ОС, и уже новые фичи (рециклер как отдельный мод, правки качества/платформ и т.д.). Сейвы 2.0 совместимы с 2.1 в одну сторону (обратно — нет).

*Полная машиночитаемая версия всех официальных ченджлогов сгенерирована в `docs/changelogs/полный-официальный-ченджлог-2.0.7-2.0.76.md` (дословно), а все изменения API для моддеров отдельно — в `docs/changelogs/modding-scripting-API-изменения-2.0.md`.*

---

## 1. Что такое Factorio 2.0 и из чего он состоит

### 1.1 Состав релиза

| Компонент | Что это | Статус |
|---|---|---|
| **base 2.0** | бесплатное обновление ядра: живость, QoL, жидкость, рельсы, роботы, цепь, GUI | бесплатно всем |
| **quality** | официальный «мод»: система качества (Common → Uncommon → Rare → Epic → Legendary) | требует Space Age (в 2.0; с 2.1 — опциональная зависимость) |
| **elevated-rails** | официальный «мод»: эстакадные рельсы (рампы, опоры, 2 яруса) | часть SA, но может включаться отдельно |
| **space-age** | официальный «мод» DLC: планеты, платформы, астероиды, новые враги и ресурсы, орбитальная логистика | платный DLC |
| **recycler** | официальный «мод»: рециклер (выделен из space-age только в ветке 2.1.7+) | см. 2.1 |

Формат зависимостей официальных модов наглядно показывает, как писать зависимости в 2.0 (это реальные `info.json` из wube/factorio-data):

```json
// space-age/info.json (2.1.17)
{
  "name": "space-age",
  "version": "2.1.17",
  "dependencies": [
    "base >= 2.1.0",
    "elevated-rails >= 2.1.0",
    "+ quality >= 2.1.0",
    "recycler >= 2.1.0"
  ]
}
```

Синтаксис зависимостей: `"modname"` — обязательная; `"?"`/`"(?)"` — мягкая (опциональная, `?` = не блокирует, но загрузится до тебя, если есть; `(?)` = вообще без гарантий порядка), `"!"` — запрет, `">=", "<", ">"` — версии, `"+"` — жёсткая рекомендация (hard recommendation), `"~"`/`"!"` обратные зависимости. Для модифика без DLC обычно: `"dependencies": ["base >= 2.0.0"]`.

### 1.2 Даты и вехи ветки

| Дата | Событие |
|---|---|
| 07.05.2024 | FFF-418: анонс даты релиза 21.10.2024, цена $35 |
| сентябрь–октябрь 2024 | FFF-374…417: анонсы всех систем 2.0 (роботы, рельсы, quality, remote view, жидкость, комбинаторы, поезда, планеты и т.д.) |
| 14.10.2024 | снят NDA: тестеры/стримеры начали показывать контент; сборки 2.0.0–2.0.6 (закрытые) |
| **21.10.2024** | **публичный релиз: 2.0.7 + Space Age** (чанжлог датирован 20.10.2024) |
| 21–31.10.2024 | горячие фиксы: 2.0.8, 2.0.9, 2.0.10, 2.0.11, 2.0.12, 2.0.13 |
| ноябрь 2024 | 2.0.14–2.0.19 (баланс SA, QoL, стабильность) |
| декабрь 2024 | 2.0.20–2.0.28 (в т.ч. sandbox-сценарий, реконнект к модулям, оптимизации) |
| январь–февраль 2025 | 2.0.29–2.0.37 (графика, оптимизации, API-добавки) |
| март–май 2025 | 2.0.38–2.0.51 (атласы 4096, decals, quality-хуки, новые прототипы, новый контент-баланс) |
| июнь–сентябрь 2025 | 2.0.52–2.0.68 (метал-рендер на macOS, splitter в цепь, скриптовые триггеры технологий, UDP-события, исправления) |
| октябрь 2025 | 2.0.69–2.0.72 (стабильные релизы; комбинаторы — primary consumers) |
| январь–февраль 2026 | 2.0.73–2.0.75 (стабильность, вагонные/поездные фиксы) |
| **25.02.2026** | **2.0.76** (последняя версия запрошенного диапазона) |
| 19.03.2026 | 2.0.76 переведена в **stable** |
| 21.05.2026 | 2.0.77 (API: quality-мультипликаторы, `drops_full_belt_stacks`, полнотекстовый поиск в API-доках) |
| 23.06.2026 | 2.0.77 → **stable** |
| 26.06.2026 | **релиз ветки 2.1 Experimental** (FFF-444: новая графика/аудио, SDL3, OS-требования; сейвы 2.0 совместимы, даунгрейд невозможен) |
| 26.08.2026 | последняя сборка на сегодня: **2.1.17** (экспериментальная) |

### 1.3 Версии 2.0.0–2.0.6 (важно честно проговорить)

Это **закрытые тестовые сборки** (рассылались стримерам/тестерам до 14.10.2024). Публичных ченджлогов к ним нет; официальная вики начинает историю 2.0 с **2.0.7**. Поэтому «абсолютно всё» по 2.0.0–2.0.6 = «всё, что есть публично» (первая публичная версия — 2.0.7 со всеми фичами). В `wube/factorio-data` (теги на каждую версию) есть тэги и для 2.0.0? — публичные релизы начинаются с 2.0.7; сравнивать прототипы можно тегами `2.0.7`…`2.0.76`.

---

## 2. Большие темы обновления 2.0 (по системам)

### 2.1 Space Age — новый слой игры

- **Планеты:** Vulcanus (металлургия, вулканы, демолишеры), Fulgora (молнии, хлам, Хольмиум), Gleba (биология, спойлинг, пентаподы, захватные роботы), Aquilo (криогеника, лёд, тепло) + **Shattered Planet** (финал, прометий).
- **Космические платформы:** хаб-модуль, сборка на орбите из «стартового набора», движение между планетами с топливными/процессионными (procession) настройками, требования к платформе (основание, карго-отсеки), автосборка с запросами материалов, фильтры астероидных коллекторов.
- **Ракеты:** пуск с планеты на платформу и обратно, карго-поды, «Отправить на орбиту автоматически» (rocket silo + circuit + orbital requests), весовая/объёмная логистика, `rocket-launch-products`, переменные результаты (2.0.74–2.0.76 фиксы именно в этой логике).
- **Астероиды:** типы (металлические/углеродные/ледяные/прометиевые), коллекторы, дробилки, топливо (углерод), спавн-определения по маршруту (`asteroid-spawn-definitions`), влияние планет.
- **Новые типы машин:** thruster, asteroid-collector, cargo-landing-pad, space-platform-hub, fusion-reactor/fusion-generator, heating-tower, agricultural-tower, capture-robot, recycler (в 2.0 — внутри SA), bio-chamber, electrolyzer, lava-*, cryo-*, em-plant, foundry, big-mining-drill, mech armor и т.д.
- **Новые жидкости:** molten iron/copper, sulfuric acid на Vulcanus, холмиум, биофлюкс, лёд, гелий-«акуило», охлаждение, `fluid` с температурами.
- **Новые враги:** Demolisher (Vulcanus), Pentapods (Gleba: stomper, wriggler, strafer; территории, «roof»-механика), а также спойлинг-механика (битер-яйцо — 2.0.9/2.0.17 и др.).

### 2.2 Quality (качество)

- Пятиуровневая система: **Common → Uncommon → Rare → Epic → Legendary** (цвета зелёный/синий/фиолетовый/оранжевый/красный, прототип `quality` с `level`, `color`, `order`, `next`, `next_probability`, `chain_probability` (с 2.1), `subgroup`, `icon`).
- Работает для **предметов, сущностей, оборудования, модулей и боеприпасов**: скорость крафта, энергия, ёмкости, урон, радиус, зарядка роботов, прочность инструментов и т.д. — через мультипликаторы прототипа: `crafting_speed_quality_multiplier`, `energy_usage_quality_multiplier`, `module_slots_quality_bonus`, `quality_affects_supply_area_distance`, `quality_affects_inventory_size`, `quality_affects_capacity`, `quality_affects_energy_usage`, `uses_quality_drain_modifier`, `drops_full_belt_stacks` и др. (API-чтения добавлены как раз в 2.0.77).
- Качественные модули, качественное лутание (лут-таблица с качествами), рецепты в качествах, `LuaInventory::get_contents()` возвращает `{name, count, quality}`, `LuaEntity::quality`, параметры качества везде в API (`quality` в `create_entity`, `set_recipe` и т.д.).
- **Для моддеров:** любой новый прототип может поддерживать качество автоматически (если указаны соответствующие флаги/умножители), качество предмета = суффикс-прототип (`item-name` автоматически), `quality` для инвентаря/стака.

### 2.3 Рельсы и эстакады

- **Полностью новый рельсовый код**: произвольные формы рельсов, плавные повороты, **22.5° диагонали** (2.0.7), новые «переходные» тайлы.
- **Elevated rails:** рампы (16×4, 4 направления), опоры (4×4, 8 направлений), верхний ярус трасс, сигналы на эстакадах, визуальные ограждения; спавн поверх воды (опоры), пересечения ярусов; поезда на разных ярусах.
- **Rail planner:** привязка к ближайшим рельсам, снэп между ярусами, «умное» соединение, планирование на карте/в remote view (FFF-403).
- Curve/диагональные сегменты стоят 3 рельса (2.0.13); ghost-поезда, rolling stock connections в чертежах (фиксы 2.0.66/2.0.73/2.0.74 — «ghost trains», «rolling stock ghost connections»).
- **API:** `LuaTrainManager` (все поезда/станции мира), `LuaRailEnd`, `LuaEntity::get_rail_end`, `rail_layer` (ярус), `mirroring`, `LuaEntityPrototype::reversing_power_modifier` (2.0.76), `get_item_insert_specification`, `LuaEntity::get_item_insert_specification` и др.

### 2.4 Жидкости (новая система)

- Новая физика «сегментов жидкости» (fluid segments) вместо старых «fluid systems»: давление/поток по трубам, подземные трубы (underground pipes), смешивание с предпочтением большего объёма (2.0.16), фильтрация, горячие/холодные жидкости, тепло (`heat` interface расширен в 2.0.64 — греть сущности и тайлы).
- Цистерны: 25 000 → **50 000** (баланс 2.0.7); `fluid_wagon_tank_valve_max_distance` и графика подключения (в 2.1 заменены поля).
- **API:** `LuaFluidBox::get_fluid_segment_id`, `get_fluid_segment_contents`, `get_fluid_segment_extent_bounding_box()` (2.0.67), `add_linked_connection/get_linked_connection/...`, `LuaEntity::fluids_count`, `get_fluid/set_fluid`, `LuaFluidPrototype::visualization_color` (2.0.77), водонасосы-качество, карта трубопроводов-оверлей.

### 2.5 Роботы

- «Smarter worker robots» (FFF-374): лучшее планирование задач, связность робопортов, отсутствие «залипаний», очередь зарядки.
- **Запросы робопортов** (roboport requests) — робопорт даёт составные запросы; штраф «конструкторная» логистика.
- Новый цвет в обзоре роботов на карте (красный = роботы летят ко мне — 2.0.7).
- **API:** `LuaLogisticPoint`, `LuaLogisticSection` (унифицированные секции запросов вместо кучи методов), `LuaEntity::get_logistic_sections()` (2.0.16), `logistic_cell_charging_energy_multiplier`, `RobotWithLogisticInterfacePrototype::max_payload_size_after_bonus` (2.0.67), `LuaItemCommon::entity_logistics_enabled` и др. (2.0.69).

### 2.6 Комбинаторы и цепь

- **Selector combinator** (новый, 2.0.7), улучшения decider/arithmetic; с 2.0.72 они **primary energy consumers** с увеличенным буфером (переживают просадки сети), selector 5кВт→1кВт.
- **Вся цепь переведена на `wire_connector_id`** вместо `circuit_connector_id` (API-ломка для старых модов!): `defines.wire_connector_id`, `LuaEntity::get_wire_connector(s)`, `LuaWireConnector`, `LuaCircuitNetwork::wire_connector_id`, сигнатуры `get_circuit_network(wire_connector_id)`.
- К цепи подключены: **турели** (чтение боезапаса/отключение; FFF-410), **ракетная шахта** (чтение содержимого + орбитальные запросы), **сборочные машины** (список ингредиентов рецепта), **сплиттеры** (2.0.67), программируемый динамик с параметризацией чертежа (2.0.11), лампы/двери и т.д.
- `LuaControlBehavior` теперь принимает условие напрямую (без таблицы `condition`), удалён `LuaConstantCombinatorControlBehavior::parameters/…`, `defines.circuit_connector_id` удалён.
- Приоритеты целей турелей (enemy priority), `LuaEntity::priority_targets` (2.0.64), get/set_priority_target.

### 2.7 Поезда

- **Train interrupts** (FFF-389/395), условия ожидания: топливо, «станция заполнена/свободна», время, жидкость (округление вверх <1.0 — фикс 2.0.6x), прерывания по сигналам.
- Автоцвет локомотива от цвета станции, приоритеты станций (`train_stop_priority`, 2.0.7 API), временные станции.
- Жел-вид карты, «trains map view», предпросмотр путей, `LuaEntity::copy_color_from_train_stop`, `train_stop_priority`, расписания с fuel condition.
- Rolling stock (вагоны/etc): соединения в чертежах, ghost-поезда, фиксы 2.0.66/2.0.73–2.0.75 (order ghosts, auto mode после топлива и т.д.).

### 2.8 Remote view, управление и UX

- **Remote view** (FFF-380): удалённое строй-во/управление сущностями/поездами/платформами, пиннинг и отслеживание (pins, FFF-400), конфигурация через открытие интерфейсов, new controller type `remote`, `LuaPlayer::physical_surface/vehicle/position`, `LuaPlayer::centered_on`, `set_controller`.
- Контroller input method (геймпад) — новый «controller input method» с автоснапом машин к 8 направлениям (2.0.46), Space Map free cursor фиксы.
- **Factoriopedia** — энциклопедия всего (с симуляциями; прототипы `factoriopedia-simulations`, ключи `factoriopedia` в локали; поле `custom_tooltip_fields` с 2.0.59).
- Blueprint library: `LuaRecord`, `LuaPlayer::blueprints`, `LuaGameScript::blueprints`, previews, иконки; upgrade planner: динамический размер, установка модулей, фильтры машин/максимум модулей, paste behaviour; «flipping» сущностей; ghost поверх воды с landfill-ghost; smart drag подземных труб и лент; модуль/топливо-запросы удалённо (FFF-380).

### 2.9 Графика, звук, техника (что менялось по патчам)

- **2.0.38:** минимальный размер атласа спрайтов поднят до **4096** (даже на «среднем» качестве) — моддерам важно для VRAM-бюджета.
- **2.0.44:** decals (декали) теперь **маскируются водой** при слое выше `capture_water_mask_at_layer`, `lightmap_alpha < 1`, `opacity_over_water < 1` (нужен Space Age; не работает на Switch).
- **2.0.68:** на macOS по умолчанию графический бэкенд **Metal**, OpenGL — deprecated; настройка «Graphics backend» удалена.
- **2.0.61:** «Render in native screen resolution» без перезапуска; Metal-фиксы.
- **2.0.16:** SDL 2.30.9; **2.0.66:** подпись Windows-исполняемых файлов; **2.1:** SDL3, macOS 26 иконка, min macOS 10.13, переработка графики/аудио (FFF-444).
- **Звук (2.0.7):** `Sound::advanced_volume_control` (затухание, фейды по зуму, порог темноты), `Sound::priority`, `Sound::speed_smoothing_window_size`, `SoundDefinition::min_volume/max_volume`, dynamic volume modifiers, non-linear attenuation, activity matching; **2.0.59** — новые SoundPath-типы `item-open/close/pick/drop/move`.
- **Производительность:** `entity_renderer_search_box_limits` унифицированы до 6, `light_renderer_search_distance_limit` до 20 (2.0.38), «unassuming» оптимизации роботов, «latency hiding» для машин/спидэртронов, неблокирующее сохранение, `LuaGameScript::allow_debug_settings` (2.0.66) и т.д.

### 2.10 Контент-баланс (выборочно, самые заметные)

- fluid wagon 25k→50k; LDS стак 10→50; beacon стак 10→20 (2.0.7); rocket part в 10 раз дешевле; кривые рельсы 3 шт.; offshore pump скорость от качества (2.0.13); stack inserter = новая сущность (старый stack inserter переименован в **bulk inserter**, миграция `base/migrations/1.2.0 stack inserter rename.json`); спидэртрон-громкость; quality-селектор кнопками (2.0.17); пенкэйдже баланс, `Territory` для пентаподов; бойлеры — консервация энергии с учётом теплоёмкости (2.0.7); топливо/катализаторы; «всё, что связано с битер-яйцом» и т.д.

---

## 3. Полная хронология 2.0.7 → 2.0.76

Полные дословные ченджлоги — в `docs/changelogs/полный-официальный-ченджлог-2.0.7-2.0.76.md`. Ниже — сводная таблица каждой публичной версии (дата / разделы / главное для игры и моддинга):

| Версия | Дата (офиц. ченджлог) | Разделы | Ключевое |
|---|---|---|---|
| **2.0.7** | 20. 10. 2024 | Major Features, Features, Ease of use, Circuit Network, Minor Features, Optimizations, Graphics, Sounds, Balancing, Changes, Gui, Modding, Scripting, Bugfixes | Features: Rail planner is usable in the map (remote view). (https://factorio.com/blog/post/fff-403); Features: Added smart dragging of underground belts and pipes. … |
| **2.0.8** | 21. 10. 2024 | Bugfixes | только багфиксы |
| **2.0.9** | 22. 10. 2024 | Changes, Bugfixes | Changes: Achievement logistic-network-embargo updated with different condition for base game and space age. |
| **2.0.10** | 23. 10. 2024 | Features, Changes, Bugfixes | Features: [space-age] Galaxy of fame. Offered when the game is finished. (https://www.factorio.com/galaxy); Features: Added flying text for more cases of unsuccessful resource mining.; Changes: Non-blocking saving setting is no longer synced over the Steam cloud. |
| **2.0.11** | 25. 10. 2024 | Features, Changes, Optimizations, Bugfixes, Modding, Scripting | Features: [space-age] Asteroid collector filters can be modified by blueprint parametrisation.; Features: Programmable speaker can be modified by blueprint parametrisation. … |
| **2.0.12** | 28. 10. 2024 | Bugfixes, Modding | Modding: Added LoaderPrototype::frozen_patch_in and frozen_patch_out. |
| **2.0.13** | 30. 10. 2024 | Minor Features, Changes, Bugfixes, Scripting, Sounds | Minor Features: [space-age] Offshore pump speed increases with quality.; Changes: Curved rails cost 3 rail items to build. … |
| **2.0.14** | 01. 11. 2024 | Changes, Bugfixes, Modding, Scripting | Changes: [space-age] Changed self-recycling recipe statistics to be ignored in production graph.; Changes: Changed sprites with scale between 0.5 and 1 (exclusive) to apply downscaling to low resolution (affects base game biter sprites). … |
| **2.0.15** | 05. 11. 2024 | Minor Features, Changes, Bugfixes, Modding, Scripting | Minor Features: Cars and tanks will auto-refuel. ; Minor Features: Relation between offshore pump and fluid tiles added to Factoriopedia. … |
| **2.0.16** | 08. 11. 2024 | Minor Features, Changes, Bugfixes, Scripting | Minor Features: Search is now case and accent insensitive for all official languages.; Changes: [space-age] Changed tree seed default import location to Nauvis.  … |
| **2.0.17** | 12. 11. 2024 | Changes, Bugfixes, Modding, Scripting | Changes: [space-age] Gleba evolution is smoother and more gradual.; Changes: [space-age] Small stomper pentapod moves more slowly (also decreases stomp DPS). … |
| **2.0.18** | 14. 11. 2024 | Changes, Bugfixes, Modding, Scripting | Changes: Allowed negative multiplier of logistic (and constant combinator) groups. ; Changes: Updated shortcut icons and increased their size to 56px. … |
| **2.0.19** | 15. 11. 2024 | Minor Features, Changes, Bugfixes | Minor Features: Added debug option 'always-show-lightning-protection'.; Changes: [space-age] Changed captive biter spawner to inherit quality from the wild spawner instead of the capture robot. ; Changes: Spidertron selections saved into the quickbar will be darkened with a planet icon in the top when the selection leads to a different planet than the current one. |
| **2.0.20** | 18. 11. 2024 | Minor Features, Bugfixes | Minor Features: Added gamepad stick sensitivity setting for map movement.; Minor Features: Selecting a spidertron remote selection in the quickbar which is for a different planet than the current one will center on the planet. |
| **2.0.21** | 21. 11. 2024 | Minor Features, Changes, Bugfixes, Modding, Scripting | Minor Features: Added drag-to-reorder to the research queue.; Minor Features: Added "Occlude light sprites" graphics option to allow disabling 2.0 light rendering to improve performance. As a side effect, it disables also lava glow.  … |
| **2.0.22** | 26. 11. 2024 | Minor Features, Changes, Bugfixes, Modding, Scripting | Minor Features: Assemblers circuit allows to choose if items in crafting should be included by read contents.; Minor Features: Asteroid collector circuit allow to choose if items held by hands should be included by read contents. … |
| **2.0.23** | 28. 11. 2024 | Changes, Optimizations, Bugfixes | Changes: Added an error message when manually trying to launch a rocket to a full space platform.; Changes: Changed space platforms to not delete items on the ground when deconstructing them. ; Changes: Added back a simple version of the Sandbox scenario. Improved the behavior of god controller. |
| **2.0.24** | 05. 12. 2024 | Minor Features, Graphics, Balancing, Changes, Bugfixes, Modding, Scripting | Minor Features: [space-age] Added "Nauvis Bus" and "Nauvis Power Up" menu simulations.; Minor Features: [space-age] Added camera views to Space platform tooltips. … |
| **2.0.25** | 12. 12. 2024 | Minor Features, Changes, Graphics, Bugfixes, Modding, Scripting | Minor Features: Dragging and dropping a blueprint file into the game window will import the file contents as a blueprint string.; Minor Features: Dragging and dropping text into the game window on X11 will import the text as a blueprint string. … |
| **2.0.26** | 16. 12. 2024 | Minor Features, Changes, Optimizations, Bugfixes, Scripting | Minor Features: Re-added the sandbox scenario questionnaire.; Changes: Space age mods no longer count as "has mods" in the server browser.  … |
| **2.0.27** | 18. 12. 2024 | Changes, Graphics, Bugfixes, Modding, Scripting | Changes: Wrigglers will no longer proactively attack pollen emitters. However, they will still respond to artillery.; Changes: Attack groups containing stompers or strafers will now contain fewer units. … |
| **2.0.28** | 20. 12. 2024 | Optimizations, Bugfixes | только багфиксы |
| **2.0.29** | 06. 01. 2025 | Minor Features, Graphics, Bugfixes, Scripting, Modding | Minor Features: Added smart pipette for items on the ground.; Scripting: Added LuaRecord::get_active_index. … |
| **2.0.30** | 10. 01. 2025 | Changes, Bugfixes, Scripting | Changes: Changed map generated lightning attractors to always produce full-health items when mined. ; Changes: Reordered results of scrap recycling to make the recycler stack them on belts more efficiently. (https://mods.factorio.com/mod/better-scrap-stacking)  … |
| **2.0.31** | 16. 01. 2025 | Changes, Bugfixes, Scripting | Changes: Disabled achievements "It stinks and they don't like it", "It stinks and they do like it", and "Get off my lawn" in peaceful mode and no enemies mode. ; Changes: Adding more effect info to yumako, mash, jellynut, jelly, bioflux and slowdown capsule tooltips.; Scripting: ItemPrototype::spoil_result and spoil_to_trigger_result can now be used at the same time. |
| **2.0.32** | 20. 01. 2025 | Optimizations, Graphics, Bugfixes, Scripting, Modding | Scripting: Added connection_category to LuaFluidboxPrototype::pipe_connections.; Modding: Added FluidStream::target_initial_position_only. It's used by worm acid spit. |
| **2.0.33** | 28. 01. 2025 | Minor Features, Changes, Graphics, Optimizations, Bugfixes, Modding, Scripting | Minor Features: Show a warning in the blueprint library if it's using a lot of RAM.; Minor Features: Show a warning in blueprint and blueprint book tooltips if they are using a lot of RAM. … |
| **2.0.34** | 06. 02. 2025 | Minor Features, Balancing, Changes, Optimizations, Bugfixes, Scripting | Minor Features: Extended the virtual signals, and unified/changed graphics of some of the existing ones.; Minor Features: Added an ability to pin the selected resource patch directly from map view. … |
| **2.0.35** | 20. 02. 2025 | Minor Features, Changes, Bugfixes, Modding, Scripting | Minor Features: GUIs can now also be navigated with D-pad in controller input method.; Minor Features: Added drag-to-reorder to pins. … |
| **2.0.36** | 26. 02. 2025 | Minor Features, Changes, Graphics, Optimizations, Bugfixes, Modding, Scripting | Minor Features: Added an option to mute sound categories in sound settings. ; Minor Features: Added an option to control the volume of Programmable speaker sounds via circuit network.  … |
| **2.0.37** | 26. 02. 2025 | Bugfixes | только багфиксы |
| **2.0.38** | 04. 03. 2025 | Changes, Bugfixes, Modding, Scripting | Changes: Space platform "request missing materials for construction" will no longer request items for entity ghosts which can't yet be built. ; Changes: Increased minimum sprite atlas size to 4096 even when sprite resolution is set to medium.  … |
| **2.0.39** | 05. 03. 2025 | Changes, Bugfixes | Changes: Added extra info about the evaluation order and dependencies into the blueprint parametrisation UI. |
| **2.0.40** | 12. 03. 2025 | Bugfixes, Modding | Modding: Added ElectricPolePrototype::rewire_neighbours_when_destroying.; Modding: Moved the agricultural tower growth area radius to the prototype as growth_area_radius.  |
| **2.0.41** | 12. 03. 2025 | Bugfixes | только багфиксы |
| **2.0.42** | 19. 03. 2025 | Minor Features, Graphics, Bugfixes, Modding, Scripting | Minor Features: Added additional information to Landing pad, Platform Hub and Cargo bay in factoriopedia. ; Modding: Changed working_visualisations to enforce that the provided array is contiguous. … |
| **2.0.43** | 26. 03. 2025 | Minor Features, Graphics, Balancing, Bugfixes, Modding | Minor Features: Added support for volume and speed activity matching for persistent working sounds.; Minor Features: The swap-players command can now handle basic remote view and players in space platform hubs. … |
| **2.0.44** | 07. 04. 2025 | Minor Features, Changes, Gui, Graphics, Bugfixes, Modding, Scripting | Minor Features: Items manually inserted or removed from space platform dump inventory will always reset drop cooldown to two seconds. This should make manual interactions more responsive and intuitive. ; Minor Features: Added filter support to burner fuel inventories. … |
| **2.0.45** | 14. 04. 2025 | Minor Features, Changes, Graphics, Bugfixes, Modding | Minor Features: Equipment grid GUIs have improved click-and-drag support. In addition to installing equipment, you can now click and drag to pick up, transfer, and fast-replace equipment.; Changes: Improve relative vehicle driving with gamepad in multiplayer, especially when shooting. … |
| **2.0.46** | 29. 04. 2025 | Minor Features, Balancing, Changes, Graphics, Bugfixes, Modding, Scripting | Minor Features: Added Space Age expansion filter to the mod portal explore pane.; Minor Features: Added "planets" and "character" tags to the mod portal explore pane. … |
| **2.0.47** | 29. 04. 2025 | Bugfixes | только багфиксы |
| **2.0.48** | 12. 05. 2025 | Minor Features, Bugfixes, Modding, Scripting | Minor Features: Show existing turrets' radius when holding a turret to be built. ; Minor Features: Smart underground belt building now considers splitter to be an obstacle if there was something connected to the lane already. … |
| **2.0.49** | 12. 05. 2025 | Bugfixes, Modding, Scripting | Modding: Added AgriculturalTowerPrototype::randomize_planting_tile.; Modding: Added RecipePrototype::additional_categories.; Scripting: Added LuaEntity::owned_plants read. |
| **2.0.50** | 16. 05. 2025 | Bugfixes, Balancing, Scripting | Balancing: Fuel acceleration bonus and equipment speed bonuses now apply quarter of compound bonus rate to turning rate of tank-driving cars (e.g. tank); Scripting: Added LuaEntity::set_inventory_size_override/get_inventory_size_override methods with support for container and cargo-wagon. … |
| **2.0.51** | 19. 05. 2025 | Minor Features, Bugfixes, Scripting | Minor Features: Spidertron remote tooltips show a camera view of the selected spiders.; Scripting: Added LuaSurface::spill_inventory. |
| **2.0.52** | 23. 05. 2025 | Minor Features, Bugfixes, Modding, Scripting | Minor Features: Added --run-replay command line option.; Modding: Added ItemPrototype::moved_to_hub_when_building.; Scripting: Added LuaSchedule::get_inside_interrupt()/set_inside_interrupt(). |
| **2.0.53** | 30. 05. 2025 | Bugfixes, Modding, Scripting | Modding: Added utility constants logistic_slots_per_row, crafting_queue_slots_per_row, blueprint_big_slots_per_row, blueprint_small_slots_per_row, and trash_inventory_width.; Modding: Added LandMinePrototype::trigger_interval. … |
| **2.0.54** | 30. 05. 2025 | Bugfixes | только багфиксы |
| **2.0.55** | 02. 06. 2025 | Bugfixes, Modding, Scripting | Modding: Added `helpers` to settings and prototype stages.; Scripting: Added LuaHelpers::game_version read.; Scripting: Added LuaHelpers::compare_versions(). |
| **2.0.56** | 19. 06. 2025 | Minor Features, Changes, Bugfixes, Modding, Scripting | Minor Features: Added ability to undo rotating or flipping an entity. ; Changes: Changed how captive spawners work to always allow spoilage into the trash slots.  … |
| **2.0.57** | 19. 06. 2025 |  | только багфиксы |
| **2.0.58** | 23. 06. 2025 | Bugfixes, Modding, Scripting | Modding: Added the "mod-data" prototype type.; Modding: Added CraftingMachinePrototype::crafting_speed_quality_multiplier, module_slots_quality_bonus and energy_usage_quality_multiplier.; Scripting: Added LuaEntityPrototype::neighbour_connectable read. |
| **2.0.59** | 09. 07. 2025 | Changes, Optimizations, Graphics, Bugfixes, Modding, Scripting | Changes: [space-age] Remastered and remixed music.; Changes: [space-age] More icons in factoriopedia made unique. … |
| **2.0.60** | 10. 07. 2025 | Changes, Bugfixes | Changes: Moved the ammo turret request-slot closer to the turret center visually.  |
| **2.0.61** | 30. 07. 2025 | Changes, Graphics, Bugfixes, Modding, Scripting | Changes: When dragging belts, going forward and back will remove the extra belts built.; Changes: When using smart belt building to make a turn, the player can decide to change the direction after the turn by dragging in the opposite direction. … |
| **2.0.62** | 31. 07. 2025 | Bugfixes | только багфиксы |
| **2.0.63** | 04. 08. 2025 | Bugfixes | только багфиксы |
| **2.0.64** | 12. 08. 2025 | Minor Features, Changes, Bugfixes, Scripting | Minor Features: Heat interface can now heat entities and tiles.; Changes: Changed the blueprint setup GUI description field to include the icon picker.  … |
| **2.0.65** | 22. 08. 2025 | Bugfixes, Modding, Scripting | Modding: Heat energy sources support pollution.; Modding: Omitting required_tiles in a tile_buildability_rules's item now default to "all" (instead of "none" which was making the entities unbuildable)  … |
| **2.0.66** | 02. 09. 2025 | Minor Features, Changes, Bugfixes, Modding, Scripting | Minor Features: Windows executables now undergo code signing.; Changes: Reverted belt building changes from 2.0.61. … |
| **2.0.67** | 22. 09. 2025 | Minor Features, Changes, Graphics, Bugfixes, Modding, Scripting | Minor Features: Partially fulfilled wait conditions use different background color to indicate progress.; Minor Features: Splitters can be connected to circuit network. … |
| **2.0.68** | 23. 09. 2025 | Graphics, Bugfixes | только багфиксы |
| **2.0.69** | 29. 09. 2025 | Bugfixes, Modding, Scripting | Modding: Added MiningDrillPrototype::resource_searching_offset.; Modding: Added "scripted" technology trigger. … |
| **2.0.70** | 13. 10. 2025 | Bugfixes, Modding | Modding: Added CargoStationParameters::is_input_station and ::is_output_station to mainly clarify tooltips.  |
| **2.0.71** | 16. 10. 2025 | Bugfixes | только багфиксы |
| **2.0.72** | 22. 10. 2025 | Changes, Bugfixes | Changes: Decider combinator, arithmetic combinator and selector combinator are now primary energy consumers and have buffer size increased to make them more reliable in case of low power.; Changes: Reduced selector combinator energy usage from 5kW to 1kW. … |
| **2.0.73** | 13. 01. 2026 | Gui, Bugfixes, Scripting | Scripting: Added LuaEntity::send_to_orbit_automatically read/write. |
| **2.0.74** | 10. 02. 2026 | Bugfixes, Modding, Scripting | Modding: space-age, quality and elevated-rails mod versions were not bumped for this update as nothing has changed.; Scripting: Added LuaEntityPrototype::inserter_max_belt_stack_size read.; Scripting: Changed LuaEntityPrototype::automated_ammo_count read to also work for artillery wagons. |
| **2.0.75** | 12. 02. 2026 | Bugfixes, Modding | Modding: space-age, quality and elevated-rails mod versions were not bumped for this update as nothing has changed. |
| **2.0.76** | 25. 02. 2026 | Bugfixes, Scripting | Scripting: Added LuaEntityPrototype::reversing_power_modifier read. |
---

## 4. Что изменилось в моддинге при переходе на 2.0 (и что добавилось потом)

> Порядок: сначала data-этап (прототипы), затем runtime-этап (скриптинг). Всё взято из официальных ченджлогов (разделы **Modding** и **Scripting**), полный список по версиям — в `docs/changelogs/modding-scripting-API-изменения-2.0.md`.

### 4.1 Новые типы прототипов (data stage) — введены в 2.0.7

| Прототип | Назначение |
|---|---|
| `asteroid` | астероиды (типы с составом, размерами, добычей) |
| `asteroid-collector` | коллекторы астероидов (фильтры через control behavior) |
| `asteroid-chunk` | чанки-предметы астероидов |
| `thruster` | двигатели космических платформ |
| `cargo-landing-pad` | посадочные площадки карго (запросы, логистика) |
| `space-platform-starter-pack` | стартовый набор платформы |
| `space-location` | любая точка в космосе (планета, орбита, своя локация) |
| `planet` | планета: `surfaces`, `map_gen_settings`, `surface_properties`, `gravity_pull`, `distance`, `orientation`, `order`, `platform_procession_set`, `planet_procession_set`, `asteroid_spawn_influence`, `persistent_ambient_sounds`, `pollutant_type` и т.д. |
| `space-connection` | гиперпрыжок/маршрут между локациями, стоимость, условия |
| `surface-property` | свойства поверхности (день/ночь, гравитация, магнитное поле, солнечная энергия, давление и др.) |
| `surface` | прототипы поверхностей (планетные поверхности) |
| `procession`, `procession-layer-inheritance-group` | «процессии» — визуальные караваны объектов на орбите/планете (используются в SA для симпатичных шествий на орбите) |
| `active-trigger`, `chain-active-trigger` | триггеры активностей (события при входе/выходе и т.д.) |
| `quality` | уровни качества (поля: `level`, `color`, `next`, `next_probability`, `chain_probability` (2.1), все `*_multiplier`) |
| `spider-unit` | универсальные «пауки» (спидэртроны и похожие, API-тип `LuaSpiderVehicle`) |
| `capture-robot` | роботы захвата существ (Gleba) |
| `custom-event` | кастомные события, объявляемые в data-этапе (общий namespace с custom-input и встроенными) |

Добавлено позже: **`infinity-cargo-wagon`** и **`proxy-container`** (2.0.38), `SpiderVehicleGraphicsSet::default_color` (2.0.38), `FusionReactorPrototype::target_temperature` (2.0.44), `RocketSiloPrototype::can_launch_without_landing_pads` (2.0.44), `CargoStationParameters::is_input_station`/`is_output_station` (2.0.70), `FusionGeneratorPrototype::burns_fluid`/`effectivity` + `heating_energy` для Thruster (2.0.67), `LightningPrototype::attractor_hit_effect` (2.0.67), `RoboportPrototype::render_recharge_icon` (2.0.67), `loader`-поля (`respect_insert_limits` 2.0.65, `per_lane_filters` 2.0.14, `frozen_patch_in/out` 2.0.12), `ItemPrototype::spoil_level` (2.0.18), `LoaderPrototype::frozen_patch_*`, `MiningDrillPrototype::resource_searching_offset` (2.0.69), скриптовый триггер технологии `scripted` (2.0.69), `FluidWagonPrototype::connection_category` (2.0.69), `RecipePrototype::hide_from_bonus_gui` (2.0.61), `EntityPrototype::draw_stateless_visualisations_in_ghost` (2.0.65), `custom_tooltip_fields` на всех прототипах (2.0.59/2.0.67), `Prototype::custom_tooltip_fields`.

### 4.2 Важное: переименования и удаления в data-этапе

- `LuaEntityPrototype::stack` → **`bulk`**; мосты: «stack inserter» теперь НОВАЯ сущность, старые — `bulk-inserter`.
- Удалены: `StorageTankPrototype::scale_entity_info_icon`, `LinkedContainerPrototype::scale_info_icons`, `ContainerPrototype::scale_info_icons`, `RobotWithLogisticInterfacePrototype::cargo_centered`, утилита `pollution_color`, глобал `biter_ai_settings` (теперь `require("biter-ai-settings.lua")` возвращает таблицу), product type **`research-progress`** из рецептов (2.0.67).
- `LuaTilePrototype::placeable_by` → `LuaTilePrototype::items_to_place_this` (2.0.59).
- Автоплейс-контроли: вода стала прототипом с noise-выражениями (`water_level`, `segmentation_multiplier`), имена переменных в noise-выражениях укорочены (2.0.7); скрытие автоплейса убирает его из GUI мап-генерации (2.0.67).
- `RenderLayer` у части прототипов — **строка вместо числа** (`LuaParticlePrototype::render_layer`, `LuaTrivialSmokePrototype::render_layer`, 2.0.65).
- `utility constants` для графики: `recipe_icon_scale` (2.0.67), объединённые ghost-тинты `ghost_shader_tint`/`ghost_shaderless_tint` (2.0.14).
- `base/space-age` tile collision mask tables больше не шаринг-ссылки (2.0.18) — если делаешь миграции/онли-патчи, копируй таблицы, а не мутируй.

### 4.3 Runtime (control stage): главные изменения 2.0

**Переименования/удаления (ломают старые моды — обязательно прочитать!):**

- `global` → **`storage`** (это самое известное). Функции внутри `global` теперь ошибка при сохранении.
- Глобальные объекты: **`prototypes`**, **`helpers`** (в т.ч. в `on_load`); `helpers` содержит `table_to_json/json_to_table/write_file/remove_path/direction_to_string/evaluate_expression/encode_string/decode_string/parse_map_exchange_string/check_prototype_translations/is_valid_sound_path/is_valid_sprite_path`; `prototypes` содержит все `LuaPrototypes::*` (вместо `game.X_prototypes`), `get_history`, `style`, `map_gen_preset`, `named_noise_expression`.
- `LuaBootstrap::active_mods` вместо `game.active_mods`; `LuaSettings::player` → **`player_default`**.
- Удалены `help()` у всех объектов, `LuaObject::isluaobject`, тип Lua-объектов теперь `userdata` (не `table`), `__self` удалён.
- `LuaUnitGroup` → **`LuaCommandable`** (`group_number` → `id`; `unit_group` → `parent_group`; заменители `command`, `set_command`, `distraction_command`, `moving` удалены).
- `on_entity_destroyed` → **`on_object_destroyed`** (и `register_on_entity_destroyed` → `register_on_object_destroyed`).
- Статистика: `LuaForce::item_production_statistics` и др. → методы `get_item_production_statistics()`, `get_fluid_production_statistics()`, `get_kill_count_statistics()`, `get_entity_build_count_statistics()`; `LuaGameScript::pollution_statistics` → `get_pollution_statistics()`; `LuaFlowStatistics::get_flow_count` аргумент `bool input` → `string category` (+ `storage` категория, `set_storage_count`, `storage_counts`).
- Железнодорожный API: `LuaSurface::get_trains`, `LuaForce::get_trains`, `get_train_stops`, `game.get_train_by_id` → **`LuaTrainManager`** (`game.train_manager:get_trains()`, `:get_train_stops()`, `:get_train_by_id()`, `:request_train_path()`); `LuaTrain::front_rail/back_rail/rail_direction_from_*` → `LuaEntity::get_rail_end` (`LuaRailEnd`).
- Логистика: унифицировано через `LuaLogisticPoint`/`LuaLogisticSection`; удалены `clear_vehicle_logistic_slot`, `get_requester_point` теперь `LuaControl::get_requester_point()`, `LuaEntity::request_slot_*` удалены.
- Цепь: см. раздел 2.6 (`defines.circuit_connector_id` удалён; `LuaCircuitNetwork` привязан к `WireConnectorID`).
- `LuaEntity::text` удалён; `LuaPlayer::open_map/zoom_to_world/close_map` удалены (вместо `set_controller` + `centered_on`).
- `LuaTechnology::effects` → `LuaTechnologyPrototype::effects`; `LuaForce::research_queue_enabled` удалено; `LuaForce::get_saved_technology_progress/set_…` → `LuaTechnology::saved_progress`.
- `defines.direction` стал **16 направлений** (моды, хранящие направления, мигрируют умножением на 2 — официальная рекомендация из ченджлога!).
- `LuaRendering` → `LuaRenderObject` для манипуляций; `LuaGameScript::is_valid_sound_path` → `helpers.is_valid_sound_path`; `LuaRendering::is_font_valid` → `prototypes.font`.
- `LuaSurface::spill_item_stack` теперь принимает **таблицу параметров** (добавлены `max_radius`, `use_start_position_on_failure`).
- `on_built_entity`/`on_robot_built_entity`: параметр `created_entity` → **`entity`**, вместо `stack/item` передаётся **`consumed_items`** (модифицируемый стек).
- `LuaEntity::rotate` без опций; `LuaEntity::get_upgrade_direction` удалён; `LuaEntityPrototype::max_health` → `get_max_health(quality?)` + `LuaEntity::max_health`.

**Крупные добавления (для новых модов):**

- `LuaSpacePlatform`, `LuaPlanet` (`:get_space_platforms()` 2.0.64, `associate_surface`), `LuaSimulation`, `LuaTrainManager`, `LuaRecord` (+ `is_preview` 2.0.66, `blueprint_description` 2.0.64), `LuaUndoRedoStack` (`player.undo_redo_stack`), `LuaNamedNoiseFunction`, `LuaAirbornePollutantPrototype`, `LuaWireConnector`, `LuaRailEnd`, `LuaLogisticSection`, `LuaCustomEventPrototype`, `LuaEntity::custom_status`, `LuaEntity::quality`, `LuaEquipment::quality`, `LuaEntity::rail_layer`, `mirroring`, `commandable`, `LuaPlayer::physical_*`, `LuaPlayer::land_on_planet()`, `enter/leave_space_platform()`, `LuaForce::unlock_space_location/create_space_platform/unlock_space_platforms/unlock_quality + is_*`, `set_surface_hidden`, `platforms`, `game.planets`, `game.simulation`, `get_entity_by_unit_number`, `set_win_ending_info/set_lose_ending_info`, `LuaSurface::planet`, `platform`, `execute_lightning`, `global_electric_network`, `pollutant_type`, `deletable`, `create_global_electric_network`, `set_double_hidden_tile`, `LuaTile::double_hidden_tile`, `LuaPlayer::locale`, `LuaPlayer::swap_characters()` (2.0.67), `pipette()` (2.0.59), `LuaPlayer::get_recipe_notifications()` (2.0.67), `flip_horizontal/flip_vertical` для `build_from_cursor` (2.0.67), `LuaForce::get_chunk_chart` (2.0.61), `LuaHelpers::send_udp/recv_udp` + `on_udp_packet` (2.0.59), `LuaEntity::apply_upgrade()` (2.0.61), `LuaPlanet`, `on_player_dropped_item_into_entity` (2.0.69), `LuaForce::script_trigger_research()` (2.0.69), `maximum_quality_jump` utility constant (2.0.69), демолишер/территория API (2.0.61), события агро-башен (`on_tower_planted_seed`, `on_tower_pre_mined_plant`, `on_tower_mined_plant`), `on_cargo_pod_started_ascending` (2.0.67), `on_marked_for_upgrade` + `previous_target`/`previous_quality` (2.0.67), `in_gui` в custom input events (2.0.67 + десинк-фикс 2.0.77), `surface_index` в UndoRedoActions (2.0.67), `LuaSplitterControlBehavior` (2.0.67), `LuaCustomChartTag::position/surface` write (2.0.67), `LuaFluidBox::get_fluid_segment_extent_bounding_box()` (2.0.67), `LuaItemPrototype::get_module_effects()` (2.0.67), `LuaEntity::display_panel_*` (2.0.59), `LuaEntityPrototype::tile_buildability_rules` (2.0.61), `register_plant` в `LuaSurface::create_entity` (2.0.61), `LuaEntity::register_tree()` (2.0.61), `LuaRendererObject::dash_offset` (2.0.66), `overflow` в `revive/silent_revive` (2.0.66), `LuaGameScript::allow_debug_settings` (2.0.66), `LuaPlayer::set_zoom_limits()` (2.0.61), `LuaControl::can_place_entity` из `player` (2.0.61), `LuaEntity::pumped_last_tick` (2.0.61), `LuaEntity::send_to_orbit_automatically` (2.0.73), `LuaEntity::reversing_power_modifier` (2.0.76), `LuaEntityPrototype::inserter_max_belt_stack_size` (2.0.74), `automated_ammo_count` для арт-вагонов (2.0.74), quality-reads (2.0.77).

### 4.4 Официальные инструменты для моддера

- **API-документация:** `https://lua-api.factorio.com/latest/` (текущая), по версии: `https://lua-api.factorio.com/2.0.76/` — тот же URL-шаблон с версией; JSON-варианты: `runtime-api.json`, `prototype-api.json` (страницы `json-docs.html`, `index-prototype.html`). В 2.0.77 у дока появился полнотекстовый поиск (онлайн).
- **Локальная документация в игре:** папка `doc-html/` рядом с `data/` (например `<install>/doc-html/auxiliary/data-lifecycle.html`).
- **wube/factorio-data** — все прототипы официальных модов по версиям (теги!), `changelog.txt` (источник всех ченджлогов), `base/migrations/` (готовые примеры миграций). Сравнение версий: `git diff 2.0.70 2.0.76` или GitHub compare-URL.
- **Mod Portal:** `https://mods.factorio.com/`, API: `https://mods.factorio.com/api/v2/mods?...`, токен API создаётся в профиле на factorio.com (права: Upload/Edit/Publish mods).
- **Блог Wube / Friday Facts:** `https://factorio.com/blog` (архив) и `https://wiki.factorio.com/Friday_Facts` (оглавление). Ключевые для 2.0: FFF-374 (роботы), FFF-375 (quality), FFF-377 (рельсы), FFF-378 (эстакады), FFF-380 (remote view), FFF-384/405 (комбинаторы), FFF-389/395 (поезда), FFF-393 (stack inserters), FFF-398/399 (Fulgora), FFF-401 (террейн), FFF-403 (rail planner), FFF-406 (музыка Petr Wajsar), FFF-408 (график аккумуляторов), FFF-410 (турели+цепь), FFF-416 (жидкости), FFF-418 (дата релиза), FFF-444 (2.1 Experimental).
- **Factorio Wiki, раздел моддинга:** `Tutorial:Modding_tutorial`, `Mod_structure`, `Prototype_definitions`, `Data_lifecycle`, категория `Modding`; `Version_history` — вся история версий.

---

## 5. Гайд: как устроен мод изнутри (актуально для 2.0)

### 5.1 Структура мода

```
my-mod/                       ← zip: my-mod_1.0.0.zip (name_version)
├── info.json                 ← единственный обязательный файл
├── settings.lua              ← настройки мода (startup/runtime)
├── data.lua                  ← прототипы (расширение)
├── data-updates.lua          ← правки чужих прототипов (после их data)
├── data-final-fixes.lua      ← последние правки (после ВСЕХ модов)
├── control.lua               ← рантайм-логика
├── locale/
│   ├── en/base.cfg           ← [item-name], [entity-name], [recipe-name]…
│   └── ru/base.cfg           ← переводы
├── graphics/                 ← png-спрайты, анимации, иконки
├── sound/                    ← ogg/wav
├── prototypes/               ← твои lua-модули для data
├── migrations/<версия>.lua   ← правки существующих сейвов
├── thumbnails/thumbnail.png  ← обложка на портале (512×512)
└── changelog.txt             ← версии и изменения (показывается в игре)
```

### 5.2 info.json (все поля)

```json
{
  "name": "my-mod",
  "version": "1.0.0",
  "title": "My Mod",
  "author": "You",
  "factorio_version": "2.0",
  "homepage": "https://mods.factorio.com/mod/my-mod",
  "description": "Короткое описание (до ~800 символов).",
  "dependencies": [
    "base >= 2.0.0",
    "? space-age >= 2.0.0",
    "(?) quality >= 2.0.0",
    "! incompatible-mod"
  ],
  "license": "MIT"
}
```

- `factorio_version` в 2.0 **устарел/опционален** (портал ведёт версии сам), но полезен для читаемости; реальная совместимость задаётся `dependencies`.
- `license` — рекомендован (портал показывает); популярные: MIT, CC BY-NC-SA, «Custom».
- `thumbnail` по умолчанию берётся из `thumbnails/thumbnail.png` (512×512 PNG).
- Портал требует: имя `[a-z0-9-_]+`, уникальность `name`, версия `x.y.z`.

### 5.3 Жизненный цикл загрузки (data lifecycle)

1. **settings stage** — у всех модов `settings.lua` (только `ModSetting*` прототипы; стартап-настройки доступны в data-этапе через `settings.startup`).
2. **data stage** — у всех модов `data.lua` в порядке зависимостей, затем `data-updates.lua`, затем `data-final-fixes.lua` (повторно в том же порядке; `data` и `data-updates` итерируются, `data-final-fixes` — финально).
3. **control stage** — `control.lua` запускается при старте мира (и `on_load` для восстановления `storage`).

Всё определяется в `data:extend({...})`, читается через `data.raw` (глобальный `data` + `settings` + `mods` в data-этапе). Каждый прототип обязан иметь `type` и `name`; имена валидны для `item.raw`, `entity.raw`, `recipe.raw`, `technology.raw`, `fluid.raw`, `tile.raw`, `equipment.raw`, `module.raw`, `quality.raw`, `planet.raw`, `space-location.raw` и т.д.

### 5.4 Пример 1 — предмет + рецепт + технология

```lua
-- data.lua
data:extend({
  {
    type = "item",
    name = "my-super-ore",
    icon = "__my-mod__/graphics/icons/my-super-ore.png",
    icon_size = 64,
    subgroup = "raw-resource",
    order = "z[super-ore]",
    stack_size = 100
  },
  {
    type = "recipe",
    name = "my-super-ore-smelting",
    category = "smelting",
    energy_required = 8,
    ingredients = {{type="item", name="my-super-ore", amount=2}},
    results = {{type="item", name="iron-plate", amount=1}},
    enabled = false,          -- открывается технологией
    icons = {{icon = "__my-mod__/graphics/icons/my-super-ore.png", icon_size = 64}},
    always_show_made_in = true
  },
  {
    type = "technology",
    name = "my-super-ore-processing",
    icon = "__my-mod__/graphics/icons/my-super-ore.png",
    icon_size = 64,
    effects = {
      {type = "unlock-recipe", recipe = "my-super-ore-smelting"},
      {type = "mining-productivity", modifier = 0.1}
    },
    prerequisites = {"automation-science-pack", "logistics"},
    unit = {
      count = 100,
      ingredients = {{"automation-science-pack", 1}},
      time = 30,
      researching_speed = 1
    },
    order = "z"
  }
})
```

### 5.5 Пример 2 — новое здание (сборочная машина)

```lua
{
  type = "assembling-machine",
  name = "my-assembler",
  icon = "__my-mod__/graphics/icons/my-assembler.png",
  icon_size = 64,
  flags = {"placeable-neutral", "player-creation"},
  minable = {mining_time = 0.5, result = "my-assembler"},
  max_health = 300,
  corpse = "my-assembler-remnant",
  collision_box = {{-1.4, -1.4}, {1.4, 1.4}},
  selection_box = {{-1.5, -1.5}, {1.5, 1.5}},
  fast_replaceable_group = "assembling-machine",
  energy_usage = "200kW",
  energy_source = {type = "electric", usage_priority = "secondary-input", drain = "10kW"},
  crafting_categories = {"crafting", "advanced-crafting"},
  crafting_speed = 1.5,
  ingredient_count = 4,
  result_inventory_size = 2,
  fluid_boxes = {...},
  animation = {
    layers = {
      { filename = "__my-mod__/graphics/entity/my-assembler.png", -- цикл работы
        width = 192, height = 192, frame_count = 32, line_length = 8,
        direction_count = 4, animation_speed = 0.5,
        shift = util.by_pixel(0, 0), scale = 0.5 },
      { ... маски/подсветки ... }
    }
  },
  working_visualisation = {...},          -- заготовки/прогресс
  open_sound / close_sound / working_sound = {...},
  circuit_wire_connection_points / circuit_connector = {...},
  allowed_effects = {"consumption", "speed", "productivity", "pollution"},
  module_specification = {module_slots = 2, module_info_icon_shift = ...}
}
```

### 5.6 Настройки (`settings.lua`)

Типы: `int-setting`, `string-setting`, `bool-setting`, `double-setting`, `color-setting` (в 2.0.66 добавлено поле `forced_value`), `dropdown-setting` (значения `{type="choice", ...}` — в 2.0 можно и просто массив строк). Поля: `name, setting_type ("startup"|"runtime-global"|"runtime-per-user"), default_value, allowed_values, order, per_user, force_restart, visible_if` (условие показа). Чтение: `settings.startup["x"].value`, `settings.global["x"].value`, `settings.get_player_settings(player)["x"].value`.

### 5.7 Локализация

- Файлы: `locale/<lang>/cfg-файлы` (`base.cfg`, `my-mod.cfg`), секции `[item-name]`, `[item-description]`, `[entity-name]`, `[entity-description]`, `[recipe-name]`, `[technology-name]`, `[fluid-name]`, `[mod-setting-name]`, `[mod-setting-description]`, `[shortcut-name]`, `[tips-and-tricks]` и т.д.
- Плейсхолдеры: `__1__`, `__2__`; **плюрализация в 2.0 — с двойными подчёркиваниями вокруг индекса параметра** (`__1__` → `__1__` для ед., `__2__` для мн., формат изменился по сравнению с 1.1 — см. ченджлог 2.0.7).
- **Автоматические параметры локали** (2.0.67): `__TECHNOLOGY__` и `__RECIPE__` — вставляют локализованные названия из прототипов.
- `helpers.check_prototype_translations()` — проверка покрытия переводов; `game.players`/`prototypes` читают `LuaPlayer::locale` (2.0.7).
- Переводы портала: `https://forums.factorio.com/viewforum.php?f=165` (Сrowdin Wave? — официальный перевод-трек), но для мода проще: портал сам умеет черновики переводов (языковые файлы в моде).

### 5.8 Миграции и совместимость сейвов

- `migrations/<from-version>.lua` — выполняются при загрузке сейва со старой версии (имя файла = версия мода, с которой мигрирует). Меняют `data.raw` ПОСЛЕ data-этапа: `data.raw["item"]["x"]...` и вызывают `game.merge_prototypes`? — нет, миграции работают на `data.raw` и `game` (см. `base/migrations/2.0.0 stack inserter rename.json`).
- В `control.lua` — `script.on_configuration_changed(data)` для runtime-миграций (`data.mods`, `data.migrations`, `data.mod_changes`); именно там чинят `global/storage` и объекты.
- Никогда не храни в `storage` ссылки на `LuaEntity`/`LuaPlayer` — храни `unit_number`; восстановление в `on_load`/`on_init`.

### 5.9 Скрипты: базовый каркас

```lua
-- control.lua
local event = require("__core__.lualib.event_handler")
local mod_gui = require("__core__.lualib.mod-gui")   -- добавление GUI в интерфейс

script.on_init(function() storage.started = true end)
script.on_load(function() ... end)

script.on_event(defines.events.on_built_entity, function(e)
  local ent = e.entity -- в 2.0 параметр называется entity!
  ...
end)

script.on_event(defines.events.on_space_platform_built_entity, function(e) ... end)
script.on_event("my-custom-event", function(e) ... end)  -- кастомные события по имени
```

- `script` — унаследованный API; в 2.0 рекомендована связка `storage` + `prototypes` + `helpers` + `script` (всё ещё `script.on_event`, `register_on_*`).
- Начни с `event_handler.lua` из `core/lualib` — там паттерн `add_handlers` и защита от повторной регистрации.
- Для GUI: `LuaGuiElement` современный API (`player.gui`, `add{type="frame", ...}`, `mod_gui.get_frame_flow`), иконки: `icon_selector` в textfield/textbox (2.0.7).

### 5.10 Space Age в модах: мини-планета

```lua
data:extend({
  {
    type = "planet",
    name = "my-planet",
    icon = "__my-mod__/graphics/icons/my-planet.png",
    starmap_icon = "__my-mod__/graphics/icons/my-planet-starmap.png",
    starmap_icon_size = 512,
    gravity_pull = 10, distance = 20, orientation = 0.3, magnitude = 2,
    order = "d[my-planet]", subgroup = "planets",
    map_gen_settings = { ... свой генератор ... },
    surface_properties = {
      ["day-night-cycle"] = 10 * 60,
      ["magnetic-field"] = 20,
      ["solar-power"] = 300,
      pressure = 1000, gravity = 20
    },
    platform_procession_set = { arrival = {...}, departure = {...} },
    planet_procession_set = { arrival = {...}, departure = {...} },
    asteroid_spawn_influence = 1,
    asteroid_spawn_definitions = {...},
    persistent_ambient_sounds = {...}
  },
  {
    type = "space-location",
    name = "my-moon",
    planet = "my-planet",  -- or distance/orientation for free-floating
    ...
  }
})
```

Для готовой обвязки используй **PlanetsLib** (github.com/danielmartin0/PlanetsLib, mods.factorio.com/mod/PlanetsLib, MIT): орбитальные деревья, плането-специфичные варианты сущностей, генерируемые планеты и т.д. Отличный источник паттернов — исходники `space-age/prototypes/planet/planet.lua` в wube/factorio-data.

### 5.11 Factoriopedia и «встроенные» страницы

Моды могут: давать `factoriopedia-simulations` (прототипы), подключать `custom_tooltip_fields` (2.0.59/2.0.67), использовать `__TECHNOLOGY__/__RECIPE__`, `recipe_icon_scale` utility constant, `hide_from_bonus_gui` (2.0.61), иконки с `icons_positioning`/`icon_draw_specification` (2.0.66/2.0.67). Вики-аналог: `https://wiki.factorio.com/Factoriopedia`.

---

## 6. Графика, анимации и «3D» в Factorio (полный разбор)

### 6.1 Почему «3D-модели» — это неправильное понимание движка

- Factorio **не имеет 3D-рендера в рантайме**. Всё, что видно в игре — **2D-спрайты** (PNG) и **анимации-последовательности** (кадры). Есть перспектива/псевдо-ортогональная проекция («2.5D»), тени, освещение (в т.ч. dynamic lights), но это всё растеризованные спрайты с эффектами.
- Wube и моддеры создают «3D» **офлайн**: модель в Blender → рендер со статичной камеры на каждый угол поворота и каждый кадр анимации → набор PNG → сборка в спрайт-шит (`*.png` big sheet) → описание в `animation`/`pictures`.
- Значит, для качественного мода с уникальной графикой тебе нужен **один из двух пайплайнов**:
  1. **Pixel-art (2D)** — Aseprite/Krita/Piskel: рисуешь кадры вручную (стиль Wube: «facility» со скруглениями, тёмные обводки, палитра).
  2. **3D-рендер → спрайты** — Blender (как Wube): экономит время на сложных машинах, даёт консистентное освещение и повороты.

### 6.2 Базовые типы спрайтов/анимаций (актуальные поля)

| Тип | Назначение | Ключевые поля |
|---|---|---|
| `sprite` | одиночное изображение (pictures, иконки вместо `icon`) | `filename, width, height, frame_count=1, line_length, scale, shift, tint, hr_version` |
| `animation` | многокадровая анимация (машины, роботы, существа) | `frames` (или `filename`-сборка), `frame_count, line_length, direction_count, animation_speed, repeat_count, run_mode ("forward"/"backward"/"forward_backward"), shift, scale, tint, layers` |
| `animation_sheet` | она же, но один файл-шит | `filename` + `size`/`width`/`height` + `frame_count` + `direction_count` |
| `animation4way` | упрощённый 4-напр. вариант | `east/north/west/south` (каждый — animation) |
| `graphics_set` | полный сет сущности (для 2.0 добавлены `SpiderVehicleGraphicsSet::default_color` и т.п.) | `animation, water_reflection, corpse, shadow...` |
| `belt_animation_set` | ленты | `animation_set` (шит 20/позиции: 1=east, 3=north, ... 13–20 = старты/концы, индексы можно переопределить), `belt_reader`, `side/backing` |
| `rail` (прототип) | рельсы | `rail_pictures` (straight/curved/…), `rail_ramp`, `rail_support` — свои прототипы; `rail_layer` |
| `icon`/`icon_size` | иконки предметов/технологий | `icon` + `icon_size` (32/64/128), `icons` (массив со `tint`, `shift`, `scale`, `icons_positioning`), `icon_draw_specification` |
| `decal` | накладки/декали (вода-маскирование — 2.0.44) | `layer` (vs `UtilityConstants::capture_water_mask_at_layer`), `lightmap_alpha`, `opacity_over_water` |
| `light` | источники света | `intensity, size, color, minimum_darkness...` |
| `corpse`/`remnant` | обломки | `remnants` + `corpse` на прототипе сущности |
| `sound` | звуки (см. §7) | `advanced_volume_control, priority, speeds...` |

Ключевые общие поля для всех графических типов: `filename` (**обязательно** с `__modname__/` префиксом пути), `width/height` или `size`, `frame_count`, `line_length`, `direction_count`, `scale` (обычно 0.5 для 64px тайла с 128px ассетами), `shift` (коррекция позиции; `util.by_pixel(x, y)` — сдвиг в пикселях из центра), `tint` (цветовой оттенок, `{r,g,b,a}`), `blend_mode` (`normal`, `additive`, `multiply`, `subtract`...), `render_layer`, `flags` (`mask`, `no-crop`, `icon`, `compress`, `group`, `mipmap`...), `hr_version` (версия в высоком разрешении; поле в 2.0 используется реже, т.к. хайрез покрывается отдельными файлами `-hr.png`/`scale`), `uv`/`sprite_parameters`, `draw_as_shadow`, `draw_as_glow`, `fade_out...`, `max_shift`/`max_shadow_shift` (у специфических сущностей).

### 6.3 Правила компоновки листов (очень важно!)

- **Сетка тайла:** 1 тайл = 32×32 пикселя «логических» (base resolution). Сущности 3×3 тайла = 96×96 логических. Обычно рисуем в 2× (`scale = 0.5` при 64px/тайл) или 4× (256px/тайл, `scale=0.25`).
- **Направления:** 4 (упрощённые, `direction_count=4`), 8 («стандарт» для машин/роботов), 16/32 (для детальных существ; в 2.0 `defines.direction` = 16, но у графики `direction_count` может отличаться). Порядок кадров: сначала кадры 0..N для направления 0, потом направление 1 и т.д.; `line_length` = сколько кадров в строке листа.
- **Именование:** `my-entity.png` + `my-entity-hr.png`, `my-entity-shadow.png`, `my-entity-mask.png` (если нужен blend-маска).
- **Атласы:** минимальный 4096 (2.0.38) — очень большие одиночные `animation_sheet` дешевле по VRAM, чем тысячи отдельных `frame_count`, но помни про лимит размера текстуры; не превышай 8192×8192 без нужды. Используй `compress` флаг и `mipmap` для иконок.
- **Иконки:** 32–64px `icon_size` (и 128 для спеков планет/технологий). Steam-обложка мода: 512×512.

### 6.4 Полный 3D-пайплайн (как у Wube) — по шагам

1. **Моделирование** в Blender: низкий/средний полигонаж под стиль игры; материалы — node-материалы с освещением; «каноничный» вкус Wube — тёмный контур, скругления, «инженерная» палитра (красный/серый/чёрный + акцент цвета фракции).
2. **Сцена:** ортографическая камера (ортографический масштаб = размер тайла), объект на origin в центре тайла, сетка тайлов-«плитки» (плашка 32/64px), плоскость-тень (shadow catcher), солнце сверху-слева, ambient-заливка, для «высотных» объектов — лёгкая перспектива/смещение по Y (`shift`).
3. **Анимация:** NLA-треки (работа/ходьба/атака/умирание) с кейфреймами; для гусениц/конвейеров — «волнистые» сдвиги фаз (у Wube — procedurally «chained» массивы; для моддеров отлично работает аддон ARew0 — фейковые массивы).
4. **Рендер по направлениям:** камера смотрит сверху, модель вращается (4×90°, 8×45°, 16×22.5°), либо камера вокруг модели с сохранением «севера»; в Blender удобно кейфрамить камеру + `scale.x = -1` для зеркальных курсов (как в известном гайде «How to make new belt graphics»). Экспорт кадров: `PNG RGBA` без сжатия-потерь.
5. **Сборка шита:** склейка кадров по сетке (напр. 32×32 кадра, `factorio-spritter`: `spritter spritesheet input/ output/ --lua --tile-resolution 64 --scale 0.5`, авто-кроп прозрачности, дедупликация пустых кадров с генерацией `frame_sequence` — это **прямо поддерживает 2.0**!); ImageMagick: `magick montage "*.png" -geometry +0+0 -tile 32x32 -background rgba(0,0,0,0) sheet.png`.
6. **Генерация Lua-описания:** `factorio-spritter --lua` отдаёт таблицу `animation` с нужными полями; либо `blender-factorio-utils` генерирует «блок lua-кода» из аддона.
7. **Проверка в игре:** загрузка мода, `animation_speed` подгонка, тень (`draw_as_shadow` или отдельный shadow-слой), проверка на совместимость с `scale`, `shift`, чтоб объект «стоял» на тайле, а не «плавал».

**Инструменты сообщества (проверены и живут):**

- **factorio-spritter** (github.com/fgardt/factorio-spritter, Rust CLI): сборка спрайт-шитов из папок, генерация Lua/JSON, mipmap-иконки, gif, оптимизация (pngquant), split-обратное, crop, `frame_sequence` — идеален для CI-конвейера.
- **blender-factorio-utils** (github.com/AshenHermit/blender-factorio-utils, v0.8+): сетап сцены (shadow catcher, сетка тайлов, камера/свет), рендер NLA-анимаций в спрайты по направлениям, генерация Lua.
- **Spritify** (forum f=34 t=5336, ремейк для Blender 2.8+ — github.com/jmattspartacus/blender_spritify): аддон-специфичный для спрайт-шитов.
- **ImageMagick** (montage) — простейшая склейка.
- **Aseprite / Krita / GIMP** — для 2D-пайплайна и «докрутки» рендеров (обводки, уникальные циклы).
- Кейсы «с нуля»: гайд «How to make new belt graphics» (форумы, t=58416) — там весь процесс рельсовой/ленточной графики с Blender; примеры Scourge/df_belt_graphics.

### 6.5 Чек-лист графики «уровня Wube»

- [ ] Все пути через `__modname__/...`, иконки читаемы на 32px.
- [ ] Спрайты: верные размеры (`width/height` или `size`), `scale=0.5` для 128px, `shift` через `util.by_pixel`.
- [ ] `direction_count` совпадает с реальным числом направлений; `line_length` — с шириной листа.
- [ ] HR-версии (если обещаешь хайрез): отдельные файлы (обычно `-hr.png`).
- [ ] Тень/отражение воды (`water_reflection`), `corpse/remnant`, `mask`/`draw_as_glow` для эффектов.
- [ ] Анимация: `frame_count` верный, `animation_speed` согласована с `tick`-логикой (60 FPS тайминг).
- [ ] Нет «дрожания»: позиции кратны 0.5 пикселя тайла; `pixel_snap`/`draw_as_light` where needed.
- [ ] VRAM-бюджет: предпочтительно меньше файлов большего размера на один лист; `compress` флаг.
- [ ] `custom_tooltip_fields`, Factoriopedia-симуляции, `icon_draw_specification` — если сущность с иконками в интерфейсе.
- [ ] Для SA: качество-поведение (`quality_affects_*`, `*_quality_multiplier`), иконки качества-уровней, planet/starmap иконки, `persistent_ambient_sounds`.

### 6.6 Sound-прототипы (важное из 2.0)

```lua
working_sound = {
  sound = {filename = "__my-mod__/sound/my-assembler.ogg", volume = 0.8},
  apparent_volume = 1.5,
  max_sounds_per_type = 3,
  advanced_volume_control = {
    attenuation = {distance = true},
    fades = {fade_in = 0.5, fade_out = 1.0},
    darkness_threshold = 0.3
  },
  priority = "some-priority",          -- 2.0.7
  speed_smoothing_window_size = 12     -- 2.0.7
}
```

- Поддерживаются `SoundDefinition::min_volume/max_volume`, `activity matching` (объём/скорость от активности), non-linear attenuation, sound aggregation с priority (замена при нехватке каналов), `SoundPath` типы `item-open/close/pick/drop/move` (2.0.59). Формат — **OGG** обычно.

---

## 7. Тестирование, отладка, CI и публикация

### 7.1 Локальный запуск

- Пути: Windows `%APPDATA%\Factorio\mods`, Linux `~/.factorio/mods`, macOS `~/Library/Application Support/factorio/mods`. Пакет = папка `name_version/` или zip `name_version.zip`. Симлинки/джанкшены работают — удобно для dev.
- `--mod-directory <path>` — отдельная папка модов (полезно для тестов).
- Headless-сервер (бесплатный, для тестов без GUI): `factorio.com/get-download/experimental/headless/linux64`; `--server-settings`, `--port`, `--rcon-port`...
- Консоль: `/c <lua>` (в сингле, выключает ачивки), `/editor` (editor/симулятор), `/perf` (профайлер), `/alerts`, `/time`, `--debug` лог, `LuaGameScript::allow_debug_settings` (2.0.66).
- Логи: `factorio-current.log`, `factorio-previous.log` рядом с модами; при падении мода в логе всегда стек Lua с номером строки.
- **FMTK** (VSCode «Factorio Modding Tool Kit», justarandomgeek.factoriomod-debug) — отладчик, автодополнение прототипов, быстрый reload; есть официальное видео-интро.

### 7.2 Чек-лист перед релизом

1. `info.json` валиден; `changelog.txt` в строгом формате (портал показывает и версии).
2. Все `data`-файлы без ошибок в `--validate`/чистом запуске; никаких `nil` в `data.raw`.
3. Миграции протестированы на сейвах прошлых версий мода.
4. `control.lua`: нет сохранения Lua-объектов в `storage`, нет уязвимостей к `on_load`; событийная дублируемость (`event_handler`).
5. Локализация min. en + ru; `helpers.check_prototype_translations()`.
6. Производительность: профиль `/perf`, избегай `on_tick` кода на каждый тик для каждого объекта (кэшируй), `event_filter`/`filter` в событиях построения.
7. Совместимость: минимум `base >= 2.0.0`; если SA — `space-age >= 2.0.0`; если работаешь с качеством — `quality >= 2.0.0` (или `(?)`).
8. Публикация: Mod Portal → «My Mods» → Upload (.zip), обязательно `thumbnail.png` 512×512; статус «Internal» для себя, потом «public»; портал проверяет `factorio_version`/`dependencies`.
9. Автоматизация: **github.com/fgardt/factorio-mod-template** — GitHub Actions: токен API (права Upload/Edit/Publish) → автосборка и заливка новых версий при git-теге.

### 7.3 Правила/этика (портал, кратко)

- Корректная лицензия; нельзя использовать чужие ассеты без разрешения (Wube-ассеты — собственность Wube; многие моддеры берут за основу «тинтированные» версии ванильных спрайтов — это серая зона, лучше рендерить свои или брать из **Factorio Assets** — каталога с пермиссивными лицензиями, см. The Foundry).
- Имя/иконка/описание без «клона» чужих модов; указывай зависимости честно; не пиши «спойлеры» в описании, если мод скрывает контент.

---

## 8. Ключевые неофициальные ресурсы (проверены)

| Ресурс | Что даёт |
|---|---|
| **The Foundry** (foundrygg.com) | сообщество мод-разработчиков, блог, шаблон мода, каталог ассетов (Factorio Assets), Discord |
| **PlanetsLib** (github.com/danielmartin0/PlanetsLib, mods.factorio.com/mod/PlanetsLib, MIT) | библиотека планет/лун/систем: орбитальные деревья, варианты сущностей, генерация |
| **factorio-2.0-mod-porting-guide** (github.com/tburrows13/factorio-2.0-mod-porting-guide) | самый полный неофициальный гайд портирования 1.1 → 2.0 (включая `2.0-changelog-filtered.md` и скрипты удаления/переименования HR-файлов) |
| **factorio-mod-template** (github.com/fgardt/factorio-mod-template) | шаблон репо с Actions-релизом на портал |
| **factorio-spritter** (github.com/fgardt/factorio-spritter) | CLI сборки спрайт-шитов с Lua-выводом |
| **blender-factorio-utils** (github.com/AshenHermit/blender-factorio-utils) | Blender-аддон: сцена + рендеры + генерация Lua |
| **Spritify** (форум t=5336; blender_spritify от jmattspartacus) | классика для спрайт-шитов из Blender |
| **FMTK** (marketplace.visualstudio.com, justarandomgeek.factoriomod-debug) | VSCode-инструмент (отладка, дополнение) |
| **r/factorio** + **r/technicalfactorio** | все обсуждения патчей, фичи-запросы, фиксы; поток «Version 2.0.x» сразу после каждого релиза |
| **patched.gg / patchtracker.gg / soren.com** | агрегаторы патчноутов (удобно следить за стабильными/экспериментальными переходами) |
| **NamuWiki (Factorio/Обновление)** | подробная хронология 2.0/2.1 на корейском |
| **Steam News / Community Hub** | официальные посты о релизах и гайдах |
| **Discord** | официальный Discord Wube (каналы #mod-dev-guide, #modding-help, #modding-discussion) и сервер The Foundry |
| **Aweird Imagination** (aweirdimagination.net, «A Newbie's Introduction to Factorio Modding») | отличный вводный туториал от коммьюнити |

---

## 9. Мой план: как именно я буду делать твои моды

### 9.1 Принципы

1. **Сначала — спецификация и «карта» мода** (что добавляем, масштаб, зависимости, версия-таргет — сейчас разумно целиться в **2.0.x** (стабильная ветка), и параллельно проверять совместимость с 2.1, т.к. движок уже обновился экспериментально; если мод для SA — обязательно `space-age >= 2.0.0`).
2. **Максимум переиспользования официального кода**: ванильные прототипы из `wube/factorio-data` как эталон (это официальный «учебник»), `meld()` и `util` из `core/lualib`, паттерны `space-age`, `quality`, `elevated-rails`.
3. **Разделение data / control / графика**: прототипы в `prototypes/*.lua`, runtime в `control` (с `event_handler`-паттерном), ассеты — отдельные пайплайны (Blender → spritter), чтобы можно было перегенерировать арт без правки кода.
4. **Автоматизация через git-репозиторий**: вот как будет выглядеть структура работы в твоём GitHub-репо (по готовности создам по такому шаблону, когда скажешь делать конкретный мод):

```
factoriomodstest2/
├── README.md
├── docs/                      ← сейчас здесь: отчёты, ченджлоги, ссылки
├── mods/
│   └── <имя-мода>/
│       ├── info.json
│       ├── changelog.txt
│       ├── settings.lua
│       ├── data.lua / data-updates.lua / data-final-fixes.lua
│       ├── control.lua
│       ├── locale/{en,ru}/*.cfg
│       ├── prototypes/
│       ├── graphics/          ← готовые PNG-шиты
│       ├── sound/
│       ├── migrations/
│       └── thumbnails/thumbnail.png
├── art/                       ← исходники: .blend, рендер-скрипты, концепты, плитки
│   ├── blender/<entities>/*.blend
│   └── render/ (скрипты, факторные output)
├── scripts/                   ← spritter-команды, рендер-скрипты python, сборка шитов
├── tests/                     ← smoke-тесты запуска (headless), чек-листы
└── .github/workflows/release.yml   ← автосборка+выгрузка на Mod Portal по тегам
```

5. **Итерации с проверкой в игре**: каждый шаг запускаем `--mod-directory`, смотрим логи, правим; перед релизом — чек-лист (см. §7.2).

### 9.2 Конкретный порядок работы над любым модом

**Этап A — Исследование (1–3 дня меньше):** собрать требования (что за мод: контентный? QoL? Overhaul? планета?), найти ванильные аналоги, решить: base-only или SA, нужна ли quality-интеграция, какие прототипы переиспользовать.

**Этап B — Прототип «на бумаге»:** список сущностей/предметов/рецептов/технологий, баланс-прикидка (стоимость, скорость, науки), зависимости, названия-схема (`my-mod-*`), порядки в GUI (subgroup/order), тексты (ru/en).

**Этап C — Data-этап:** пишу `prototypes/entity.lua`, `item.lua`, `recipe.lua`, `technology.lua`, `fluid.lua`, `signal.lua` (если нужны), настройки. Проверка: чистый запуск, `-validate`-эквивалент (у Factorio нет `--validate` для модов — проверяю запуском с подгрузкой), визуально в editor (`/editor`), тултипы сущностей.

**Этап D — Логика:** `control.lua` с `on_init/on_load`, события, кастом-ивенты, GUI (если нужно), `remote.add_interface` для интеграции, миграции.

**Этап E — Арт:** 
- для простых предметов — генерирую иконку (AI-концепт → доводка в Aseprite/Krita; или чистый пиксель-арт в стиле ванилы),
- для машин — Blender-модель (я строю базовую геометрию, настраиваю орто-камеру/свет, NLA-анимации), рендерю 4/8/16 направлений × кадры, собираю шиты `factorio-spritter` (с `--lua`, `--tile-resolution`, `--scale`), вписываю в прототип.
- звуки — беру лицензионные/генерю простые (синтез/семплы с CC0), OGG, `advanced_volume_control`.

**Этап F — Локализация:** `locale/en`, `locale/ru` (все ключи), проверка `check_prototype_translations`.

**Этап G — Тесты:** headless-сервер + сценарий-смоук (прописать предметы/построить), проверка совместимости с чистым 2.0.76 и с SA, мультиплеер-десинк-тест (если мод интерактивный), производительность (`/perf`, тик-стоимость).

**Этап H — Публикация:** репо → CI Actions (токен портала) → версия `x.y.z` → тег → заливка; `changelog.txt`, описание, скриншоты, thumbnail 512.

### 9.3 Что мне нужно от тебя для старта (когда решишь делать конкретный мод)

1. **Идея** (1–2 предложения) или выбор из каталога (контентный/QoL/overhaul/планета).
2. **Таргет:** vanilla 2.0.x (стабильная), с Space Age, с Quality, или «как можно базовая».
3. **Масштаб:** один предмет/рецепт, набор зданий, новая планета, целый overhaul.
4. **Стиль графики:** «ванильный» пиксель-арт/рендер или своя эстетика; есть ли референсы.
5. **Права:** твои ассеты или можно использовать CC0/лицензионно-свободные; имя мода, авторство, лицензия.
6. **Готовность к публикации** на Mod Portal (аккаунт, API-токен для CI) или мод только для себя.

### 9.4 Что я точно умею/сделаю (чтобы было ясно)

- Написать полностью рабочий мод под 2.0.x: все файлы, прототипы, `info.json`, локали, миграции, `control.lua`.
- Собрать **графику**: спроектировать и сгенерировать спрайты/иконки (AI-генерация концептов + пиксельная доводка + рендер-пайплайн), собрать шиты, написать описания анимаций, проверить в игре.
- Построить **3D-пайплайн** (Blender-сцена, орто-камера, повороты 4/8/16, NLA-анимации, рендер, spritter) — то есть «3D-модели и анимации» для Factorio именно так и делаются, и я это автоматизирую.
- Настроить **CI/CD**: Actions → Mod Portal, авто-сбор zip, автологика changelog.
- Держать **совместимость**: следить за патчами (2.0.77, 2.1.x), обновлять мод по ченджлогам API (`modding-scripting-API-изменения-2.0.md`).

### 9.5 Ограничения, о которых честно предупреждаю

- **3D в реальном времени для модов недоступен** — только пререндер в спрайты. Никаких собственных шейдеров/геометрии в рантайме (только встроенные эффекты: `blend_mode`, маски, света, декали).
- **AI-генерация изображений даёт концепты, но не даёт готовые игровые шиты** нужной точности (пиксель-перфект, сетка, прозрачность, 16 направлений) — их я буду доводить/рендерить и автоматически склеивать.
- **Локальная проверка в игре на моей стороне ограничена** — в сандбоксе нет установленного Factorio/Steam-версии; тест-цикл «мод → запуск игры → правка» я смогу частью автоматизировать (headless-бинарник можно скачать, он бесплатный!), а финальные визуальные проверки — на твоей машине/скриншотах.
- Лицензии: если мод публичный, ассеты должны быть чистыми; ванильные PNG использовать в новых прототипах можно как основу только в рамках лицензии Wube (для личного использования — ок, для публикации — соблюдай правила портала; безопасный путь — свои ассеты или Factorio Assets).

---

## 10. Что важно знать про 2.0.77 и ветку 2.1 (влияет на будущие моды)

- **2.0.77** (21.05.2026, стабильная с 23.06.2026): фиксы + quality-чтения API (`crafting_speed_quality_multiplier`, `energy_usage_quality_multiplier`, `module_slots_quality_bonus`, `quality_affects_*`, `drops_full_belt_stacks`), `visualization_color` для жидкостей, полный текст-поиск в API-доках.
- **2.1.0 Experimental** (26.06.2026, FFF-444): **переработанные графический и аудио-пайплайны**, SDL3, новые требования к ОС (Linux/macOS), сейвы 2.0 совместимы (но нельзя откатиться), первый контент-дроп «2.1» (правки хабов, рециклер-отдельный мод, `chain_probability` в quality, `PumpPrototype::{fluid_wagon_tank_valve_max_distance,...}`, `can_launch_without_landing_pads`-фиксы и т.д. — см. `Version_history/2.1.0`).
- **Совет:** новые моды пишу под `base >= 2.0.0`, тестирую на 2.0.77 (стабильная) и держу в уме 2.1 (для публикации в 2.1 достаточно поднять версию зависимостей после проверки; большинство API-изменений — добавления, ломающих немного).

---

## 11. Ссылки (быстрый доступ)

**Официальные:**
- factorio.com · factorio.com/blog · factorio.com/download/experimental · factorio.com/galaxy
- forums.factorio.com (разделы: Announcements/News, Modding help, Modding interface requests, Bug reports)
- wiki.factorio.com (Version_history, Tutorial:Modding_tutorial, Mod_structure, Prototype_definitions, Data_lifecycle, Factoriopedia, Friday_Facts)
- lua-api.factorio.com/latest/ (и /2.0.76/, JSON: runtime-api.json, prototype-api.json, index-prototype.html, json-docs.html)
- github.com/wube/factorio-data (прототипы+changelog по тегам)
- mods.factorio.com · mod portal API v2
- официальный Discord Wube (ссылка на сайте)

**Неофициальные:**
- github.com/tburrows13/factorio-2.0-mod-porting-guide
- github.com/fgardt/factorio-mod-template · github.com/fgardt/factorio-spritter
- github.com/AshenHermit/blender-factorio-utils · github.com/jmattspartacus/blender_spritify
- github.com/danielmartin0/PlanetsLib · mods.factorio.com/mod/PlanetsLib
- foundrygg.com (Discord + Factorio Assets + шаблон)
- reddit.com/r/factorio · r/technicalfactorio
- patched.gg/games/factorio · patchtracker.gg/factorio · soren.com
- en.namu.wiki (Factorio/Update)
- aweirdimagination.net (Newbie's Introduction to Factorio Modding)

---

*Отчёт подготовлен по состоянию на 28.08.2026. Полные официальные ченджлоги 2.0.7–2.0.76 (дословно, 70 версий) — в `docs/changelogs/полный-официальный-ченджлог-2.0.7-2.0.76.md`; выжимка всех изменений Modding/Scripting по версиям — в `docs/changelogs/modding-scripting-API-изменения-2.0.md`.*
