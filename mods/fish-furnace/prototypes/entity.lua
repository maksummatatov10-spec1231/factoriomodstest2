-- Fish Furnace — entity prototype (furnace) + corpse remnant.
-- Mirrors the vanilla stone-furnace definition, adjusted: 4x crafting speed,
-- higher energy usage, fish graphics.

require("util")

-- circuit connector definitions are global after base data stage
if not circuit_connector_definitions then
  require("__core__.lualib.circuit-connector-sprites")
end

data:extend(
{
  {
    type = "furnace",
    name = "fish-furnace",
    icon = "__fish-furnace__/graphics/icons/fish-furnace.png",
    icon_size = 128,
    flags = {"placeable-neutral", "placeable-player", "player-creation"},
    minable = {mining_time = 0.2, result = "fish-furnace"},
    fast_replaceable_group = "furnace",
    next_upgrade = "steel-furnace",
    circuit_wire_max_distance = 9,
    circuit_connector = circuit_connector_definitions["stone-furnace"],
    max_health = 200,
    corpse = "fish-furnace-remnants",
    dying_explosion = "stone-furnace-explosion",
    repair_sound = { filename = "__base__/sound/manual-repair.ogg" },
    mined_sound = { filename = "__base__/sound/deconstruct-bricks.ogg", volume = 0.8 },
    open_sound = { filename = "__base__/sound/machine-open.ogg" },
    close_sound = { filename = "__base__/sound/machine-close.ogg" },
    allowed_effects = {"speed", "consumption", "pollution"},
    effect_receiver = {
      uses_module_effects = false,
      uses_beacon_effects = false,
      uses_surface_effects = true
    },
    impact_category = "stone",
    icon_draw_specification = {scale = 0.66, shift = {0, -0.1}},
    working_sound =
    {
      sound =
      {
        filename = "__base__/sound/furnace.ogg",
        volume = 0.6,
        audible_distance_modifier = 0.4
      },
      fade_in_ticks = 4,
      fade_out_ticks = 20
    },
    resistances =
    {
      { type = "fire", percent = 90 },
      { type = "explosion", percent = 30 },
      { type = "impact", percent = 30 }
    },
    collision_box = {{-0.7, -0.7}, {0.7, 0.7}},
    selection_box = {{-0.8, -1}, {0.8, 1}},
    damaged_trigger_effect =
    {
      type = "direct",
      action_delivery =
      {
        type = "instant",
        source_effects =
        {
          {
            type = "create-particle",
            repeat_count = 1,
            particle_name = "stone-particle",
            initial_speed = 0.5,
            initial_height = 1,
            offset_deviation = {{-0.3, -0.3}, {0.3, 0.3}}
          }
        }
      }
    },
    crafting_categories = {"smelting"},
    result_inventory_size = 1,
    energy_usage = "360kW",
    crafting_speed = 4,
    source_inventory_size = 1,
    energy_source =
    {
      type = "burner",
      fuel_categories = {"chemical"},
      effectivity = 1,
      fuel_inventory_size = 1,
      emissions_per_minute = { pollution = 8 },
      light_flicker =
      {
        color = {0, 0, 0},
        minimum_intensity = 0.6,
        maximum_intensity = 0.95
      },
      smoke =
      {
        {
          name = "smoke",
          deviation = {0.1, 0.1},
          frequency = 5,
          position = {0.0, -0.8},
          starting_vertical_speed = 0.08,
          starting_frame_deviation = 60
        }
      }
    },
    graphics_set =
    {
      animation =
      {
        layers =
        {
          {
            filename = "__fish-furnace__/graphics/entity/fish-furnace/fish-furnace.png",
            priority = "extra-high",
            width = 302,
            height = 292,
            frame_count = 2,
            shift = util.by_pixel(-0.25, 6),
            scale = 0.5
          },
          {
            filename = "__fish-furnace__/graphics/entity/fish-furnace/fish-furnace-shadow.png",
            priority = "extra-high",
            width = 328,
            height = 148,
            draw_as_shadow = true,
            shift = util.by_pixel(14.5, 13),
            scale = 0.5
          }
        }
      },
      working_visualisations =
      {
        {
          fadeout = true,
          effect = "flicker",
          animation =
          {
            layers =
            {
              {
                filename = "__fish-furnace__/graphics/entity/fish-furnace/fish-furnace-fire.png",
                priority = "extra-high",
                line_length = 8,
                width = 82,
                height = 200,
                frame_count = 48,
                draw_as_glow = true,
                shift = util.by_pixel(0, 15),
                scale = 0.5
              },
              {
                filename = "__fish-furnace__/graphics/entity/fish-furnace/fish-furnace-light.png",
                blend_mode = "additive",
                width = 212,
                height = 288,
                repeat_count = 48,
                draw_as_glow = true,
                shift = util.by_pixel(0, 8),
                scale = 0.5
              }
            }
          }
        },
        {
          fadeout = true,
          effect = "flicker",
          animation =
          {
            filename = "__fish-furnace__/graphics/entity/fish-furnace/fish-furnace-ground-light.png",
            blend_mode = "additive",
            width = 232,
            height = 220,
            repeat_count = 48,
            draw_as_light = true,
            shift = util.by_pixel(-1, 44),
            scale = 0.5
          }
        }
      },
      water_reflection =
      {
        pictures =
        {
          filename = "__fish-furnace__/graphics/entity/fish-furnace/fish-furnace-reflection.png",
          priority = "extra-high",
          width = 16,
          height = 16,
          shift = util.by_pixel(0, 35),
          variation_count = 1,
          scale = 5
        },
        rotate = false,
        orientation_to_variation = false
      }
    }
  },
  {
    type = "corpse",
    name = "fish-furnace-remnants",
    icon = "__fish-furnace__/graphics/icons/fish-furnace.png",
    icon_size = 128,
    flags = {"placeable-neutral", "building-direction-8-way", "not-on-map"},
    hidden_in_factoriopedia = true,
    subgroup = "smelting-machine-remnants",
    order = "a-a-a",
    selection_box = {{-1, -1}, {1, 1}},
    tile_width = 2,
    tile_height = 2,
    selectable_in_game = false,
    time_before_removed = 60 * 60 * 15, -- 15 minutes
    expires = false,
    final_render_layer = "remnants",
    remove_on_tile_placement = false,
    animation =
    {
      {
        filename = "__fish-furnace__/graphics/entity/fish-furnace/remnants/fish-furnace-remnants.png",
        line_length = 1,
        width = 302,
        height = 292,
        direction_count = 1,
        frame_count = 1,
        shift = util.by_pixel(0, 9.5),
        scale = 0.5
      }
    }
  }
})
