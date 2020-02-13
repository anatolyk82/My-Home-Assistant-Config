
light_id = 'light.bed_led'
timer_id = 'timer.bed_light_timer'
timer_delta = 3

# 2sec -> 2*255 = 500 secs -> 8:20
# 3sec -> 3*255 = 765 secs -> 12:45

light_state = hass.states.get(light_id).state

if light_state == 'off':
    service_data = { 'entity_id': light_id, 'brightness': 1, 'rgb_color':[255, 255, 0] }
    hass.services.call('light', 'turn_on', service_data, False)

    service_data = { 'entity_id': timer_id, 'duration': timer_delta }
    hass.services.call('timer', 'start', service_data, False)
else:
    l = hass.states.get(light_id)
    brightness = l.attributes['brightness']
    logger.debug("[Light Transition]: Brightness of %s is %s", light_id, brightness)

    brightness = brightness + 2

    service_data = { 'entity_id': light_id , 'brightness':brightness }
    hass.services.call('light', 'turn_on', service_data, False)

    if brightness < 255:
        service_data = { 'entity_id': timer_id, 'duration': timer_delta }
        hass.services.call('timer', 'start', service_data, False)



