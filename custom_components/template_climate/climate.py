# based heavily off other template components: https://github.com/home-assistant/core/tree/dev/homeassistant/components/template
"""Support for Template climate entities."""
import logging

import voluptuous as vol

DOMAIN = "template_climate"

import homeassistant.helpers.config_validation as cv
from homeassistant.components.climate import (
    ClimateEntity,
    ENTITY_ID_FORMAT,
    PLATFORM_SCHEMA,
)
from homeassistant.components.climate.const import (
    ATTR_HVAC_MODE,
    HVAC_MODE_OFF,
    HVAC_MODES,
)
from homeassistant.const import (
    CONF_ENTITY_ID,
    CONF_FRIENDLY_NAME,
    CONF_UNIQUE_ID,
    CONF_VALUE_TEMPLATE,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
)
from .const import CONF_AVAILABILITY_TEMPLATE
from .template_entity import TemplateEntity
from homeassistant.exceptions import TemplateError
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.helpers.script import Script
from homeassistant.core import callback

_LOGGER = logging.getLogger(__name__)

CONF_CLIMATES = "climates"
CONF_SET_HVAC_MODE_ACTION = "set_hvac_mode"
CONF_HVAC_LIST = "hvac_modes"

CLIMATE_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
        vol.Required(CONF_VALUE_TEMPLATE): cv.template,
        vol.Optional(CONF_AVAILABILITY_TEMPLATE): cv.template,
        vol.Required(CONF_SET_HVAC_MODE_ACTION): cv.SCRIPT_SCHEMA,
        vol.Optional(CONF_HVAC_LIST, default=HVAC_MODES): vol.All(
            cv.ensure_list, [vol.In(HVAC_MODES)]
        ),
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
        availability_template = device_config.get(CONF_AVAILABILITY_TEMPLATE)
        set_hvac_mode_action = device_config[CONF_SET_HVAC_MODE_ACTION]
        hvac_list = device_config.get(CONF_HVAC_LIST)
        unique_id = device_config.get(CONF_UNIQUE_ID)

        climates.append(
            TemplateClimate(
                hass,
                device,
                friendly_name,
                state_template,
                availability_template,
                set_hvac_mode_action,
                hvac_list,
                unique_id,
            )
        )

    return climates

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the template climates."""
    async_add_entities(await _async_create_entities(hass, config))

class TemplateClimate(TemplateEntity, ClimateEntity):
    """A template climate component."""

    def __init__(
        self,
        hass,
        device_id,
        friendly_name,
        state_template,
        availability_template,
        set_hvac_mode_action,
        hvac_list,
        unique_id,
    ):
        """Initialize the climate."""
        super().__init__(availability_template=availability_template)
        self.hass = hass
        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT, device_id, hass=hass
        )
        self._name = friendly_name
        self._template = state_template
        self._hvac_list = hvac_list
        self._unique_id = unique_id

        domain = __name__.split(".")[-2]
        self._set_hvac_mode_script = Script(hass, set_hvac_mode_action, friendly_name, domain)

        self._state = None
        self._supported_features = 0
        self._temperature_unit = hass.config.units.temperature_unit

    @property
    def name(self):
        """Return the display name of this climate."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this climate."""
        return self._unique_id

    @property
    def supported_features(self) -> int:
        """Flag supported features."""
        return self._supported_features

    @property
    def hvac_mode(self):
        """Return current operation (state)."""
        return self._state or HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """List of available operation modes."""
        return self._hvac_list

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._temperature_unit

    async def async_set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        if hvac_mode not in self.hvac_modes:
            _LOGGER.error(
                "Received invalid hvac_mode: %s. Expected: %s", hvac_mode, self.hvac_modes
            )
            return

        self._state = hvac_mode

        await self._set_hvac_mode_script.async_run(
            {ATTR_HVAC_MODE : self._state}, context=self._context
        )

    @callback
    def _update_state(self, result):
        super()._update_state(result)
        if isinstance(result, TemplateError):
            self._state = None
            return

        # Validate state
        if result in self.hvac_modes:
            self._state = result
        elif result in [STATE_UNAVAILABLE, STATE_UNKNOWN]:
            self._state = None
        else:
            _LOGGER.error(
                "Received invalid climate hvac_mode state: %s. Expected: %s",
                result,
                ", ".join(self.hvac_modes),
            )
            self._state = None

    async def async_added_to_hass(self):
        """Register callbacks."""
        self.add_template_attribute("_state", self._template, None, self._update_state)
        await super().async_added_to_hass()