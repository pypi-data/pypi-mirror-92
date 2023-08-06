"""Constants for wilight platform."""

DEFAULT_RECONNECT_INTERVAL = 60
DEFAULT_KEEP_ALIVE_INTERVAL = 12
CONNECTION_TIMEOUT = 15
DEFAULT_PORT = 46000

DOMAIN = "wilight"

CONF_ITEMS = "items"

# Item types
ITEM_NONE = "none"
ITEM_LIGHT = "light"
ITEM_SWITCH = "switch"
ITEM_FAN = "fan"
ITEM_COVER = "cover"

# Light types
LIGHT_NONE = "none"
LIGHT_ON_OFF = "light_on_off"
LIGHT_DIMMER = "light_dimmer"
LIGHT_COLOR = "light_rgb"

# Switch types
SWITCH_NONE = "none"
SWITCH_V1 = "switch_v1"
SWITCH_VALVE = "switch_valve"
SWITCH_PAUSE_VALVE = "switch_pause_valve"

# Fan types
FAN_NONE = "none"
FAN_V1 = "fan_v1"

# Cover types
COVER_NONE = "none"
COVER_V1 = "cover_v1"

# Light service support
SUPPORT_NONE = 0

# Fan status / commands
WL_DIRECTION_OFF = "off"
WL_DIRECTION_FORWARD = "forward"
WL_DIRECTION_REVERSE = "reverse"
WL_SPEED_HIGH = "high"
WL_SPEED_LOW = "low"
WL_SPEED_MEDIUM = "medium"

# Cover commands
WL_OPEN = "open"
WL_CLOSE = "close"
WL_STOP = "stop"

# Cover status
WL_CLOSING = "closing"
WL_OPENING = "opening"
WL_STOPPED = "stopped"

WL_MODELS = [
    "0001",
    "0002",
    "0100",
    "0102",
    "0103",
    "0104",
    "0105",
    "0107",
    "0110",
]
