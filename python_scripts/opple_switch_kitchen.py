
event = data.get('event')

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

pos_start = event.find('id=') + 3
pos_end = event.find(',', pos_start)
switch_id = event[pos_start:pos_end]
logger.debug("[Kitchen Opple Switch]: switch_id=%s", switch_id)

pos_start = event.find('unique_id=') + 10
pos_end = event.find(',', pos_start)
unique_id = event[pos_start:pos_end]
logger.debug("[Kitchen Opple Switch]: unique_id=%s", unique_id)

pos_start = event.find('event=') + 6
pos_end = event.find(',', pos_start)
code = event[pos_start:pos_end]
logger.debug("[Kitchen Opple Switch]: code=%s", code)

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

if code == "1002":
    if light1.state == 'on':
        turnOffLights( kitchen_lights_1 )
    else:
        turnOnLights( kitchen_lights_1 )
elif code == "2002":
    if light2.state == 'on':
        turnOffLights( kitchen_lights_2 )
    else:
        turnOnLights( kitchen_lights_2 )
elif code == "3002":
    if light1.state == 'on':
        new_brightness = decrease_value(brightness_l1, brightness_delta, 1)
        service_data = { 'entity_id': l1, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        new_brightness = decrease_value(brightness_l2, brightness_delta, 1)
        service_data = { 'entity_id': l2, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
elif code == "3001":
    if light1.state == 'on':
        service_data = { 'entity_id': l1, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        service_data = { 'entity_id': l2, 'brightness': 1 }
        hass.services.call('light', 'turn_on', service_data, False)
elif code == "4002":
    if light1.state == 'on':
        new_brightness = increase_value(brightness_l1, brightness_delta, 255)
        service_data = { 'entity_id': l1, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        new_brightness = increase_value(brightness_l2, brightness_delta, 255)
        service_data = { 'entity_id': l2, 'brightness': new_brightness }
        hass.services.call('light', 'turn_on', service_data, False)
elif code == "4001":
    if light1.state == 'on':
        service_data = { 'entity_id': l1, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
    if light2.state == 'on':
        service_data = { 'entity_id': l2, 'brightness': 255 }
        hass.services.call('light', 'turn_on', service_data, False)
elif code == "5002":
    if light1.state == 'on' or light2.state == 'on':
        #hass.services.call('light', 'turn_off', { 'entity_id': [l1, l2] }, False)
        turnOffLights( kitchen_lights_1 )
        turnOffLights( kitchen_lights_2 )
    else:
        #hass.services.call('light', 'turn_on', { 'entity_id': [l1, l2] }, False)
        turnOnLights( kitchen_lights_2 )
        turnOnLights( kitchen_lights_1 )
elif code == "6002":
    if light_cupboard.state == 'on':
        hass.services.call('light', 'turn_off', { 'entity_id': lc }, False)
    else:
        hass.services.call('light', 'turn_on', { 'entity_id': lc }, False)

