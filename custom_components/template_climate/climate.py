"""Support for Template climate entities."""
import logging

import voluptuous as vol

DOMAIN = "template_climate"

import homeassistant.helpers.config_validation as cv
from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity#TODO: what of these do I actually need?
from homeassistant.components.climate.const import (#TODO: what of these do I actually need?
    ATTR_PRESET_MODE,
    CURRENT_HVAC_COOL,
    CURRENT_HVAC_HEAT,
    CURRENT_HVAC_IDLE,
    CURRENT_HVAC_OFF,
    HVAC_MODE_COOL,
    HVAC_MODE_HEAT,
    HVAC_MODE_OFF,
    PRESET_AWAY,
    PRESET_NONE,
    SUPPORT_PRESET_MODE,
    SUPPORT_TARGET_TEMPERATURE,
)
from homeassistant.const import ( #TODO: what of these do I actually need?
    CONF_ENTITY_ID,
    CONF_FRIENDLY_NAME,
    CONF_UNIQUE_ID,
    CONF_VALUE_TEMPLATE,
    STATE_OFF,
    STATE_ON,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,

    ATTR_ENTITY_ID,
    ATTR_TEMPERATURE,
    CONF_NAME,
    EVENT_HOMEASSISTANT_START,
    PRECISION_HALVES,
    PRECISION_TENTHS,
    PRECISION_WHOLE,
    SERVICE_TURN_OFF,
    SERVICE_TURN_ON,
)
#TODO: from .const import CONF_AVAILABILITY_TEMPLATE
from .template_entity import TemplateEntity#TODO: do i need this? and therefore the template_entity.py file
#TODO: what of these do I actually need?
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.script import Script
# from homeassistant.core import DOMAIN as HA_DOMAIN, CoreState, callback
# from homeassistant.exceptions import ConditionError
# from homeassistant.helpers import condition
# from homeassistant.helpers.event import (
#     async_track_state_change_event,
#     async_track_time_interval,
# )
# from homeassistant.helpers.reload import async_setup_reload_service
# from homeassistant.helpers.restore_state import RestoreEntity

_LOGGER = logging.getLogger(__name__)

#TODO: TEST SERVICES
# climate.set_hvac_mode
# climate.turn_on
# climate.turn_off

#TODO: MVP SERVICES
# climate.set_temperature
# climate.set_fan_mode
# availability

#TODO: FUTURE SERVICES
# climate.set_aux_heat
# climate.set_preset_mode
# climate.set_humidity
# climate.set_swing_mode

CONF_CLIMATES = "climates"
CONF_ON_ACTION = "turn_on"
CONF_OFF_ACTION = "turn_off"
CONF_SET_HVAC_MODE_ACTION = "set_hvac_mode"
#TODO: CONF_SPEED_LIST = "speeds"
#TODO: CONF_SPEED_COUNT = "speed_count"

CLIMATE_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
        vol.Required(CONF_VALUE_TEMPLATE): cv.template,
        #TODO: vol.Optional(CONF_AVAILABILITY_TEMPLATE): cv.template,
        vol.Optional(CONF_ON_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(CONF_OFF_ACTION): cv.SCRIPT_SCHEMA,
        vol.Required(CONF_SET_HVAC_MODE_ACTION): cv.SCRIPT_SCHEMA,
        #TODO: vol.Optional(CONF_SPEED_COUNT): vol.Coerce(int),
        #TODO: vol.Optional(
        #     CONF_SPEED_LIST,
        #     default=[SPEED_OFF, SPEED_LOW, SPEED_MEDIUM, SPEED_HIGH],
        # ): cv.ensure_list,
        vol.Optional(CONF_ENTITY_ID): cv.entity_ids,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)

PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_CLIMATES): cv.schema_with_slug_keys(CLIMATE_SCHEMA)}
)


async def _async_create_entities(hass, config):
    """Create the Template Climates."""
    climates = []

    for device, device_config in config[CONF_CLIMATES].items():
        friendly_name = device_config.get(CONF_FRIENDLY_NAME, device)

        state_template = device_config[CONF_VALUE_TEMPLATE]
        #TODO: availability_template = device_config.get(CONF_AVAILABILITY_TEMPLATE)

        on_action = device_config.get(CONF_ON_ACTION)
        off_action = device_config.get(CONF_OFF_ACTION)
        set_hvac_mode_action = device_config[CONF_SET_HVAC_MODE_ACTION]
        
        #TODO: speed_list = device_config[CONF_SPEED_LIST]
        #TODO: speed_count = device_config.get(CONF_SPEED_COUNT)
        unique_id = device_config.get(CONF_UNIQUE_ID)

        climates.append(
            TemplateClimate(
                hass,
                device,
                friendly_name,
                state_template,
                #TODO: availability_template,
                on_action,
                off_action,
                set_hvac_mode_action,
                #TODO: speed_count,
                #TODO: speed_list,
                unique_id,
            )
        )

    return climates


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the template climates."""
    async_add_entities(await _async_create_entities(hass, config))

