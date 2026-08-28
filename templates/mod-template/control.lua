-- Control stage: рантайм-логика (выполняется в мире).
-- Храни состояние в storage (не global!), Lua-объекты НЕ сохранять —
-- только unit_number/имена.

-- script.on_init(function() storage.initialized = true end)
-- script.on_load(function() ... end)
--
-- script.on_event(defines.events.on_built_entity, function(event)
--   local entity = event.entity  -- в 2.0 параметр называется entity!
-- end)
