-- Fish Furnace technology: 1 red science pack in a lab.

data:extend(
{
  {
    type = "technology",
    name = "fish-furnace",
    icon = "__fish-furnace__/graphics/icons/fish-furnace-tech.png",
    icon_size = 128,
    effects =
    {
      {type = "unlock-recipe", recipe = "fish-furnace"}
    },
    prerequisites = {"automation"},
    unit =
    {
      count = 1,
      ingredients = {{"automation-science-pack", 1}},
      time = 2,
      researching_speed = 1
    },
    order = "a-a",
    upgrade = false,
    max_level = 1
  }
})
