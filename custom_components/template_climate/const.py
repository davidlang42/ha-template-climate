# SOURCE: https://github.com/home-assistant/core/blob/dev/homeassistant/components/template/const.py @ 65126cec3e8b075d48b2df124117ae26abeaf2b2
"""Constants for the Template Platform Components."""

CONF_AVAILABILITY_TEMPLATE = "availability_template"
CONF_ATTRIBUTE_TEMPLATES = "attribute_templates"
CONF_TRIGGER = "trigger"

DOMAIN = "template"

PLATFORM_STORAGE_KEY = "template_platforms"

PLATFORMS = [
    "alarm_control_panel",
    "binary_sensor",
    "cover",
    "fan",
    "light",
    "lock",
    "sensor",
    "switch",
    "vacuum",
    "weather",
]

CONF_AVAILABILITY = "availability"
CONF_ATTRIBUTES = "attributes"
CONF_PICTURE = "picture"
CONF_OBJECT_ID = "object_id"