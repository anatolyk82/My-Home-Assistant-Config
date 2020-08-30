
switch_to_light = { 
        "ikea_switch_6":"light.ikea_lamp_13",    # Workroom
        "ikea_switch_5":"light.gledopto_lamp_3", # Guestroom
        "ikea_switch_2":"light.gledopto_lamp_4", # Bedroom
        "ikea_switch_4":"light.aqara_lamp_1",     # Upstairs
        }
brightness_delta = 50
color_temp_delta = 50


def increase_value(current_value, delta, max_value):
    if current_value < max_value:
        current_value = current_value + delta
        if current_value < max_value:
            return current_value
        else:
            return max_value
    else:
        return max_value

def decrease_value(current_value, delta, min_value):
    if current_value > min_value:
        current_value = current_value - delta
        if current_value > min_value:
            return current_value
        else:
            return min_value
    else:
        return min_value

# Input parameters
switch_id = data.get('switch_id')
action = data.get('action')

light_id = switch_to_light[switch_id]
logger.debug("IKEA Switch Control: Light: %s", switch_to_light[switch_id])

light = hass.states.get(light_id)

#for i in light.attributes:
#    logger.debug('light.attributes[%s] = %s', i, light.attributes[i])

brightness = -1
color_temp = -1
if light.state == 'on':
    if 'brightness' in light.attributes:
        brightness = int(light.attributes['brightness'])
    if 'color_temp' in light.attributes:
        color_temp = int(light.attributes['color_temp'])

min_mireds = -1
if 'min_mireds' in light.attributes:
    min_mireds = int(light.attributes['min_mireds'])

max_mireds = -1
if 'max_mireds' in light.attributes:
    max_mireds = int(light.attributes['max_mireds'])

#if color_temp > -1:
#    min_mireds = int(light.attributes['min_mireds'])
#    max_mireds = int(light.attributes['max_mireds'])

logger.debug("IKEA Switch Control: min_mireds: %s, max_mireds: %s", min_mireds, max_mireds)
logger.debug("IKEA Switch Control: brightness: %s, color_temp: %s", brightness, color_temp)


if action == "toggle":
    service_data = { 'entity_id': light_id }
    if light.state == 'on':
        hass.services.call('light', 'turn_off', service_data, False)
    else:
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "brightness_up_click" and (brightness > -1):
    if light.state == 'on':
        new_brightness = increase_value(brightness, brightness_delta, 255)
        service_data = { 'entity_id': light_id, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "brightness_down_click" and (brightness > -1):
    if light.state == 'on':
        new_brightness = decrease_value(brightness, brightness_delta, 1)
        service_data = { 'entity_id': light_id, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "arrow_right_click" and (color_temp > -1):
    if light.state == 'on':
        new_color_temp = increase_value(color_temp, color_temp_delta, max_mireds)
        service_data = { 'entity_id': light_id, 'color_temp': new_color_temp }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "arrow_left_click" and (color_temp > -1):
    if light.state == 'on':
        new_color_temp = decrease_value(color_temp, color_temp_delta, min_mireds)
        service_data = { 'entity_id': light_id, 'color_temp': new_color_temp }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "arrow_left_click" and (color_temp < 0) and (min_mireds > -1):
    if light.state == 'on':
        service_data = { 'entity_id': light_id, 'color_temp': min_mireds }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "arrow_right_click" and (color_temp < 0) and (max_mireds > -1):
    if light.state == 'on':
        service_data = { 'entity_id': light_id, 'color_temp': max_mireds }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "brightness_up_hold" and (brightness > -1):
    if light.state == 'on':
        service_data = { 'entity_id': light_id, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "brightness_down_hold" and (brightness > -1):
    if light.state == 'on':
        service_data = { 'entity_id': light_id, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)





