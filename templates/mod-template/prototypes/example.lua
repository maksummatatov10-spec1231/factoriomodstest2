-- Пример прототипа (замени на свой).
-- Правила (см. docs/моддинг-уроки-и-недочёты.md):
--  * все типы/поля — из официальных доков 2.0.76;
--  * shift/scale — от ванильного аналога (экранный размер = файл × scale);
--  * frame_count одинаковый во всех слоях анимации (повтор — repeat_count);
--  * пути к звукам/графике — только существующие файлы.

data:extend({
  {
    type = "item",
    name = "{{MOD_NAME}}-example",
    icon = "__{{MOD_NAME}}__/graphics/icons/{{MOD_NAME}}-example.png",
    icon_size = 64,
    subgroup = "intermediate-product",
    order = "z[{{MOD_NAME}}]",
    stack_size = 50
  }
})
