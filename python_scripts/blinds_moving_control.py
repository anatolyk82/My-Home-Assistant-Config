
blinds_entity_id = data.get('entity_id')
isMoving = data.get('is_moving')

sensor_name = 'binary_sensor.' + blinds_entity_id.split('.')[1] + '_moving'

if hass.states.get(sensor_name) == None:
    hass.states.set(sensor_name, 'off')
else:
    hass.states.set(sensor_name, isMoving)

