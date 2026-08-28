-- Fish Furnace item (placeable building).

data:extend(
{
  {
    type = "item",
    name = "fish-furnace",
    icon = "__fish-furnace__/graphics/icons/fish-furnace.png",
    icon_size = 128,
    subgroup = "smelting-machine",
    order = "a[fish-furnace]",
    inventory_move_sound = { filename = "__base__/sound/item/brick-inventory-move.ogg" },
    pick_sound = { filename = "__base__/sound/item/brick-inventory-pickup.ogg" },
    drop_sound = { filename = "__base__/sound/item/brick-inventory-move.ogg" },
    place_result = "fish-furnace",
    stack_size = 50
  }
})
