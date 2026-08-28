# Изменения Modding/Scripting API по версиям 2.0.7–2.0.76

> Автоматически выбрано из официального changelog.txt (wube/factorio-data). Это то, что реально влияет на моды.


## 2.0.76 (25. 02. 2026)

- **Scripting:** Added LuaEntityPrototype::reversing_power_modifier read.

## 2.0.75 (12. 02. 2026)

- **Modding:** space-age, quality and elevated-rails mod versions were not bumped for this update as nothing has changed.

## 2.0.74 (10. 02. 2026)

- **Modding:** space-age, quality and elevated-rails mod versions were not bumped for this update as nothing has changed.
- **Scripting:** Added LuaEntityPrototype::inserter_max_belt_stack_size read.
- **Scripting:** Changed LuaEntityPrototype::automated_ammo_count read to also work for artillery wagons.

## 2.0.73 (13. 01. 2026)

- **Scripting:** Added LuaEntity::send_to_orbit_automatically read/write.

## 2.0.72 (22. 10. 2025)


## 2.0.71 (16. 10. 2025)


## 2.0.70 (13. 10. 2025)

- **Modding:** Added CargoStationParameters::is_input_station and ::is_output_station to mainly clarify tooltips. (126749)

## 2.0.69 (29. 09. 2025)

- **Modding:** Added MiningDrillPrototype::resource_searching_offset.
- **Modding:** Added "scripted" technology trigger.
- **Modding:** Added FluidWagonPrototype::connection_category.
- **Scripting:** Added on_player_dropped_item_into_entity event.
- **Scripting:** Added LuaItemCommon::entity_logistics_enabled and entity_enable_logistics_while_moving read/write.
- **Scripting:** Added LuaItemCommon::entity_driver_is_gunner, entity_auto_target_without_gunner and entity_auto_target_with_gunner read/write.
- **Scripting:** Added maximum_quality_jump utility constant.
- **Scripting:** Added LuaEntity::mining_area read.
- **Scripting:** Added LuaForce::script_trigger_research().

## 2.0.68 (23. 09. 2025)


## 2.0.67 (22. 09. 2025)

- **Modding:** Removed "research-progress" product type from RecipePrototype.
- **Modding:** Added RobotWithLogisticInterfacePrototype::max_payload_size_after_bonus.
- **Modding:** Added FusionGeneratorPrototype::burns_fluid.
- **Modding:** Added FusionGeneratorPrototype::effectivity.
- **Modding:** Changed Generator and FusionGenenerator tooltips to not show temperatures when in burns_fluid mode.
- **Modding:** Added support for heating_energy to FusionGeneratorPrototype and ThrusterPrototype.
- **Modding:** Added recipe_icon_scale chart utility constant.
- **Modding:** Added LightningPrototype::attractor_hit_effect.
- **Modding:** Added RoboportPrototype::render_recharge_icon.
- **Modding:** Changed CargoWagonPrototype to use EntityPrototype::icon_draw_specification when drawing cargo wagon content.
- **Modding:** Changed DisplayPanelPrototype to use render_layer from icon_draw_specification when drawing icon.
- **Modding:** Added __TECHNOLOGY__ and __RECIPE__ built-in locale parameters.
- **Scripting:** Added LuaPlayer::get_recipe_notifications().
- **Scripting:** Added LuaPlayer::swap_characters().
- **Scripting:** Added flip_horizontal and flip_vertical parameters to LuaPlayer::build_from_cursor().
- **Scripting:** Added skip_fog_of_war to LuaPlayer::can_build_from_cursor().
- **Scripting:** Added LuaCustomChartTag::position and surface write.
- **Scripting:** Added LuaFluidBox::get_fluid_segment_extent_bounding_box().
- **Scripting:** Added LuaItemPrototype::get_module_effects().
- **Scripting:** Added LuaInventory::get_item_count_filtered().
- **Scripting:** Added LuaInventory::get_item_quality_counts().
- **Scripting:** Added LuaLogisticNetwork::custom_name read/write.
- **Scripting:** Added LuaRecord::export_record().
- **Scripting:** Added LuaRecord::get_selected_record().
- **Scripting:** Added LuaEntity::transitional_request_target read.
- **Scripting:** Added LuaEntity::rail_length read.
- **Scripting:** Added LuaEntity::get_movement() and set_movement().
- **Scripting:** Added LuaHelpers::multilingual_to_lower().
- **Scripting:** Added LuaEntityPrototype::get_attraction_range_elongation() and get_energy_distribution_efficiency().
- **Scripting:** Added LuaEntityPrototype::fluid_buffer_size, activation_buffer_ratio and fluid_buffer_input_flow read.
- **Scripting:** Added LuaEntityPrototype::spider_engine read.
- **Scripting:** Added LuaEntityPrototype::range_from_player, combat_robot_friction, destroy_action and follows_player read.
- **Scripting:** Added LuaEntityPrototype::strike_effect, attractor_hit_effect, damage and energy read.
- **Scripting:** Added LuaEntityPrototype::support_range read.
- **Scripting:** Added LuaGuiElement::icon_selector read.
- **Scripting:** Added LuaItemCommon::entity_logistic_sections and entity_request_from_buffers read/write.
- **Scripting:** Added custom_tooltip_fields reads to all LuaPrototypes that support it.
- **Scripting:** Added on_cargo_pod_started_ascending event.
- **Scripting:** Added previous_target and previous_quality to on_marked_for_upgrade event.
- **Scripting:** Added in_gui to custom input events.
- **Scripting:** Added LuaSplitterControlBehavior.
- **Scripting:** Added surface_index to all UndoRedoActions.
- **Scripting:** Changed LuaSpacePlatform::destroy_asteroid_chunks() to return the number of destroyed chunks.
- **Scripting:** Changed LuaEntity::color read/write to also work for character corpses.

## 2.0.66 (02. 09. 2025)

- **Modding:** Added color mod setting "forced_value".
- **Modding:** InserterPrototype::pickup_position and insert_position are no longer checked for being too close to tile edge.
- **Scripting:** Added an "overflow" inventory option to LuaEntity::revive and silent_revive.
- **Scripting:** Added LuaEntityPrototype::icons_positioning and icon_draw_specification read.
- **Scripting:** Added LuaRenderObject::dash_offset read/write.
- **Scripting:** Added tile_condition to LuaItemPrototype::place_as_tile_result.
- **Scripting:** Changed LuaAchievementPrototype::to_kill and module to returns arrays of LuaPrototypes instead of arrays of strings.
- **Scripting:** Added LuaRecord::is_preview read.
- **Scripting:** Added LuaGameScript::allow_debug_settings read/write.

## 2.0.65 (22. 08. 2025)

- **Modding:** Heat energy sources support pollution.
- **Modding:** Omitting required_tiles in a tile_buildability_rules's item now default to "all" (instead of "none" which was making the entities unbuildable) (130230)
- **Modding:** Added EntityPrototype::draw_stateless_visualisations_in_ghost.
- **Modding:** Added LoaderPrototype::respect_insert_limits.
- **Scripting:** Changed LuaParticlePrototype::render_layer, render_layer_when_on_ground and LuaTrivialSmokePrototype::render_layer to be strings instead of integers.

## 2.0.64 (12. 08. 2025)

- **Scripting:** Added LuaItemCommon::blueprint_description read/write.
- **Scripting:** Added LuaRecord::blueprint_description read/write.
- **Scripting:** Added LuaControl::render_position read.
- **Scripting:** Added LuaControl::flight_height read.
- **Scripting:** Added LuaControl::is_flying read.
- **Scripting:** Added LuaEntity::created_by_corpse read.
- **Scripting:** Added heat pipe to LuaEntity::neighbours read.
- **Scripting:** Added LuaEntity::heat_neighbours read.
- **Scripting:** Added LuaPlanet::get_space_platforms().
- **Scripting:** Added LuaEntity::priority_targets read.

## 2.0.63 (04. 08. 2025)


## 2.0.62 (31. 07. 2025)


## 2.0.61 (30. 07. 2025)

- **Modding:** Added RecipePrototype::hide_from_bonus_gui.
- **Modding:** Changed pentapods to prioritize using the torso base sprite to control rotations, or if no base sprite is defined, the head sprite is used.
- **Modding:** Added ability for SpiderVehicles to rotate their legs like pentapods when provided with a base sprite that has rotation frames. (128638)
- **Modding:** Added SpaceLocationPrototype::starmap_icon_orientation.
- **Scripting:** Added demolisher and territory API.
- **Scripting:** Moved LuaPlayer::can_place_entity to LuaControl::can_place_entity so that it can be called on character entities. (129225)
- **Scripting:** Added LuaPlayer::set_zoom_limits() to set zoom limits for any controller type. (128887)
- **Scripting:** Added LuaForce::get_chunk_chart(surface, position).
- **Scripting:** Added LuaEntity::apply_upgrade().
- **Scripting:** Added LuaEntity::pumped_last_tick read.
- **Scripting:** Added LuaEntityPrototype::tile_buildability_rules read.
- **Scripting:** Added agricultural tower events: on_tower_planted_seed, on_tower_pre_mined_plant, and on_tower_mined_plant.
- **Scripting:** Changed LuaEntity::copy_color_from_train_stop and vehicle_automatic_targeting_parameters to work on ghosts.
- **Scripting:** Added LuaEntity::register_tree().
- **Scripting:** Added register_plant to LuaSurface::create_entity.

## 2.0.60 (10. 07. 2025)


## 2.0.59 (09. 07. 2025)

- **Modding:** Added InserterPrototype::uses_inserter_stack_size_bonus.
- **Modding:** Added Prototype::custom_tooltip_fields.
- **Modding:** Renamed "aquilo-4-hero" ambient-sound to "aquilo-3-hero", corresponding audio file was renamed as well.
- **Scripting:** Added LuaPlayer::pipette. LuaPlayer::pipette_entity is deprecated and should not be used.
- **Scripting:** Added ConfigurationChangedData::migrations.
- **Scripting:** Added "item-open", "item-close", "item-pick", "item-drop" and "item-move" SoundPath types. (129710)
- **Scripting:** Removed LuaTilePrototype::placeable_by. Use LuaTilePrototype::items_to_place_this instead.
- **Scripting:** Added LuaEquipmentGrid::itemstack_owner read.
- **Scripting:** Added LuaEntity::display_panel_text, display_panel_icon, display_panel_always_show and display_panel_show_in_chart read/write.
- **Scripting:** Added LuaHelpers::send_udp and recv_udp. Added on_udp_packet_received.

## 2.0.58 (23. 06. 2025)

- **Modding:** Added the "mod-data" prototype type.
- **Modding:** Added CraftingMachinePrototype::crafting_speed_quality_multiplier, module_slots_quality_bonus and energy_usage_quality_multiplier.
- **Scripting:** Added LuaEntityPrototype::neighbour_connectable read.

## 2.0.57 (19. 06. 2025)


## 2.0.56 (19. 06. 2025)

- **Modding:** Added `with_filters`, `with_weight_limit` and `with_custom_stack_size` options to ContainerPrototype::inventory_type and LinkedContainerPrototype::inventory_type.
- **Modding:** Added LoaderPrototype::wait_for_full_stack.
- **Modding:** Added QualityPrototype::default_multiplier, inserter_speed_multiplier, fluid_wagon_capacity_multiplier, inventory_size_multiplier, lab_research_speed_multiplier, crafting_machine_speed_multiplier, crafting_machine_energy_usage_multiplier, logistic_cell_charging_energy_multiplier, tool_durability_multiplier, accumulator_capacity_multiplier, flying_robot_max_energy_multiplier, range_multiplier, asteroid_collector_collection_radius_bonus, equipment_grid_width_bonus, equipment_grid_height_bonus, electric_pole_wire_reach_bonus, electric_pole_supply_area_distance_bonus, beacon_supply_area_distance_bonus, logistic_cell_charging_station_count_bonus, beacon_module_slots_bonus, crafting_machine_module_slots_bonus, mining_drill_module_slots_bonus, mining_drill_mining_radius_bonus and lab_module_slots_bonus.
- **Modding:** Added `quality_selector_dropdown_threshold` utility constant.
- **Modding:** Added CraftingMachinePrototype::quality_affects_energy_usage.
- **Modding:** Added MiningDrillPrototype::quality_affects_mining_radius.
- **Modding:** Added BeaconPrototype::quality_affects_supply_area_distance.
- **Modding:** Added CraftingMachinePrototype::quality_affects_module_slots, LabPrototype::quality_affects_module_slots, MiningDrillPrototype::quality_affects_module_slots and BeaconPrototype::quality_affects_module_slots.
- **Modding:** Added CharacterPrototype::crafting_speed.
- **Scripting:** Added LuaAsteroidChunkPrototype::dying_trigger_effect read.
- **Scripting:** Added LuaItemPrototype::send_to_orbit_mode read.
- **Scripting:** Added LuaEntityPrototype::captured_spawner_entity read.
- **Scripting:** Added LuaEntityPrototype::min_performance read.
- **Scripting:** Added LuaEntityPrototype::max_performance read.
- **Scripting:** Added target_filter to ammo type read.
- **Scripting:** Added LuaInventory::weight and max_weight read.
- **Scripting:** Added LuaEntity::pickup_from_left_lane and pickup_from_right_lane read/write for inserters.
- **Scripting:** Added ghost_mode to LuaGuiElement::anchor.
- **Scripting:** Added LuaPlayer::exit_remote_view().
- **Scripting:** Added "blink_interval" and "render_mode" parameters to LuaRendering functions.
- **Scripting:** Added LuaRenderObject::blink_interval and render_mode read/write.
- **Scripting:** Added several LuaEntityPrototype reads for asteroid collector prototypes and entity with health prototypes.
- **Scripting:** Added several LuaItemPrototype reads for starter pack prototypes.
- **Scripting:** Added LuaForce::get_logistic_groups(), get_logistic_group(), create_logistic_group(), and delete_logistic_group().
- **Scripting:** Added on_research_queued.
- **Scripting:** Added player to on_research_moved and on on_research_cancelled.
- **Scripting:** Added fusion reactor properties to LuaEntityPrototype.
- **Scripting:** Added LuaSurface get_default_cover_tile() and set_default_cover_tile().
- **Scripting:** Added CustomInputEvent::element to get the LuaGuiElement under the cursor when the custom input was activated.
- **Scripting:** Changed LuaInventory::set_bar to allow passing nil as well.
- **Scripting:** Added LuaPrototypes::utility_constants read.
- **Scripting:** Added LuaEntityPrototype::get_fluid_capacity().
- **Scripting:** Added force to LuaEntityDiedEventFilter.
- **Scripting:** Added LuaSpacePlatform::hidden read/write.
- **Scripting:** LuaGuiElement::locked can be set during add().
- **Scripting:** Added LuaEntity::inventory_supports_bar(), get_inventory_bar(), set_inventory_bar(), inventory_supports_filters(), is_inventory_filtered(),

## 2.0.55 (02. 06. 2025)

- **Modding:** Added `helpers` to settings and prototype stages.
- **Scripting:** Added LuaHelpers::game_version read.
- **Scripting:** Added LuaHelpers::compare_versions().

## 2.0.54 (30. 05. 2025)


## 2.0.53 (30. 05. 2025)

- **Modding:** Added utility constants logistic_slots_per_row, crafting_queue_slots_per_row, blueprint_big_slots_per_row, blueprint_small_slots_per_row, and trash_inventory_width.
- **Modding:** Added LandMinePrototype::trigger_interval.
- **Modding:** Added SolarPanelEquipmentPrototype::performance_at_day, performance_at_night and solar_coefficient_property.
- **Scripting:** Changed LuaEntity::set_passenger() to work with cargo pods.
- **Scripting:** Changed LuaLogisticSection::set_slot() to return the existing conflicting slot (if one exists) instead of erroring.

## 2.0.52 (23. 05. 2025)

- **Modding:** Added ItemPrototype::moved_to_hub_when_building.
- **Scripting:** Added LuaSchedule::get_inside_interrupt()/set_inside_interrupt().
- **Scripting:** Added `quality` to on_script_trigger_effect event when item spoils to script trigger.

## 2.0.51 (19. 05. 2025)

- **Scripting:** Added LuaSurface::spill_inventory.

## 2.0.50 (16. 05. 2025)

- **Scripting:** Added LuaEntity::set_inventory_size_override/get_inventory_size_override methods with support for container and cargo-wagon.
- **Scripting:** Added LuaEntity::crane_end_position_3d read for getting current ending position of agricultural crane. (128752)

## 2.0.49 (12. 05. 2025)

- **Modding:** Added AgriculturalTowerPrototype::randomize_planting_tile.
- **Modding:** Added RecipePrototype::additional_categories.
- **Scripting:** Added LuaEntity::owned_plants read.
- **Scripting:** Added LuaEntityPrototype::launch_to_space_platforms read.

## 2.0.48 (12. 05. 2025)

- **Modding:** Added the "valve" entity type.
- **Modding:** Added SolarPanelPrototype::performance_at_day, performance_at_night and solar_coefficient_property.
- **Modding:** Added LightningProperties::lightning_multiplier_at_day, lightning_multiplier_at_night, multiplier_surface_property and lightning_warning_icon.
- **Modding:** Added AgriculturalTowerPrototype::accepted_seeds.
- **Scripting:** Added LuaSpacePlatform::ejected_items read.
- **Scripting:** Added LuaSpacePlatform::eject_item().
- **Scripting:** Added LuaSpacePlatform::clear_ejected_items().
- **Scripting:** Added LuaEntity::valve_threshold_override read/write.
- **Scripting:** Added LuaEntityPrototype::valve_mode read, LuaEntityPrototype::valve_threshold read, and LuaEntityPrototype::get_valve_flow_rate(quality).
- **Scripting:** Added drop_full_stack parameter to LuaSurface::spill_item_stack.
- **Scripting:** Added character parameter to LuaEntity::launch_rocket.
- **Scripting:** Added LuaSurface::set_pollution.
- **Scripting:** Added defines.inventory.agricultural_tower_input and defines.inventory.agricultural_tower_output.
- **Scripting:** Added defines.inventory.linked_container_main, asteroid_collector_output, crafter_input, crafter_output, crafter_modules, crafter_trash, lab_trash.
- **Scripting:** Added LuaControl::get_inventory_name.
- **Scripting:** Added LuaInventory::name read.
- **Scripting:** Added LuaGuiElement::quality read/write for "sprite-button" type.
- **Scripting:** Added LuaEntity::cargo_bay_connection_owner read.
- **Scripting:** Added LuaEntity::use_transitional_requests read/write.
- **Scripting:** Added LuaEntityPrototype::fluid_source_offset.
- **Scripting:** Added LuaEntity::get_fluid_source_tile() and get_fluid_source_fluid().
- **Scripting:** Added LuaSurface::pollution_statistics read.
- **Scripting:** Added LuaSurface::global_electric_network_statistics read.
- **Scripting:** Added LuaSurface::daytime_parameters read/write.
- **Scripting:** Added LuaEntityPrototype::agricultural_tower_radius, crane_energy_usage and growth_area_radius read.
- **Scripting:** Changed on_space_platform_changed_state event to run after all starter pack actions are done when applying it and LuaSpacePlatform::hub is set.

## 2.0.47 (29. 04. 2025)


## 2.0.46 (29. 04. 2025)

- **Modding:** Added CarPrototype::rotation_snap_angle
- **Modding:** Instead of "enemy-bases" autoplace control being hardcoded to be the one to affect achievements, achievements are now affected by
- **Modding:** Fluid boxes with diagonal connections now throw a prototype error.
- **Scripting:** Added LuaEntity::item_request_proxy read as the recommended way to check for the presence of one.
- **Scripting:** Added optional amount to LuaItemStack::transfer_stack().
- **Scripting:** Added base_damage_modifiers and bonus_damage_modifiers when creating projectile types through LuaSurface::create_entity().
- **Scripting:** Added LuaEntity::base_damage_modifiers and bonus_damage_modifiers read/write.
- **Scripting:** Made LuaPlayer::zoom readable
- **Scripting:** Added LuaPlayer::zoom_limits
- **Scripting:** Added LuaTransportLine::total_segment_length.

## 2.0.45 (14. 04. 2025)

- **Modding:** Added MiningDrillPrototype::uses_force_mining_productivity_bonus.
- **Modding:** Added PumpPrototype::flow_scaling.

## 2.0.44 (07. 04. 2025)

- **Modding:** Added collision-layer out_of_map for out-of-map tiles.
- **Modding:** Decals now support draw_as_light and draw_as_glow.
- **Modding:** [space-age] Decals can now be masked by water if their layer is above UtilityConstants::capture_water_mask_at_layer, the tile effect has a lightmap_alpha of less than 1, and the decal has opacity_over_water less than 1. This is currently requires Space Age as the effect is not supported on Switch.
- **Modding:** Added FusionReactorPrototype::target_temperature.
- **Modding:** Added RocketSiloPrototype::can_launch_without_landing_pads.
- **Scripting:** Added support for fusion reactors to LuaEntityPrototype::target_temperature.
- **Scripting:** Added label, preview_distance and always_visible fields to LuaPlayer::add_pin.
- **Scripting:** The remote view controller now supports enabling and disabling flashlight.
- **Scripting:** Added LuaControl::open_factoriopedia_gui(...).
- **Scripting:** Added LuaControl::close_factoriopedia_gui().

## 2.0.43 (26. 03. 2025)

- **Modding:** Added AirbornePollutantPrototype::damages_trees.

## 2.0.42 (19. 03. 2025)

- **Modding:** Changed working_visualisations to enforce that the provided array is contiguous.
- **Modding:** Added FluidBoxPrototype::volume_reservation_fraction.
- **Modding:** Added ExplosionPrototype::delay and ExplosionPrototype::delay_deviation for adding an artificial delay to an explosion effect.
- **Modding:** Added ExplosionPrototype::explosion_effect which triggers after the delay has passed instead of when the explosion entity is created as with EntityPrototype::created_effect.
- **Modding:** Added TechnologyPrototype::show_levels_info.
- **Scripting:** LuaEntity::infinity_inventory_filters and remove_unfiltered_items now support infinity-cargo-wagon.
- **Scripting:** LuaControl::walking_state now reads and writes spider-vehicle walking state if the player is driving one.
- **Scripting:** Added LuaEntity::cargo_pod_origin which stores which station entity the pod departed from. (Migrated existing pods from before this version do NOT retroactively gain this information)
- **Scripting:** Added 'spoil-result' and 'plant-result' filter to ItemPrototypeFilters.

## 2.0.41 (12. 03. 2025)


## 2.0.40 (12. 03. 2025)

- **Modding:** Added ElectricPolePrototype::rewire_neighbours_when_destroying.
- **Modding:** Moved the agricultural tower growth area radius to the prototype as growth_area_radius. (127340)

## 2.0.39 (05. 03. 2025)


## 2.0.38 (04. 03. 2025)

- **Modding:** Added the "infinity-cargo-wagon" entity type.
- **Modding:** Added the "proxy-container" entity type.
- **Modding:** Added SpiderVehicleGraphicsSet::default_color.
- **Modding:** Unified entity_renderer_search_box_limits to 6 from all sides due to reduced update rate optimization of robots.
- **Modding:** Reduced light_renderer_search_distance_limit to 20 to compensate for entity_renderer_search_box_limits change.
- **Scripting:** Added LuaSchedule::get_records(), set_records(), clear_records(), get_interrupts(), set_interrupts(), clear_interrupts().
- **Scripting:** Changed LuaSchedule::add_record() to purely add without any extra behavior.
- **Scripting:** Changed LuaSchedule::add_record() to accept index saying where the record is added.
- **Scripting:** Added LuaProxyContainerControlBehavior.
- **Scripting:** Added defines.inventory.proxy_main.
- **Scripting:** Added LuaEntity::proxy_target_entity and proxy_target_inventory.
- **Scripting:** Added LuaEntity::get_cargo_bays().
- **Scripting:** Added LuaPlayer::add_pin().
- **Scripting:** Added LuaPrototypeBase::factoriopedia_description read.
- **Scripting:** Added factoriopedia_alternative reads to all LuaPrototypes that support it.

## 2.0.37 (26. 02. 2025)


## 2.0.36 (26. 02. 2025)

- **Modding:** Added optional ProgrammableSpeakerNote::cyclic_sound. (112852)
- **Scripting:** Added optional 'stop_playing_sounds' parameter to LuaEntity::play_note().
- **Scripting:** Added LuaSchedule.
- **Scripting:** Added LuaSpacePlatform::get_schedule().
- **Scripting:** Added LuaTrain::get_schedule().

## 2.0.35 (20. 02. 2025)

- **Modding:** Added FurnacePrototype::circuit_connector, circuit_connector_flipped, circuit_wire_max_distance, default_recipe_finished_signal, default_working_signal.
- **Modding:** Added AssemblingMachinePrototype::circuit_connector_flipped.
- **Modding:** Added AssemblingMachinePrototype::max_item_product_count.
- **Modding:** Added LoaderPrototype::adjustable_belt_stack_size.
- **Scripting:** Added LuaFurnaceControlBehavior.
- **Scripting:** Added LuaTransportLine::force_insert_at.
- **Scripting:** Added LuaEntity::loader_belt_stack_size_override read/write.
- **Scripting:** Added LuaEntityPrototype::loader_max_belt_stack_size read.
- **Scripting:** Added LuaEntityPrototype::loader_adjustable_belt_stack_size read.
- **Scripting:** Added on_cargo_pod_finished_descending and on_cargo_pod_delivered_cargo events.
- **Scripting:** Added LuaRecord::contents_size read.
- **Scripting:** Added CustomInputEvent::cursor_direction.
- **Scripting:** Added on_singleplayer_init and on_multiplayer_init.
- **Scripting:** Added defines.inventory.assembling_machine_trash and defines.inventory.furnace_trash.

## 2.0.34 (06. 02. 2025)

- **Scripting:** Added LuaRecord::preview_icons read/write.
- **Scripting:** Added record to on_player_setup_blueprint and on_player_deconstructed_area. (88100)
- **Scripting:** Added LuaEntity::create_cargo_pod().
- **Scripting:** Added LuaEntity::cargo_hatches read.
- **Scripting:** Added LuaEntity::cargo_pod_state read.
- **Scripting:** Added LuaEntity::cargo_pod_destination read/write.
- **Scripting:** Added LuaCargoHatch.
- **Scripting:** Added Luaentity::attached_cargo_pod read.
- **Scripting:** Added LuaEntity::rocket read.
- **Scripting:** Added LuaSpacePlatform::can_leave_current_location().
- **Scripting:** Added LuaSpacePlatform::distance read/write.
- **Scripting:** Added LuaSpacePlatform::space_connection read/write.
- **Scripting:** Changed LuaSpacePlatform::space_location to read/write.

## 2.0.33 (28. 01. 2025)

- **Modding:** Renamed WorkingSound::max_sounds_per_type to WorkingSound::max_sounds_per_prototype. The limit is now applied per prototype.
- **Modding:** Removed WorkingSound::apparent_volume.
- **Modding:** Removed WorkingSound::audible_distance_modifier, MainSound::audible_distance_modifier and SoundAccent::audible_distance_modifier. Sound::audible_distance_modifier is used instead.
- **Modding:** Removed PlaySoundTriggerEffectItem::volume_modifier and PlaySoundTriggerEffectItem::audible_distance_modifier.
- **Scripting:** Added LuaEntityPrototype::get_pumping_speed. LuaEntityPrototype::pumping_speed is deprecated and should not be used.
- **Scripting:** Added optional 'surface' parameter to LuaPlayer::create_local_flying_text().

## 2.0.32 (20. 01. 2025)

- **Scripting:** Added connection_category to LuaFluidboxPrototype::pipe_connections.
- **Modding:** Added FluidStream::target_initial_position_only. It's used by worm acid spit.

## 2.0.31 (16. 01. 2025)

- **Scripting:** ItemPrototype::spoil_result and spoil_to_trigger_result can now be used at the same time.

## 2.0.30 (10. 01. 2025)

- **Scripting:** Added LuaEntity::inserter_spoil_priority read/write.

## 2.0.29 (06. 01. 2025)

- **Scripting:** Added LuaRecord::get_active_index.
- **Scripting:** Added LuaEntityPrototype::science_pack_drain_rate_percent read.
- **Scripting:** Added LuaEntityPrototype::get_fluid_usage_per_tick. LuaEntityPrototype::fluid_usage_per_tick is deprecated and should not be used.
- **Scripting:** Added LuaEntityPrototype::get_max_power_output. LuaEntityPrototype::max_power_output is deprecated and should not be used.
- **Scripting:** LuaEntity::combinator_description supports ghosts of combinators.
- **Scripting:** Added LuaDefines::car_trash read. (124950)
- **Scripting:** Added asteroid collector support to LuaEntity::get_filter, set_filter, and filter_slot_count.
- **Scripting:** Added LuaPlayer::clear_recipe_notification().
- **Scripting:** Changed LuaEntity::get_passenger() to give the character in cargo pods. (121766)
- **Scripting:** Added LuaControl::hub read.
- **Scripting:** Changed LuaEntity::cargo_pod read into LuaControl::cargo_pod read and made it work for players in cargo pods.
- **Scripting:** Changed LuaEntity::get_logistic_point() and LuaEntity::get_logistic_sections() to work with ghosts.
- **Modding:** Added CargoWagonPrototype::quality_affects_inventory_size.
- **Modding:** Added FluidWagonPrototype::quality_affects_capacity.

## 2.0.28 (20. 12. 2024)


## 2.0.27 (18. 12. 2024)

- **Modding:** TipsAndTricksItem requires at least one dependency if it has a `dependencies-met` trigger.
- **Modding:** Added UnitAISettings::size_in_group and UnitAISettings::join_attacks.
- **Modding:** Added LuaAISettings::size_in_group and LuaAISettings::join_attacks.
- **Modding:** Added EnemySpawnerPrototype::max_count_of_owned_defensive_units and EnemySpawnerPrototype::max_defensive_friends_around_to_spawn.
- **Modding:** Added LuaEntityPrototype::max_count_of_owned_defensive_units and LuaEntityPrototype::max_defensive_friends_around_to_spawn.
- **Scripting:** Added LuaSurface::ignore_surface_conditions.

## 2.0.26 (16. 12. 2024)

- **Scripting:** Added LuaEntity::minable_flag read/write. Write to LuaEntity::minable is now deprecated.
- **Scripting:** Added LuaEntity::is_updatable read, disabled_by_script read/write, disabled_by_control_behavior read and disabled_by_recipe read.
- **Scripting:** Added LuaEntity::is_freezable read and frozen read.

## 2.0.25 (12. 12. 2024)

- **Modding:** UTF-8 encoding is now checked for all mod text files to ensure proper rendering. Mods with ANSI encoded text files will not load anymore. (Prompted by 120452)
- **Modding:** Added InserterPrototype::starting_distance.
- **Modding:** Added minimum collision box restriction to cargo bays, cargo landing pads and space platform hubs. (124079)
- **Modding:** Burner inserter initial energy amount was changed to be defined on the burner energy source prototype.
- **Modding:** Changed UseEntityInEnergyProductionAchievementPrototype::consumed_condition into ItemIDFilter.
- **Modding:** ItemProductPrototype and FluidProductPrototype ignored_by_productivity defaults to value of ignored_by_stats.
- **Modding:** Added heating_radius to ReactorPrototype and HeatPipePrototype.
- **Scripting:** Added LuaBurnerPrototype::initial_fuel and initial_fuel_percent read.
- **Scripting:** Added LuaSpacePlatform::last_visited_space_location read.
- **Scripting:** Added LuaSpacePlatform::paused read/write.

## 2.0.24 (05. 12. 2024)

- **Modding:** Added support for Opus audio codec.
- **Modding:** Added FluidBox::mirrored_pipe_picture and mirrored_pipe_picture_frozen.
- **Modding:** Added CharacterArmorAnimation::mining_with_tool_particles_animation_positions.
- **Modding:** Underground fluid box connections with incompatible underground_collision_mask are allowed to connect as long as tiles between do not collide with any of them.
- **Scripting:** Added LuaCustomEventPrototype::event_id read.
- **Scripting:** Added LuaCustomInputPrototype::event_id read.
- **Scripting:** Added LuaBootstrap::get_event_id.
- **Scripting:** Unified parsing of event types into LuaEventType. Made it possible to specify custom events and custom inputs by providing prototype instance.
- **Scripting:** Custom events and custom inputs defined by prototypes are given constants inside of defines.events.

## 2.0.23 (28. 11. 2024)


## 2.0.22 (26. 11. 2024)

- **Modding:** Corpses used by entities with health automatically use the collision box of the parent entity. (118718)
- **Modding:** Added LuaEntityPrototype::auto_setup_collision_box which defaults to true.
- **Scripting:** Added LuaEntityPrototype::auto_setup_collision_box read.
- **Scripting:** Events::on_cargo_pod_finished_ascending Lua event added.
- **Scripting:** 'rocket-launched' achievement condition now triggered by cargo pod ascending instead of rocket.
- **Scripting:** removed property 'player_index' from Events::on_rocket_launched data.
- **Scripting:** Changed LuaLogisticPoint::targeted_items_deliver and targeted_items_pickup to include quality.
- **Scripting:** Changed all instances of get_item_count to support quality.
- **Scripting:** Changed LuaPlayer::get_quick_bar_slot to include quality.
- **Scripting:** Changed LuaEquipmentGrid::get_contents() to include quality.
- **Scripting:** Changed LuaEquipmentGrid::count() to support quality.
- **Scripting:** Changed LuaEntity::storage_filter read to include quality.
- **Scripting:** Added quality to selected_prototype during custom input events.
- **Scripting:** Added GameViewSettings::show_surface_list property to control its vibility in the Remote View.

## 2.0.21 (21. 11. 2024)

- **Modding:** Added distance_from_nearest_point_x and distance_from_nearest_point_y noise expressions.
- **Modding:** Moved SpiderVehiclePrototype::chunk_exploration_radius to VehiclePrototype.
- **Modding:** Removed limit of 64 unique PipeConnectionDefinitions's connection categories.
- **Modding:** Removed music_transition_* utility constants.
- **Modding:** Changed CraftItemTechnologyTrigger::item into ItemIDFilter. Removed item_quality.
- **Modding:** Changed ProduceAchievementPrototype::item_product into ItemIDFilter. Removed quality.
- **Modding:** Changed ProducePerHourAchievementPrototype::item_product into ItemIDFilter.
- **Scripting:** Added optional build_check_type to LuaControl::teleport. (122001)
- **Scripting:** Added LuaEntityPrototype::heating_energy read. (121781)
- **Scripting:** Added LuaForce::circuit_network_enabled, cliff_deconstruction_enabled, mining_with_fluid, rail_support_on_deep_oil_ocean, rail_planner_allow_elevated_rails, vehicle_logistics read. (120676)

## 2.0.20 (18. 11. 2024)


## 2.0.19 (15. 11. 2024)


## 2.0.18 (14. 11. 2024)

- **Modding:** Changed base/space-age tile collision mask definitions so that they don't share references to the same tables.
- **Modding:** Added ItemPrototype::spoil_level.
- **Scripting:** Fixed/reworked how setting tiles behaves vis-à-vis (double)hidden tiles (concerns LuaSurface::set_tiles, editor and placing of non-mineable tiles in-game) (118527)
- **Scripting:** Added LuaEquipment::inventory_bonus read.
- **Scripting:** Added LuaEquipmentGrid::inventory_bonus and LuaEquipmentGrid::movement_bonus read.
- **Scripting:** Added LuaEquipmentPrototype::get_inventory_bonus().
- **Scripting:** Fixed that LuaEntity::get_priority_target() would give invalid results for empty filters.
- **Scripting:** Extended LuaEntity::splitter_filter, splitter_input_priority and splitter_output_priority to also work with lane splitters.

## 2.0.17 (12. 11. 2024)

- **Modding:** Input loader supports filters.
- **Scripting:** Added LuaControl::set_driving() (121014)

## 2.0.16 (08. 11. 2024)

- **Scripting:** Added hide_clouds and hide_fog parameters to LuaGameScript::take_screenshot. (120199)
- **Scripting:** Added LuaEntity::get_logistic_sections(). Added LuaLogisticSections.

## 2.0.15 (05. 11. 2024)

- **Modding:** [space-age] Changed territory noise expressions coordinate system from chunk-based to tile-based.
- **Modding:** Added option to surface.pollute() for recording the pollution change in statistics.
- **Modding:** Fixed on_entity_damaged.source not behaving according to the 2.0 specification.
- **Scripting:** Added connection_type and linked_connection_id to LuaFluidboxPrototype::pipe_connections.

## 2.0.14 (01. 11. 2024)

- **Modding:** Combined four ghost tint definitions in UtilityConstants into UtilityConstants::ghost_shader_tint and added UtilityConstants::ghost_shaderless_tint.
- **Modding:** Added LoaderPrototype::per_lane_filters.
- **Scripting:** Added LuaEntity::loader_filter_mode (read/write).

## 2.0.13 (30. 10. 2024)

- **Scripting:** Added LuaSpacePlatform::name write.
- **Scripting:** Added player_won to the on_pre_scenario_finished event.
- **Scripting:** LuaControl uses physical controller for item manipulations (LuaControl::insert, has_items_inside, get_item_count, remove_item, clear_items_inside)
- **Scripting:** Added LuaPlayer::physical_controller_type read.
- **Scripting:** Added LuaQualityPrototype::color read.

## 2.0.12 (28. 10. 2024)

- **Modding:** Added LoaderPrototype::frozen_patch_in and frozen_patch_out.

## 2.0.11 (25. 10. 2024)

- **Modding:** Added AssemblingMachinePrototype::disabled_when_recipe_not_researched.
- **Scripting:** Added LuaEntity::insert_plan and LuaEntity::removal_plan read/write.
- **Scripting:** Added removal_plan parameter to LuaSurface::create_entity for item request proxies.

## 2.0.10 (23. 10. 2024)


## 2.0.9 (22. 10. 2024)


## 2.0.8 (21. 10. 2024)


## 2.0.7 (20. 10. 2024)

- **Modding:** Added global feature_flags in the settings and prototype stages.
- **Modding:** Added BeaconPrototype::allowed_module_categories, CraftingMachinePrototype::allowed_module_categories,
- **Modding:** Replaced the map generator water slider with an autoplace control prototype; water_level and segmentation_multiplier are now noise expressions.
- **Modding:** Removed pre-defined noise variables finite_water_level, wlc_elevation_offset, wlc_elevation_minimum, cliff_elevation_offset,
- **Modding:** Added EntityWithHealthPrototype::overkill_fraction.
- **Modding:** Removed AutoplacePeak specification format.
- **Modding:** Added AmmoItemPrototype::shoot_protected.
- **Modding:** Removed ItemPrototype::rocket_launch_product. Use rocket_launch_products instead.
- **Modding:** Moved FluidBoxManagerPrototype::off_when_no_fluid_recipe up to AssemblingMachinePrototype::fluid_boxes_off_when_no_fluid_recipe.
- **Modding:** Added delayed-active-trigger ActiveTrigger type.
- **Modding:** Added ability to attach a SmokeWithTrigger to a target entity and make it fade when the target entity is destroyed.
- **Modding:** Added time-based cooldowns to TriggerEffectWithCooldown.
- **Modding:** Removed ContainerPrototype::enable_inventory_bar.
- **Modding:** Added ContainerPrototype::inventory_type "normal".
- **Modding:** Added LinkedContainerPrototype::inventory_type "normal".
- **Modding:** Added ItemPrototype::send_to_orbit_mode.
- **Modding:** Renamed ItemPrototype::placed_as_equipment_result to place_as_equipment_result to match the runtime name.
- **Modding:** Removed BurnerEnergySource::fuel_category. Use BurnerEnergySource::fuel_categories instead.
- **Modding:** Removed slice, slice_x and slice_y from Sprite and RotatedSprite.
- **Modding:** Changed PipeToGround::pictures to use a standard Sprite4Way.
- **Modding:** Removed OffshorePumpPrototype::picture. Use OffshorePumpPrototype::graphics_set instead.
- **Modding:** Removed deprecated "compressed" SpriteFlag.
- **Modding:** Removed icon_mipmaps from various prototypes using icons. Mipmap count will be inferred from icon_size and actual dimensions of the source image.
- **Modding:** Added OffshorePumpPrototype::energy_source and energy_usage.
- **Modding:** Changed research unit ingredients to only be specified by a tuple.
- **Modding:** Changed recipe ingredients to only be specified by a table with named keys.
- **Modding:** Removed catalyst_amount from recipe ingredients and products.
- **Modding:** Added ignored_by_stats to recipe ingredients.
- **Modding:** Added ignored_by_stats and ignored_by_productivity to recipe products.
- **Modding:** Added 'R' (ronna) and 'Q' (quetta) SI prefixes.
- **Modding:** Removed 'K' from allowed SI prefixes - use 'k' instead.
- **Modding:** Renamed "effectivity-module" to "efficiency-module", including all items, recipes, and technologies.
- **Modding:** Renamed technology "advanced-electronics" to "advanced-circuit".
- **Modding:** Renamed technology "advanced-electronics-2" to "processing-unit".
- **Modding:** Renamed technology "optics" to "lamp".
- **Modding:** Reset technology effects is automatically run when technology unlocks change.
- **Modding:** Renamed boiler "heat-water-inside" mode to "heat-fluid-inside".
- **Modding:** Replaced TileSpriteLayoutVariant::tall with TileSpriteLayoutVariant::tile_height.
- **Modding:** Removed WorkingVisualisation::draw_as_sprite and WorkingVisualisation::draw_as_light. Use SpriteParameters::draw_as_light and draw_as_glow instead.
- **Modding:** Removed BeaconModuleVisualization::draw_as_sprite and BeaconModuleVisualization::draw_as_light.
- **Modding:** Removed AnimationElement::draw_as_sprite and AnimationElement::draw_as_light.
- **Modding:** Removed BeaconGraphicsSet::apply_module_tint_to_light.
- **Modding:** On prototypes of entities with circuit connector removed circuit_wire_connection_points and circuit_connector_sprites but added circuit_connector.
- **Modding:** Renamed InserterPrototype::stack to InserterPrototype::bulk.
- **Modding:** Changed "forward-then-backward" animation run mode to not repeat the first and the last frame when running backward.
- **Modding:** Determining whether a tile draws transitions over different tile takes into consideration also TilePrototype::layer_group now.
- **Modding:** Renamed TileRenderLayer "ground" to "ground-natural" and added "ground-artificial".
- **Modding:** Reduced number of layers in "zero" tile render layer group from 128 to 64. And "water" from 64 to 8.
- **Modding:** Removed TilePrototype::draw_in_water_layer.
- **Modding:** Changed tile graphics definition format for both main tile pictures and tile transitions. See TilePrototype documentation.
- **Modding:** Add more prototype properties for shaping Spidertron and spider unit legs and behaviors.
- **Modding:** Loader is now circuit connectable.
- **Modding:** Increased the limit of different "optimized-decorative" types from 255 to 65535.
- **Modding:** Removed EntityPrototype::drawing_box and replaced it with drawing_box_vertical_extension.
- **Modding:** Changed icon_size default to be always 64, which is also defined by defines.default_icon_size, for the case we ever wanted to change this.
- **Modding:** Changed icon drawing in GUIs to account for all layers when scaling them to fit a slot or a button.
- **Modding:** Added IconData::draw_background.
- **Modding:** Increased the limit of different tile types from 255 to 65535.
- **Modding:** Collision layers are now defined by prototypes. There is still limit of 55 layers but the layers themselves can have any name.
- **Modding:** Collision mask has a mandatory table "layers" which must specify layers as dictionary.
- **Modding:** Removed collision layers from "layer-13" to "layer-55".
- **Modding:** Changed prototypes from straight-rail to legacy-straight-rail and curved-rail to legacy-curved-rail
- **Modding:** New rail prototypes: straight-rail, curved-rail-a, curved-rail-b, half-diagonal-rail, rail-ramp, elevated-straight-rail, elevated-curved-rail-a, elevated-curved-rail-b, elevated-half-diagonal-rail.
- **Modding:** Added rail-support prototype.
- **Modding:** Changed way of defining rail prototype graphics: pictures are tied to direction of an entity they will be used by.
- **Modding:** Changed prototype data loading to enforce the correct types are used.
- **Modding:** Restricted prototype names to only contain alphanumeric characters, dashes and underscores.
- **Modding:** Added RailPrototype::ending_shifts to fine-tune render position of rail endings.
- **Modding:** Added RollingStockPrototype::transition_collision_mask and RollingStockPrototype::elevated_collision_mask.
- **Modding:** Changed rail planner prototype: it now takes list of rail entities it is allowed to place and optional support for use with elevated rails.
- **Modding:** Added EntityPrototypeFlag "building-direction-16-way".
- **Modding:** Reworked noise expression definition system.
- **Modding:** Added circuit connections to TurretPrototype and ArtilleryPrototype.
- **Modding:** Changed most entity graphics definitions to be optional.
- **Modding:** Changed various entity prototypes to only accept "energy_source" for the energy source, not "burner".
- **Modding:** Changed PumpPrototype::fluid_box into input_fluid_box and output_fluid_box.
- **Modding:** Changed TileEffectDefinition to allow for different effects.
- **Modding:** Changed "finish-the-game-achievement" achievement type to "complete-objective-achievement".
- **Modding:** Renamed until_second to within for various achievement prototypes.
- **Modding:** Renamed spidertron-remote prototype to rts-tool.
- **Modding:** Moved subgroup property from individual prototypes to PrototypeBase.
- **Modding:** Removed "axially_symmetrical" property from RotatedSprite and RotatedAnimation definitions.
- **Modding:** Removed the entity flag fast-replaceable-no-cross-type-while-moving and fast-replaceable-no-build-while-moving.
- **Modding:** Removed support for emissions_per_second from worker robots.
- **Modding:** Renamed track_coverage_during_build_by_moving to track_coverage_during_drag_building and changed the default to true
- **Modding:** Added optional tile_condition to the place_as_tile, which allows to specify explicit list of tiles it can be built over.
- **Modding:** Added vector_to_place_result (drop target) support to crafting machines.
- **Modding:** Changed default value of TilePrototype::check_collision_with_entities to true.
- **Modding:** The fluid generated by offshore pump is property of the tile instead of the pump.
- **Modding:** Replaced ModulePrototype::limitation and ModulePrototype::limitation_blacklist with RecipePrototype::allow_[effect-name] properties (e.g. RecipePrototype::allow_productivity). By default, all effects except productivity are allowed.
- **Modding:** Replaced ModulePrototype::limitation_message_key with RecipePrototype::allow_[effect-name]_message properties (e.g. RecipePrototype::allow_productivity_message). If not set, the game uses "item-limitation.[effect-name]-effect".
- **Modding:** Added ElectricPolePrototype::auto_connect_up_to_n_wires.
- **Modding:** Added RecipePrototype::hide_from_signal_gui.
- **Modding:** Replaced min_perceived_performance, performance_to_sound_speedup, min_animation_progress and max_animation_progress with perceived_performance table containing minimum, maximum and performance_to_activity_rate.
- **Modding:** Entity selection priority is no longer deduced from collision masks. Use property 'selection_priority' for that purpose.
- **Modding:** Several prototype types have been given new 'selection_priority' default values, documented in '__base__/prototypes/entities/entity_util.lua'.
- **Modding:** The prototype names of logistic chests have been changed to match their English display name. 'logistic-chest-requester' became 'requester-chest', etc. This applies to entities, items and recipes.
- **Modding:** Added RocketSiloPrototype::rocket_quick_relaunch_start_offset, specifying the starting position for rockets created with the new quick-launch feature. 0 is the regular starting position, 1 is the end of the rising animation.
- **Modding:** Added optional RocketSiloPrototype::rocket_parts_storage_cap, denoting when a silo is considered "full" for crafting rocket parts. Has to be at least rocket_parts_required, and defaults to that value.
- **Modding:** Reworked how PipeConnectionDefinitions are specified. Added 'connection_type'. Added ability to specify 'linked' connection_type. Renamed 'type' into 'flow_direction'. Added direction. 'position' now has to be inside of the entity. Added 'connection_category'. Added 'linked_connection_id'.
- **Modding:** Deprecated player-port prototype.
- **Modding:** Changed type of 'entity-unknown', 'tile-proxy', 'tree-dying-proxy', 'tree-proxy' from flying-text to entity-ghost.
- **Modding:** Removed the "flying-text" entity type. Use LuaPlayer::create_local_flying_text or LuaRendering::draw_text instead.
- **Modding:** Removed the "flame-thrower-explosion" entity type.
- **Modding:** Removed "smoke" entity prototype.
- **Modding:** Removed "particle" and "leaf-particle" entity prototypes.
- **Modding:** Removed "mining-tool" item prototype.
- **Modding:** Removed "noise-layer" prototypes. Places previously accepting them now take a 32-bit integer or a string which gets converted using CRC32.
- **Modding:** Removed SpiderEnginePrototype::military_target check. If a spider vehicle should be a military target, set EntityWithOwnerPrototype::is_military_target directly.
- **Modding:** Removed RecipePrototype::result and result_count. Use RecipePrototype::results instead.
- **Modding:** ProductPrototype now has a mandatory "type" field and does not accept simplified syntax for item products.
- **Modding:** Unified the way hidden property of all prototypes is specified, which is always a hidden bool instead of different kind of flags.
- **Modding:** Added MiningDrillPrototype::effect_receiver, CraftingMachinePrototype::effect_receiver and LabPrototype::effect_receiver.
- **Modding:** Removed MiningDrillPrototype::base_productivity, CraftinMachinePrototype::base_productivity and LabPrototype::base_productivity. They were moved into EffectReceiverPrototype::base_effect.
- **Modding:** Restructured SelectionToolPrototype: specific modes are described under select(required), alt_select(required), reverse_select(optional) and alt_reverse_select(optional) tables.
- **Modding:** Added airborne-pollutant prototype and changed various pollution related properties to support multiple pollution types.
- **Modding:** Rearranged BoilerPrototype's pictures.
- **Modding:** Added CorpsePrototype::expires, defaulting to 'true'. Denotes whether corpses of this type expire by default.
- **Modding:** Moved character guns inventory size to the prototype as guns_inventory_size defaulting to 3.
- **Modding:** Removed hr_version from all graphics definitions. The graphics are now always considered to be in high definition.
- **Modding:** Removed ability of ItemWithInventory to extend inventory.
- **Modding:** Removed ItemPrototype::default_request_amount and wire_count.
- **Modding:** Removed normal and expensive properties from TechnologyPrototype and RecipePrototype.
- **Modding:** Removed deprecated graphics definitions from TransportBeltConnectablePrototype, use belt_animation_set instead.
- **Modding:** Removed RocketSiloPrototype::rocket_result_inventory_size.
- **Modding:** Removed ConstantCombinatorPrototype::item_slot_count.
- **Modding:** Changed "combat-robot-count" achievement type to "combat-robot-count-achievement".
- **Modding:** Changed "ghost-time-to-live" modifier type to "create-ghost-on-entity-death" and changed the modifier from double to bool.
- **Modding:** Added EntityPrototype::icon_draw_specification, to control the scale and shift of alt-info icons for entities.
- **Modding:** Removed AmmoTurretPrototype::entity_info_icon_shift.
- **Modding:** Removed CraftingMachinePrototype::entity_info_icon_shift.
- **Modding:** Removed CraftingMachinePrototype::scale_entity_info_icon.
- **Modding:** Removed StorageTankPrototype::scale_entity_info_icon.
- **Modding:** Removed LinkedContainerPrototype::scale_info_icons.
- **Modding:** Removed ContainerPrototype::scale_info_icons.
- **Modding:** Removed RobotWithLogisticInterfacePrototype::cargo_centered.
- **Modding:** Removed utility constant pollution_color.
- **Modding:** Removed biter_ai_settings global variable. Instead, when requiring "biter-ai-settings.lua", assign the returned table to a local variable.
- **Modding:** Added BeamPrototype::graphics_set and moved graphics related properties there.
- **Modding:** Added CraftingMachinePrototype::graphics_set and moved graphics related properties there.
- **Modding:** Added AccumulatorPrototype::chargable_graphics and moved graphics related properties there.
- **Modding:** [space-age] Added space-platform-hub, cargo-pod and cargo-bay prototypes.
- **Modding:** [space-age] Added asteroid, asteroid-collector and thruster prototype.
- **Modding:** Added asteroid-chunk prototype.
- **Modding:** Added cargo-landing-pad prototype.
- **Modding:** Added procession and procession-layer-inheritance-group prototypes.
- **Modding:** Added space-platform-starter-pack, space-location, planet and space-connection prototypes.
- **Modding:** Added surface-property and surface prototypes.
- **Modding:** Added active-trigger and chain-active-trigger prototypes.
- **Modding:** Added quality prototype and various related prototype properties.
- **Modding:** Added spider-unit prototype.
- **Modding:** [space-age] Added segment and segmented-unit prototypes.
- **Modding:** [space-age] Added lightning-attractor prototype.
- **Modding:** Added lightning prototype.
- **Modding:** Added plant prototype.
- **Modding:** [space-age] Added agricultural-tower prototype.
- **Modding:** Added selector-combinator and display-panel prototypes.
- **Modding:** Added fusion-generator and fusion-reactor prototypes.
- **Modding:** Added burner-usage prototype.
- **Modding:** Added temporary-container prototype.
- **Modding:** Added equipment-ghost prototype.
- **Modding:** Added impact-category, deliver-category and deliver-impact-combination prototypes.
- **Modding:** Added remote-controller prototype.
- **Modding:** Added stateless_visualisation_variations to DecorativePrototype, SimpleEntityPrototype, SimpleEntityWithOwnerPrototype and TreePrototype.
- **Modding:** Added stateless_visualisation to DecorativePrototype and EntityPrototype.
- **Modding:** Added RoboportPrototype::radar_range.
- **Modding:** Added ShortcutPrototype::unavailable_until_unlocked.
- **Modding:** Added MiningDrillPrototype::resource_drain_rate_percent and filter_count.
- **Modding:** [space-age] Added MiningDrillPrototype::drops_full_belt_stacks.
- **Modding:** [space-age] Added LoaderPrototype::max_belt_stack_size.
- **Modding:** [space-age] Added InserterPrototype::max_belt_stack_size.
- **Modding:** Added InserterPrototype::grab_less_to_match_belt_stack and enter_drop_mode_if_held_stack_spoiled.
- **Modding:** Added BeaconPrototype::profile and beacon_counter.
- **Modding:** Added AmmoItemPrototype::ammo_category.
- **Modding:** Added LogisticContainerPrototype::trash_inventory_size.
- **Modding:** Added LabPrototype::trash_inventory_size.
- **Modding:** Added CarPrototype::auto_sort_inventory and trash_inventory_size.
- **Modding:** Added RocketSiloPrototype::rocket_supply_inventory_size, logistic_trash_inventory_size, render_not_in_network_icon and cargo_station_parameters.
- **Modding:** Added TilePrototype::built_animations and related properties.
- **Modding:** Added TilePrototype::weight, max_health, dying_explosion, destroys_dropped_items and default_destroyed_dropped_item_trigger.
- **Modding:** Added ItemPrototype::weight, random_tint_color, has_random_tint, plant_result, destroyed_by_dropping_trigger and default_import_location.
- **Modding:** [space-age] Added ItemPrototype::spoil_result, spoil_to_trigger_result and spoil_ticks.
- **Modding:** Added CliffPrototype::place_as_crater.
- **Modding:** Added TurretPrototype::graphics_set and other graphics related properties.
- **Modding:** Added TechnologyPrototype::research_trigger and allows_productivity.
- **Modding:** Added AmbientSound::planet and variable_sound.
- **Modding:** Added Prototype::factoriopedia_alternative and PrototypeBase::factoriopedia_description, hidden_in_factoriopedia and factoriopedia_simulation.
- **Modding:** Added RecipePrototype::preserve_products_in_machine_output, surface_conditions and maximum_productivity.
- **Modding:** Added VehiclePrototype::allow_remote_driving.
- **Modding:** Added MapSettings::asteroids.
- **Modding:** Added RollingStockPrototype::default_copy_color_from_train_stop.
- **Modding:** Added AmmoTurretPrototype::energy_source and energy_per_shot.
- **Modding:** Added RocketSiloRocketPrototype::cargo_pod_entity.
- **Modding:** Added EntityPrototype::ambient_sounds, tile_buildability_rules, impact_category, icons_positioning and surface_conditions.
- **Modding:** Added RadarPrototype::connects_to_other_radars, energy_fraction_to_connect and energy_fraction_to_disconnect.
- **Modding:** Added CustomInputPrototype::block_modifiers.
- **Modding:** [space-age] Added ArmorPrototype::provides_flight, collision_box and related properties.
- **Modding:** Added CharacterPrototype::flying_bob_speed, grounded_landing_search_radius and flying_collision_mask.
- **Modding:** [space-age] Added capture-robot prototype.
- **Modding:** Added EnemySpawnerPrototype::captured_spawner_entity and time_to_capture.
- **Modding:** [space-age] Added EntityPrototype::heating_energy.
- **Modding:** Added frozen graphics to various entities.
- **Modding:** Added inventory-bonus-equipment prototype.
- **Modding:** Added lane-splitter prototype.
- **Modding:** Added new achievement prototypes: dont-kill-manually-achievement, dont-research-before-researching-achievement,
- **Modding:** Added FluidPrototype::visualization_color.
- **Modding:** Added PipeToGroundPrototype::visualization.
- **Modding:** Added "get-by-unit-number" entity prototype flag.
- **Modding:** Changed plural localisation format to use double underscores around parameter index.
- **Modding:** Added new prototype type "custom-event" to define custom events in the data stage. Custom events share the same namespace as custom inputs and built-in events for subscribing to and raising them.
- **Modding:** Added "grounded" sticker effect to temporarily disable mech armor flight
- **Modding:** Changed autoplace control-setting variable names in noise expressions to be shorter/less verbose.
- **Modding:** Added dynamic volume modifiers to sounds. These are applied when specific conditions in-game are met.
- **Modding:** Added non-linear modes for sound attenuation.
- **Modding:** Added an option to override default zoom level attenuation for individial sounds.
- **Modding:** Added darkness (time of day) threshold for sounds.
- **Modding:** Added Sound::advanced_volume_control which includes attenuation (distance based), fades (zoom level based) and darkness threshold.
- **Modding:** Added Sound::speed_smoothing_window_size to smooth out changes in playback speed.
- **Modding:** Added priority selection to sound aggregation.
- **Modding:** Added activity matching modifiers to further control activity to volume or speed matching of working_sound.
- **Modding:** Added Sound::priority. Sounds with higher priority can replace sounds with lower priority when all audio resources are used.
- **Modding:** Added SoundDefinition::min_volume and SoundDefinition::max_volume for automatic volume variation.
- **Scripting:** Renamed `global` into `storage`.
- **Scripting:** Added LuaBootstrap::feature_flags.
- **Scripting:** Added LuaEntityPrototype::allowed_module_categories read.
- **Scripting:** Added LuaRecipePrototype::allowed_module_categories read.
- **Scripting:** Removed LuaConstantCombiantorControlBehavior::parameters read/write.
- **Scripting:** Added LuaPlanet::associate_surface.
- **Scripting:** Added on_space_platform_pre_mined, on_space_platform_mined_item, on_space_platform_mined_entity, on_space_platform_built_entity,
- **Scripting:** Renamed on_built_entity and on_robot_built_entity parameter `created_entity` to `entity`.
- **Scripting:** Removed LuaConstantCombinatorControlBehavior::signals_count, set_signal() and get_signal().
- **Scripting:** Removed LuaGameScript::disable_tutorial_triggers().
- **Scripting:** Added LuaGameScript::enable_tip_triggers_in_custom_scenarios().
- **Scripting:** Added event on_player_used_spidertron_remote.
- **Scripting:** Added LuaEntity::cargo_pod read.
- **Scripting:** Added LuaHelpers class globally visible under `helpers` in control stage, including in `on_load`.
- **Scripting:** Moved LuaGameScript::table_to_json, json_to_table, write_file, remove_path, direction_to_string, evaluate_expression,
- **Scripting:** Removed LuaGui::is_valid_sprite_path. Use LuaHelpers::is_valid_sprite_path instead.
- **Scripting:** Removed LuaRendering::is_font_valid. Use LuaPrototypes::font instead.
- **Scripting:** Removed LuaGameScript::active_mods. Use LuaBootstrap::active_mods instead.
- **Scripting:** Added on_player_controller_changed event.
- **Scripting:** Added LuaEntity::force_finish_ascending() and force_finish_descending() methods.
- **Scripting:** Added LuaEntity::procession_tick read/write.
- **Scripting:** Removed LuaPlayer::open_map, zoom_to_world, and close_map. LuaPlayer::set_controller with type 'remote' replaces these.
- **Scripting:** Added LuaPlayer::centered_on read/write.
- **Scripting:** Added LuaPrototypes globally visible under `prototypes` in control stage, including in `on_load`.
- **Scripting:** Moved prototypes access from LuaGameScript::X_prototypes to LuaPrototypes::X.
- **Scripting:** Moved filtered prototypes access from LuaGameScript::get_filtered_X_prototypes to LuaPrototypes::get_X_filtered.
- **Scripting:** Moved LuaBootstrap::get_prototype_history to LuaPrototypes::get_history.
- **Scripting:** Moved LuaGameScript::styles to LuaPrototypes::style.
- **Scripting:** Moved LuaGameScript::map_gen_presets to LuaPrototypes::map_gen_preset.
- **Scripting:** Moved LuaGameScript::named_noise_expressions to LuaPrototypes::named_noise_expression.
- **Scripting:** Renamed LuaSettings::player to player_default.
- **Scripting:** Changed Vectors to always be read from the game as the two-element array format instead of sometimes using x and y keys.
- **Scripting:** Removed util.online_players. Use game.connected_players instead.
- **Scripting:** Removed LuaEntity::is_entity_with_force. Use LuaEntity::is_military_target instead.
- **Scripting:** Added preserve_ghosts_and_corpses argument to LuaSurface::create_entity.
- **Scripting:** Added cause argument to LuaSurface::create_entity.
- **Scripting:** Added on_pre_scenario_finished event.
- **Scripting:** Added optional gui_title to game.create_inventory().
- **Scripting:** Changed on_entity_damaged.cause semantics
- **Scripting:** Added on_entity_damaged.source
- **Scripting:** Replaced dealer argument with source and cause arguments in LuaEntity::damage().
- **Scripting:** Added LuaEntityPrototype::growth_grid_tile_size read.
- **Scripting:** Added LuaEntityPrototype::harvest_emissions read.
- **Scripting:** Added LuaSurfacePrototype::surface_properties read.
- **Scripting:** Added max_radius and use_start_position_on_failure to LuaSurface::spill_item_stack.
- **Scripting:** Changed LuaSurface::spill_item_stack to take a table of parameters.
- **Scripting:** Lua functions inside of `global` will now throw an error when saving instead of being silently discarded.
- **Scripting:** Renamed LuaEntityPrototype::stack to LuaEntityPrototype::bulk.
- **Scripting:** Added LuaTechnology::successors and LuaTechnologyPrototype::successors read.
- **Scripting:** Added LuaGameScript::technology_notifications_enabled (read/write).
- **Scripting:** Removed LuaForce::get_saved_technology_progress() and set_saved_technology_progress(). Added LuaTechnology::saved_progress (read/write).
- **Scripting:** Added LuaPlayer::locale read and on_player_locale_changed event.
- **Scripting:** Moved LuaGameScript::request_train_path into LuaTrainManager::request_train_path.
- **Scripting:** Removed LuaEntity::get_rail_segment_entity. Added LuaEntity::get_rail_segment_signal and get_rail_segment_stop.
- **Scripting:** Added LuaEntity::get_item_insert_specification.
- **Scripting:** Added LuaEntity::get_line_item_position, LuaTransportLine::get_line_item_position and LuaTransportLine::line_length.
- **Scripting:** Added LuaTransportLine::get_detailed_contents.
- **Scripting:** Added LuaEntity::fluids_count read, get_fluid() and set_fluid().
- **Scripting:** Removed ability of reading FluidWagon's fluid storage or FluidTurret's internal buffer fluid storage using LuaFluidBox.
- **Scripting:** Added new controller type (remote), which is to build space platforms, so it allows ghost building but not any physical manipulation.
- **Scripting:** Added LuaPlayer::physical_surface, physical_surface_index, physical_vehicle and physical_position read.
- **Scripting:** LuaInventory::get_contents() will now return an array of {name = name, count = count, quality = quality}.
- **Scripting:** Changed market price items to be defined as {name = name, count = count, quality = quality }.
- **Scripting:** Added 8 new directions into defines.direction. If mods are storing any direction values in their storage, they will need to migrate them by multiplying by 2.
- **Scripting:** LuaEntity::rotate no longer takes "spill_items", "enable_looted" nor "force" parameter.
- **Scripting:** Removed LuaEntity::get_upgrade_direction() method.
- **Scripting:** Changed on_built_entity event. Instead of stack/item, it passes consumed_items - modifiable stack of items used for the building.
- **Scripting:** LuaTile::to_be_deconstructed() and related events can be given a force. If not given, it checks if tile is to be deconstructed by any force.
- **Scripting:** Moved LuaItemPrototype::mapper_count property to LuaItemCommon.
- **Scripting:** Renamed LuaLogisticContainerControlBehavior::circuit_mode_of_operation into circuit_exclusive_mode_of_operation.
- **Scripting:** Added LuaCustomEventPrototype type and LuaGameScript::custom_event_prototypes read for the custom event prototypes.
- **Scripting:** Added on_achievement_gained event.
- **Scripting:** Added on_undo_applied event.
- **Scripting:** LuaBootstrap::raise_event()'s "event" parameter now also accepts event names as string as alternative to their numerical IDs. The event names are needed to raise custom events.
- **Scripting:** LuaBootstrap::on_event()'s "event" parameter now accepts event names for built-in events too, in addition to for custom inputs and the new custom events.
- **Scripting:** Added new attribute "icon_selector" to LuaGuiElement::add() for creating textfields and text-boxes with the icon selector button.
- **Scripting:** Removed __self from the LuaObjects. Intended way of checking if an object is a lua object is to check type is userdata.
- **Scripting:** Changed LuaForce::evolution_factor, evolution_factor_by_pollution, evolution_factor_by_time and evolution_factor_by_killing_spawners to get_* and set_* methods.
- **Scripting:** Type of LuaObjects is now "userdata" instead of "table".
- **Scripting:** Added defines.wire_connector_id.
- **Scripting:** Added LuaEntity::get_wire_connector and LuaEntity::get_wire_connectors.
- **Scripting:** Added LuaWireConnector.
- **Scripting:** Added LuaRecipePrototype::hide_from_signal_gui.
- **Scripting:** Removed LuaEntity::circuit_connected_entities, LuaEntity::circuit_connection_definitions and LuaEntity::copper_connection_definitions.
- **Scripting:** Removed LuaEntity::neighbours support for electric poles and power switches.
- **Scripting:** Removed LuaEntity::connect_neighbour and LuaEntity::disconnect_neighbour.
- **Scripting:** LuaCircuitNetwork is now binding to WireConnectorID. Removed LuaCircuitNetwork::circuit_connector_id. Added LuaCircuitNetwork::wire_connector_id.
- **Scripting:** LuaEntity::get_circuit_network and LuaControlBehavior::get_circuit_network now require exactly 1 parameter: wire_connector_id.
- **Scripting:** Replaced LuaEntity::get_merged_signal with LuaEntity::get_signal and LuaEntity::get_merged_signals with LuaEntity::get_signals. They no longer take circuit_connector_id but wire_connector_id.
- **Scripting:** Removed defines.circuit_connector_id.
- **Scripting:** Electric pole created through LuaSurface::create_entity can be requested to not auto connect.
- **Scripting:** Replaced LuaFlowStatistics::get_flow_count parameter "bool input" with "string category" to reflect the addition of the "storage" category.
- **Scripting:** Added LuaFlowStatistics::set_storage_count() and get_storage_count() methods.
- **Scripting:** Added LuaFlowStatistics::storage_counts read.
- **Scripting:** Removed LuaForce::item_production_statistics, fluid_production_statistics, kill_count_statistics and entity_build_count_statistics reads.
- **Scripting:** Added LuaForce::get_item_production_statistics(), get_fluid_production_statistics(), get_kill_count_statistics() and get_entity_build_count_statistics() methods.
- **Scripting:** Removed LuaGameScript::pollution_statistics read.
- **Scripting:** Added LuaGameScript::get_pollution_statistics() method.
- **Scripting:** Unified the way logistic filters are accessed, removed specific character/spidertron logistic filter methods, and all is done through get_logistic_point and get_section.
- **Scripting:** Added LuaControl::get_requester_point() method.
- **Scripting:** Removed LuaControl::clear_vehicle_logistic_slot, get_vehicle_logistic_slot, set_vehicle_logistic_slot,
- **Scripting:** Removed LuaEntity::clear_request_slot(), get_request_slot() and set_request_slot() methods.
- **Scripting:** Removed LuaEntity::request_slot_count read.
- **Scripting:** Added LuaLogisticSection.
- **Scripting:** Added LuaLogisticPoint::get_section(), add_section() and remove_section() methods.
- **Scripting:** Added LuaLogisticPoint::enabled read/write.
- **Scripting:** Added LuaLogisticNetwork::network_id read.
- **Scripting:** Added LuaRailEnd.
- **Scripting:** Added LuaEntity::get_rail_end.
- **Scripting:** Removed LuaTrain::front_rail, back_rail, rail_direction_from_front_rail, rail_direction_from_back_rail. They are replaced with LuaTrain::get_rail_end.
- **Scripting:** Added LuaFluidBox::add_linked_connection(), remove_linked_connection(), get_linked_connection() and get_linked_connections() methods.
- **Scripting:** Renamed LuaFluidBox::get_fluid_system_id() to get_fluid_segment_id().
- **Scripting:** Renamed LuaFluidBox::get_fluid_system_contents() to get_fluid_segment_contents().
- **Scripting:** Removed LuaFluidBox::get_flow() method.
- **Scripting:** Added LuaPlayer::land_on_planet() method.
- **Scripting:** Added LuaPlayer::enter_space_platform() and leave_space_platform() method.
- **Scripting:** Added LuaPlayer::display_density_scale read.
- **Scripting:** Removed LuaEntityPrototype::collision_mask_with_flags, LuaTilePrototype::collision_mask_with_flags and LuaDecorativePrototype::collision_mask_with_flags. Respective collision_mask returns mask with flags instead.
- **Scripting:** Added LuaSurface::global_effect read/write.
- **Scripting:** Removed LuaTechnology::effects, use LuaTechnologyPrototype::effects instead.
- **Scripting:** Added LuaAirbornePollutantPrototype.
- **Scripting:** Removed LuaNoiseLayerPrototype.
- **Scripting:** Removed LuaItemPrototype::limitations and LuaItemPrototype::limitation_message_key reads.
- **Scripting:** Removed LuaGameScript::get_active_entities_count() method.
- **Scripting:** Removed LuaGameScript::count_pipe_groups() method.
- **Scripting:** Removed LuaForce::zoom_to_world_* properties.
- **Scripting:** Removed LuaForce::research_queue_enabled read/write.
- **Scripting:** Removed LuaGuiElement::get_slider_discrete_slider(), set_slider_discrete_slider(), and discrete_slider.
- **Scripting:** Removed LuaGuiElement::clear_and_focus_on_right_click, it is now always true.
- **Scripting:** Removed LuaEntity::text.
- **Scripting:** Removed LuaPlayer::log_active_entity_chunk_counts() and log_active_entity_counts() methods.
- **Scripting:** Removed LuaAutoplaceControl::control_order since it was a duplicate of ::order.
- **Scripting:** CircuitCondition passed to or given by LuaControlBehavior no longer uses the "condition" table, condition should be given directly.
- **Scripting:** Renamed LuaItemStack::blueprint_icons into preview_icons.
- **Scripting:** Added LuaTrainManager available through LuaGameScript::train_manager (read).
- **Scripting:** Added LuaTrainManager::get_trains. Removed LuaSurface::get_trains and LuaForce::get_trains.
- **Scripting:** Added LuaTrainManager::get_train_stops. Removed LuaSurface::get_train_stops, LuaForce::get_train_stops and LuaGameScript::get_train_stops.
- **Scripting:** Added snap_to_grid to LuaSurface::create_entity() and LuaControl::teleport().
- **Scripting:** Added LuaRenderObject. All LuaRendering methods for manipulating object selected by id were moved to LuaRenderObject.
- **Scripting:** Added LuaSurface::localised_name read/write.
- **Scripting:** Moved LuaGameScript::get_train_by_id into LuaTrainManager::get_train_by_id.
- **Scripting:** Added LuaRecord representing records in the blueprint library.
- **Scripting:** Added LuaPlayer::blueprints read.
- **Scripting:** Added LuaGameScript::blueprints read.
- **Scripting:** LuaGameScript::print, LuaPlayer::print, LuaSurface::print and LuaForce::print no longer accept Color as a second parameter.
- **Scripting:** Changed permission related events to also fire when mods edit permissions.
- **Scripting:** Changed LuaForce::ghost_time_to_live to LuaForce::create_ghost_on_entity_death bool read/write.
- **Scripting:** Renamed on_entity_destroyed event into on_object_destroyed.
- **Scripting:** Renamed LuaBootstrap::register_on_entity_destroyed into LuaBootstrap::register_on_object_destroyed.
- **Scripting:** Removed help() method from every Factorio Lua object.
- **Scripting:** Removed LuaObject::isluaobject.
- **Scripting:** Renamed LuaUnitGroup into LuaCommandable. Renamed LuaCommandable::group_number into LuaCommandable::id.
- **Scripting:** Added LuaEntity::commandable read. LuaEntity::unit_group moved to LuaCommandable::parent_group. LuaEntity::spawner moved to LuaCommandable::spawner.
- **Scripting:** Removed LuaEntity::set_command, set_distraction_command, command, distraction_command and moving.
- **Scripting:** Added LuaEquipment::quality read.
- **Scripting:** Added LuaEquipment::to_be_removed read.
- **Scripting:** Added LuaEquipment::ghost_prototype, ghost_type and ghost_name read.
- **Scripting:** Added LuaEquipmentGrid::revive() method.
- **Scripting:** Added quality and ghost parameters to LuaEquipmentGrid::put() method.
- **Scripting:** Added search_ghosts parameter to LuaEquipmentGrid::find() method.
- **Scripting:** Added LuaEquipmentGrid::order_removal() and cancel_removal() methods.
- **Scripting:** Added LuaEquipmentGrid::entity_owner and player_owner read.
- **Scripting:** Changed LuaEquipmentGrid::generator_energy read to LuaEquipmentGrid::get_generator_energy() method.
- **Scripting:** Added LuaPrototypeBase as the common superclass for all Lua*Prototype classes.
- **Scripting:** Added LuaItem and LuaItemCommon. LuaItemCommon is the common superclass for LuaItem and LuaItemStack.
- **Scripting:** Moved LuaControl::get_blueprint_entities to LuaItemCommon and LuaRecord.
- **Scripting:** Added LuaUndoRedoStack available through LuaPlayer::undo_redo_stack (read).
- **Scripting:** Added player and undo_index parameters for undo queue to LuaSurface::set_tiles() method.
- **Scripting:** Added player and item_index parameters for undo queue to LuaEntity::destroy() method.
- **Scripting:** Added item_index parameter for undo queue to LuaSurface::cancel_deconstruct_area() method.
- **Scripting:** Added item_index parameter for undo queue to LuaSurface::create_entity() method.
- **Scripting:** Added item_index parameter for undo queue to LuaEntity::order_upgrade() method.
- **Scripting:** Added item_index parameter for undo queue to LuaEntity::order_deconstruction() method.
- **Scripting:** Added super_forced parameter to cancel_deconstruct_area and deconstruct_area in LuaSurface, LuaRecord and LuaItemCommon.
- **Scripting:** Added quality condition to count_entities_filtered and find_entities_filtered methods in LuaSurface.
- **Scripting:** Added has_double_hidden_tile boolean to count_tiles_filtered and find_tiles_filtered methods in LuaSurface.
- **Scripting:** Added LuaSurface::set_property() and get_property() methods.
- **Scripting:** Added LuaSurface::set_double_hidden_tile() and get_double_hidden_tile() methods.
- **Scripting:** Added LuaTile::double_hidden_tile read.
- **Scripting:** Added LuaSurface::execute_lightning() method.
- **Scripting:** Added max_gap_size and max_attack_distance to LuaSurface::request_path() method.
- **Scripting:** Added LuaSurface::create_global_electric_network() and destroy_global_electric_network() methods.
- **Scripting:** Added LuaSurface::has_global_electric_network read.
- **Scripting:** Added LuaSurface::platform read.
- **Scripting:** Added LuaSurface::pollutant_type read.
- **Scripting:** Added LuaSurface::deletable read.
- **Scripting:** Added LuaRecipe::productivity_bonus read/write.
- **Scripting:** Added LuaNamedNoiseFunction.
- **Scripting:** Added LuaSpacePlatform and LuaPlanet.
- **Scripting:** Added LuaEntity::custom_status read/write.
- **Scripting:** Added LuaEntity::use_filters read/write.
- **Scripting:** Added LuaEntity::name_tag read/write.
- **Scripting:** Added LuaEntity::get_priority_target() and set_priority_target() methods.
- **Scripting:** Added LuaEntity::ignore_unprioritised_targets read/write.
- **Scripting:** Changed LuaEntity::electric_output_flow_limit and electric_input_flow_limit read to get_electric_output_flow_limit() and get_electric_input_flow_limit() methods.
- **Scripting:** Added quality parameter to LuaEntity::set_recipe() method.
- **Scripting:** Added LuaEntity::combinator_description read/write.
- **Scripting:** Added LuaEntity::mining_drill_filter_mode read/write.
- **Scripting:** Added LuaEntity::tick_grown read/write.
- **Scripting:** Added LuaEntity::quality read.
- **Scripting:** Added LuaEntity::always_on read/write.
- **Scripting:** Renamed LuaEntity::electric_emissions to electric_emissions_per_joule.
- **Scripting:** Added LuaEntity::copy_color_from_train_stop read/write.
- **Scripting:** Added LuaEntity::train_stop_priority read/write.
- **Scripting:** Added LuaEntity::rail_layer read.
- **Scripting:** Added LuaEntity::mirroring read/write.
- **Scripting:** Added LuaEntity::crane_grappler_destination and crane_grappler_destination_3d write.
- **Scripting:** Added LuaEntity::crane_destination and crane_destination_3d read/write.
- **Scripting:** Added LuaEntity::artillery_auto_targeting read/write.
- **Scripting:** Added LuaEntity::robot_order_queue read.
- **Scripting:** Added LuaItemCommon::owner_location read.
- **Scripting:** Added LuaForce::unlock_space_location(), lock_space_location() and is_space_location_unlocked() methods.
- **Scripting:** Added LuaForce::create_space_platform() method.
- **Scripting:** Added LuaForce::unlock_space_platforms(), lock_space_platforms() and is_space_platforms_unlocked() methods.
- **Scripting:** Added LuaForce::set_surface_hidden() and get_surface_hidden() methods.
- **Scripting:** Added LuaForce::unlock_quality(), lock_quality() and is_quality_unlocked() methods.
- **Scripting:** Added LuaForce::copy_from() and copy_chart() methods.
- **Scripting:** Added LuaForce::platforms read.
- **Scripting:** Renamed LuaForce::stack_inserter_capacity_bonus to bulk_inserter_capacity_bonus.
- **Scripting:** Added LuaForce::beacon_distribution_modifier and belt_stack_size_bonus read/write.
- **Scripting:** Added LuaSimulation available through LuaGameScript::simulation (read).
- **Scripting:** Added LuaGameScript::get_entity_by_unit_number() method.
- **Scripting:** Added LuaGameScript::set_win_ending_info() and set_lose_ending_info() methods.
- **Scripting:** Added LuaGameScript::planets read.
- **Scripting:** Added LuaGameScript::get_vehicles.
- **Scripting:** Added LuaSurface::planet read.
- **Scripting:** Removed LuaEntityPrototype::max_health. Added LuaEntityPrototype::get_max_health(quality?). Added LuaEntity::max_health read.
- **Scripting:** Changed on_cutscene_waypoint_reached event's parameter "waypoint_index" to not be zero indexed.
- **Scripting:** Added LuaPlayer::clear_local_flying_texts() method.
- **Scripting:** Added LuaSurface::clear_hidden_tiles.