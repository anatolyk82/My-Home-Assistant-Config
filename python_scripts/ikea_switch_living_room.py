
# Living room bulbs:
light1_entity_id = 'light.gledopto_lamp_1'
light2_entity_id = 'light.gledopto_lamp_2'


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

light1 = hass.states.get(light1_entity_id)
light2 = hass.states.get(light2_entity_id)

# Get brightness of the light1
brightness1 = -1
color_temp1 = -1
if light1.state == 'on':
    if 'brightness' in light1.attributes:
        brightness1 = int(light1.attributes['brightness'])
    if 'color_temp' in light1.attributes:
        color_temp1 = int(light1.attributes['color_temp'])


# Get brightness of the light2
brightness2 = -1
color_temp2 = -1
if light2.state == 'on':
    if 'brightness' in light2.attributes:
        brightness2 = int(light2.attributes['brightness'])
    if 'color_temp' in light2.attributes:
        color_temp2 = int(light2.attributes['color_temp'])


# Input parameters
button = data.get('button')
logger.debug("IKEA Switch Control: button=%s", button)


if button == "center_click":
    any_light_is_on = ((light1.state == 'on') or (light2.state == 'on'))
    if any_light_is_on == True:
        service_data = { 'entity_id': light1_entity_id }
        hass.services.call('light', 'turn_off', service_data, False)
        service_data = { 'entity_id': light2_entity_id }
        hass.services.call('light', 'turn_off', service_data, False)
    else:
        service_data = { 'entity_id': light1_entity_id, "color_temp":460 }
        hass.services.call('light', 'turn_on', service_data, False)
        service_data = { 'entity_id': light2_entity_id, "color_temp":460 }
        hass.services.call('light', 'turn_on', service_data, False)

elif button == "left_click":
    service_data = { 'entity_id': light1_entity_id }
    logger.debug("IKEA Switch Control: service_data=%s", service_data)
    if light1.state == 'on':
        hass.services.call('light', 'turn_off', service_data, False)
    else:
        hass.services.call('light', 'turn_on', service_data, False)

elif button == "right_click":
    service_data = { 'entity_id': light2_entity_id }
    logger.debug("IKEA Switch Control: service_data=%s", service_data)
    if light2.state == 'on':
        hass.services.call('light', 'turn_off', service_data, False)
    else:
        hass.services.call('light', 'turn_on', service_data, False)

elif button == "up_click":
    if (brightness1 > -1) and light1.state == 'on':
        new_brightness = increase_value(brightness1, brightness_delta, 255)
        service_data = { 'entity_id': light1_entity_id, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
    if (brightness2 > -1) and light2.state == 'on':
        new_brightness = increase_value(brightness2, brightness_delta, 255)
        service_data = { 'entity_id': light2_entity_id, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)

elif button == "down_click":
    if (brightness1 > -1) and light1.state == 'on':
        new_brightness = decrease_value(brightness1, brightness_delta, 1)
        service_data = { 'entity_id': light1_entity_id, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
    if (brightness2 > -1) and light2.state == 'on':
        new_brightness = decrease_value(brightness2, brightness_delta, 1)
        service_data = { 'entity_id': light2_entity_id, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)

elif button == "down_press":
    if (brightness1 > -1) and light1.state == 'on':
        service_data = { 'entity_id': light1_entity_id, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)
    if (brightness2 > -1) and light2.state == 'on':
        service_data = { 'entity_id': light2_entity_id, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)

elif button == "up_press":
    if (brightness1 > -1) and light1.state == 'on':
        service_data = { 'entity_id': light1_entity_id, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
    if (brightness2 > -1) and light2.state == 'on':
        service_data = { 'entity_id': light2_entity_id, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
