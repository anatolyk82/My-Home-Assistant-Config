
action = data.get('action')

brightness_delta = 50

kitchen_lights_1 = [
        'light.ikea_lamp_4',
        'light.ikea_lamp_5',
        'light.ikea_lamp_6',
        ]

kitchen_lights_2 = [
        'light.ikea_lamp_7',
        'light.ikea_lamp_8',
        'light.ikea_lamp_9',
        ]

def turnOnLights(lights):
    for i in range(0, len(lights)):
        lamp_id = lights[ len(lights) - i - 1 ]
        service_data = { 'entity_id': lamp_id }
        hass.services.call('light', 'turn_on', service_data, False)
        time.sleep(0.3)

def turnOffLights(lights):
    for i in range(0, len(lights)):
        lamp_id = lights[ i ]
        service_data = { 'entity_id': lamp_id }
        hass.services.call('light', 'turn_off', service_data, False)
        time.sleep(0.3)

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

l1 = 'light.kitchen_lights_1'
l2 = 'light.kitchen_lights_2'
lc = 'light.kitchen_cupboard'

light1 = hass.states.get( l1 )
light2 = hass.states.get( l2 )
light_cupboard = hass.states.get( lc )

brightness_l1 = -1
if light1.state == 'on':
    if 'brightness' in light1.attributes:
        brightness_l1 = int(light1.attributes['brightness'])

brightness_l2 = -1
if light2.state == 'on':
    if 'brightness' in light2.attributes:
        brightness_l2 = int(light2.attributes['brightness'])

if action == "button_1_single":
    if light1.state == 'on':
        turnOffLights( kitchen_lights_1 )
    else:
        turnOnLights( kitchen_lights_1 )
elif action == "button_2_single":
    if light2.state == 'on':
        turnOffLights( kitchen_lights_2 )
    else:
        turnOnLights( kitchen_lights_2 )
elif action == "button_3_single":
    if light1.state == 'on':
        new_brightness = decrease_value(brightness_l1, brightness_delta, 1)
        service_data = { 'entity_id': l1, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        new_brightness = decrease_value(brightness_l2, brightness_delta, 1)
        service_data = { 'entity_id': l2, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "button_3_hold":
    if light1.state == 'on':
        service_data = { 'entity_id': l1, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        service_data = { 'entity_id': l2, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "button_4_single":
    if light1.state == 'on':
        new_brightness = increase_value(brightness_l1, brightness_delta, 255)
        service_data = { 'entity_id': l1, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        new_brightness = increase_value(brightness_l2, brightness_delta, 255)
        service_data = { 'entity_id': l2, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "button_4_hold":
    if light1.state == 'on':
        service_data = { 'entity_id': l1, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        service_data = { 'entity_id': l2, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
elif action == "button_5_single":
    if light1.state == 'on' or light2.state == 'on':
        #hass.services.call('light', 'turn_off', { 'entity_id': [l1, l2] }, False)
        turnOffLights( kitchen_lights_1 )
        turnOffLights( kitchen_lights_2 )
    else:
        #hass.services.call('light', 'turn_on', { 'entity_id': [l1, l2] }, False)
        turnOnLights( kitchen_lights_2 )
        turnOnLights( kitchen_lights_1 )
elif action == "button_6_single":
    if light_cupboard.state == 'on':
        hass.services.call('light', 'turn_off', { 'entity_id': lc }, False)
    else:
        hass.services.call('light', 'turn_on', { 'entity_id': lc }, False)

