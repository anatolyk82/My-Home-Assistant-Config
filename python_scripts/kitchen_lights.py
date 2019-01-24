
kitchen_lights = [
        'light.ikea_lamp_4',
        'light.ikea_lamp_5',
        'light.ikea_lamp_6',
        'light.ikea_lamp_7',
        'light.ikea_lamp_8',
        'light.ikea_lamp_9',
        ]

toState = data.get('state', 'off')

if toState == 'on':
    for i in range(0, len(kitchen_lights)):
        lamp_id = kitchen_lights[ len(kitchen_lights) - i - 1 ]
        service_data = { 'entity_id': lamp_id }
        hass.services.call('light', 'turn_on', service_data, False)
        time.sleep(0.3)
else:
    for i in range(0, len(kitchen_lights)):
        lamp_id = kitchen_lights[ i ]
        service_data = { 'entity_id': lamp_id }
        hass.services.call('light', 'turn_off', service_data, False)
        time.sleep(0.3)

