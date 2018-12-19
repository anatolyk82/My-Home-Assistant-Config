
all_in_bed = True

for entity_id in hass.states.entity_ids('binary_sensor'):
    if entity_id.find('motion_sensor') >= 0:
        state = hass.states.get(entity_id)
        if state.state == 'on':
            all_in_bed = False
            break

hass.states.set('binary_sensor.all_in_bed', all_in_bed, {
    'friendly_name': 'Everyone in bed',
    'icon': 'mdi:hotel'
})
