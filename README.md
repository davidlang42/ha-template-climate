# ha-template-climate
A HomeAssistant [climate](https://developers.home-assistant.io/docs/core/entity/climate/) integration using templates, similar to the built in fan/sensor/light [template integrations](https://github.com/home-assistant/core/tree/dev/homeassistant/components/template).

## Features required for MVP ##
- [x] @property: hvac_action
- [x] SUPPORT_FAN_MODE
- [x] climate.set_fan_mode
- [x] @property: fan_mode
- [x] @property: fan_modes
- [x] SUPPORT_TARGET_TEMPERATURE
- [x] climate.set_temperature
- [x] @property: precision
- [x] @property: current_temperature
- [x] @property: target_temperature
- [x] @property: target_temperature_step
- [x] @property: max_temp
- [x] @property: min_temp

## Features to complete ##
- [ ] SUPPORT_TARGET_TEMPERATURE_RANGE
- [ ] @property: target_temperature_low
- [ ] @property: target_temperature_high
- [ ] SUPPORT_AUX_HEAT
- [ ] climate.set_aux_heat
- [ ] @property: is_aux_heat
- [ ] SUPPORT_PRESET_MODE
- [ ] climate.set_preset_mode
- [ ] @property: preset_mode
- [ ] @property: preset_modes
- [ ] SUPPORT_TARGET_HUMIDITY
- [ ] climate.set_humidity
- [ ] @property: current_humidity
- [ ] @property: target_humidity
- [ ] @property: max_humidity
- [ ] @property: min_humidity
- [ ] SUPPORT_SWING_MODE
- [ ] climate.set_swing_mode
- [ ] @property: swing_mode
- [ ] @property: swing_modes