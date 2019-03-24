
counter_unavailable = 0
wifi_problem = 'off'

wifi_devices = [
        'light.xiaomi_philips_desklamp_ambient_light',
        'light.mood_lamp',
        'light.xiaomi_philips_desklamp',
        'light.bed_led',
        'light.bulb_13',
        'light.bulb_15'
        ]

for entity_id in hass.states.entity_ids('light'):
    entity_state = hass.states.get(entity_id).state
    if entity_id in wifi_devices:
        logger.debug("WiFiProblem: Check device '%s' : %s ", entity_id, entity_state)
        if entity_state == 'unavailable':
            counter_unavailable = counter_unavailable + 1
            logger.debug("WiFiProblem: The device '%s' is not available", entity_id)

if counter_unavailable > 3:
    wifi_problem = 'on'
else:
    wifi_problem = 'off'

logger.debug("WiFiProblem: Set binary_sensor.wifi_problem to %s", wifi_problem)
hass.states.set('binary_sensor.wifi_problem', wifi_problem, {
    'friendly_name': 'WiFi Problem',
    'icon': 'mdi:wifi-off',
    'last_updated': datetime.datetime.now(), 
    'last_updated_epoch': time.time(),
    'unavailable_devices': counter_unavailable
})

#if counter_unavailable > 5:
#    logger.debug("WiFiProblem: The router will be restart")
#    service_data = { 'title': "Warning!", 'message': "Too many unavailable WiFi devices. Restart the router." }
#    hass.services.call('notify', 'pushover', service_data, False)
#    hass.services.call('shell_command', 'router_restart', { }, False)
