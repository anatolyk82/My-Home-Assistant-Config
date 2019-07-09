
action = data.get('action') # Should take values: 'turn_on', 'turn_off', 'toggle'

a1 = 'automation.upstairs_light_turn_on_if_motion_06_30_23_00'
a2 = 'automation.upstairs_light_turn_on_if_motion_23_00_00_00'
a3 = 'automation.upstairs_light_turn_off_00_00_06_30'
a4 = 'automation.upstairs_light_turn_off_in_5_minutes_after_motion'

light = 'light.ikea_lamp_1'

if action == 'turn_on' or action == 'turn_off' or action == 'toggle':
    service_data = { 'entity_id': a1 }
    hass.services.call('automation', action, service_data, False)
    service_data = { 'entity_id': a2 }
    hass.services.call('automation', action, service_data, False)
    service_data = { 'entity_id': a3 }
    hass.services.call('automation', action, service_data, False)
    service_data = { 'entity_id': a4 }
    hass.services.call('automation', action, service_data, False)

    initial_state = hass.states.get( light ).state
    service_data = { 'entity_id': light }

    hass.services.call('light', 'toggle', service_data, False)
    time.sleep(0.6)
    hass.services.call('light', 'toggle', service_data, False)
    time.sleep(0.6)
    hass.services.call('light', 'toggle', service_data, False)
    time.sleep(0.6)
    hass.services.call('light', 'toggle', service_data, False)
    time.sleep(0.6)

    if initial_state == 'on':
        hass.services.call('light', 'turn_off', service_data, False)
    else:
        hass.services.call('light', 'turn_on', service_data, False)

