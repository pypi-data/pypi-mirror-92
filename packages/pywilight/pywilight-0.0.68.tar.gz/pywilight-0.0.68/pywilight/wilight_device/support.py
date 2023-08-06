"""Support functions for wilight platform."""

from ..const import (
    COVER_V1,
    FAN_V1,
    ITEM_COVER,
    ITEM_FAN,
    ITEM_LIGHT,
    ITEM_NONE,
    ITEM_SWITCH,
    LIGHT_COLOR,
    LIGHT_DIMMER,
    LIGHT_NONE,
    LIGHT_ON_OFF,
    SWITCH_PAUSE_VALVE,
    SWITCH_VALVE,
)


def check_config_ex_len(model, config_ex):
    """Get length for model config_ex."""
    if model == "0001":
        if len(config_ex) == 6:
            return True
    elif model == "0002":
        if len(config_ex) == 3:
            return True
    elif model == "0100":
        if len(config_ex) == 8:
            return True
    elif model == "0102":
        if len(config_ex) == 8:
            return True
    elif model == "0103":
        if len(config_ex) == 2:
            return True
    elif model == "0104":
        if len(config_ex) == 2:
            return True
    elif model == "0105":
        if len(config_ex) == 14:
            return True
    elif model == "0107":
        if len(config_ex) == 5:
            return True
    elif model == "0110":
        if len(config_ex) == 3:
            return True
    return False


def get_num_items(model, config_ex):
    """Get number of items."""
    num_items = 1
    if model == "0001":
        return 1
    elif model == "0002":
        num_items = 3
    elif model == "0100":
        if config_ex[1:2] == "1":
            num_items = 2
        if config_ex[2:3] == "1":
            num_items = 3
    elif model == "0102":
        if config_ex[1:2] == "1":
            num_items = 2
        if config_ex[2:3] == "1":
            num_items = 3
    elif model == "0103":
        return 1
    elif model == "0104":
        return 2
    elif model == "0105":
        return 2
    elif model == "0107":
        return 1
    elif model == "0110":
        return 1
    return num_items


def get_item_type(item, model, config_ex):
    """Get item type."""
    if model == "0001":
        if item == 1:
            return ITEM_LIGHT
    elif model == "0002":
        if config_ex[0:1] == "0":
            if item > 0 and item < 4:
                return ITEM_LIGHT
        if config_ex[0:1] == "1":
            if item == 1:
                return ITEM_LIGHT
            elif item == 2:
                return LIGHT_NONE
            elif item == 3:
                return ITEM_LIGHT
        if config_ex[0:1] == "2":
            if item == 1:
                return LIGHT_NONE
            elif item == 2:
                return ITEM_LIGHT
            elif item == 3:
                return LIGHT_NONE
    elif model == "0100":
        if item > 0 and item < 4:
            return ITEM_LIGHT
    elif model == "0102":
        if item > 0 and item < 4:
            return ITEM_LIGHT
    elif model == "0103":
        if item == 1:
            return ITEM_COVER
    elif model == "0104":
        if item == 1:
            return ITEM_LIGHT
        elif item == 2:
            return ITEM_FAN
    elif model == "0105":
        if item > 0 and item < 3:
            return ITEM_SWITCH
    elif model == "0107":
        if item == 1:
            return ITEM_LIGHT
    elif model == "0110":
        if item == 1:
            return ITEM_LIGHT
    return ITEM_NONE


def get_item_sub_types(item, model, config_ex):
    """Get sub type."""
    if model == "0001":
        if item == 1:
            return LIGHT_ON_OFF
    elif model == "0002":
        if item > 0 and item < 4:
            return LIGHT_ON_OFF
    elif model == "0100":
        if item > 0 and item < 4:
            if config_ex[item + 2 : item + 3] == "0":
                return LIGHT_ON_OFF
            elif config_ex[item + 2 : item + 3] == "1":
                return LIGHT_DIMMER
    elif model == "0102":
        if item > 0 and item < 4:
            return LIGHT_ON_OFF
    elif model == "0103":
        if item == 1:
            return COVER_V1
    elif model == "0104":
        if item == 1:
            return LIGHT_ON_OFF
        elif item == 2:
            return FAN_V1
    elif model == "0105":
        if item == 1:
            return SWITCH_VALVE
        elif item == 2:
            return SWITCH_PAUSE_VALVE
    elif model == "0107":
        if item == 1:
            return LIGHT_COLOR
    elif model == "0110":
        if item == 1:
            if config_ex[0] == "0":
                return LIGHT_ON_OFF
            elif config_ex[0] == "1":
                return LIGHT_DIMMER
    return LIGHT_NONE

def get_states_from_sum_item(sub_item):
    """Get state for sub_item."""
    if sub_item == LIGHT_ON_OFF:
        return {
            "on": False,
        }
    elif sub_item == LIGHT_DIMMER:
        return {
            "on": False,
            "brightness": 0,
        }
    elif sub_item == LIGHT_COLOR:
        return {
            "on": False,
            "hue": 0,
            "saturation": 100,
            "brightness": 0,
        }
    elif sub_item == COVER_V1:
        return {
            "motor_state": "stopped",
            "position_target": 0,
            "position_current": 0
        }
    elif sub_item == FAN_V1:
        return {
            "direction": "off",
            "speed": "low"
        }
    elif sub_item == SWITCH_VALVE:
        return {
            "on": False,
            "timer_target": 30,
            "timer_current": 0
        }
    elif sub_item == SWITCH_PAUSE_VALVE:
        return {
            "on": False,
            "timer_target": 43200,
            "timer_current": 0
        }
    return {}

def get_components_from_model(model_name):
    components = []

    if model_name is None:
        return []
    if len(model_name) < 15:
        return []
    model_config = model_name.split(' ', 1)[1].split('-', 1)
    model = model_config[0][0:4]
    config = model_config[1]
    if not check_config_ex_len(model, config):
        return []
    num_items = get_num_items(model, config)
    for item in range(1, num_items + 1):
        component = get_item_type(item, model, config)
        if component != ITEM_NONE:
            components.append(component)

    return components
