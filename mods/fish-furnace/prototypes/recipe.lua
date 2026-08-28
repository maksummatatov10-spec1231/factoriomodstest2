-- Fish Furnace recipe: 50 raw fish. Crafted by hand or in an assembling machine
-- (category "crafting"), unlocked by the fish-furnace technology.

data:extend(
{
  {
    type = "recipe",
    name = "fish-furnace",
    ingredients = {{type = "item", name = "raw-fish", amount = 50}},
    results = {{type = "item", name = "fish-furnace", amount = 1}},
    enabled = false
  }
})
