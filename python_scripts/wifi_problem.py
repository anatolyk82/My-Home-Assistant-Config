
counter_unavailable = 0

for entity_id in hass.states.entity_ids('light'):
    entity_state = hass.states.get(entity_id).state
    logger.debug("WiFiProblem: Check device '%s' : %s ", entity_id, entity_state)
    if entity_state == 'unavailable':
        counter_unavailable = counter_unavailable + 1
        logger.debug("WiFiProblem: The device '%s' is not available", entity_id)

if counter_unavailable > 5:
    logger.debug("WiFiProblem: The router will be restart")
    service_data = { 'title': "Warning!", 'message': "Too many unavailable WiFi devices. Restart the router." }
    hass.services.call('notify', 'pushover', service_data, False)
    hass.services.call('shell_command', 'router_restart', { }, False)

