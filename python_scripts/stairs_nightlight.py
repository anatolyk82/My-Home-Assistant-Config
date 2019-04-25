
motion_entity_id = data.get('entity_id')
to_state = data.get('to_state')

# Get additional values from sensors
lightlevel_upstairs = float(hass.states.get('sensor.lightlevel_upstairs').state)
lightlevel_livingroom = float(hass.states.get('sensor.lightlevel_livingroom').state)
lightlevel_kitchen = float(hass.states.get('sensor.lightlevel_kitchen').state)
lightlevel_threshold = 8
is_upstairs_dark = lightlevel_upstairs < lightlevel_threshold 
is_downstairs_dark = (lightlevel_livingroom < lightlevel_threshold) and (lightlevel_kitchen < 10)

light_stairs = hass.states.get('light.stairs')
light_stairs_state = light_stairs.state

# Check current time 
now = datetime.datetime.now()
today_23_00 = now.replace(hour=23, minute=0, second=0, microsecond=0)
today_06_30 = now.replace(hour=6, minute=30, second=0, microsecond=0)

if now > today_23_00 or now < today_06_30:
    if to_state == 'on' and light_stairs_state == 'off':
        if motion_entity_id == 'binary_sensor.presence_livingroom' and is_downstairs_dark:
            logger.debug("[StairsLight: NightLight]: Turn on NightLight")
            service_data = {
                    'entity_id':'light.stairs',
                    'brightness':255,
                    'rgb_color':[255, 0, 0],
                    'effect':'NightLight'
                    } #EndLight
            hass.services.call('light', 'turn_on', service_data, False)
        elif motion_entity_id == 'binary_sensor.presence_livingroom' and not is_downstairs_dark:
            logger.debug("[StairsLight: NightLight]: Detected motion in the Living room but it's not dark enough")
        elif motion_entity_id == 'binary_sensor.presence_upstairs' and is_upstairs_dark:
            logger.debug("[StairsLight: NightLight]: Turn on NightLight")
            service_data = {
                    'entity_id':'light.stairs',
                    'brightness':255,
                    'rgb_color':[255, 0, 0],
                    'effect':'NightLight'
                    } #StartLight
            hass.services.call('light', 'turn_on', service_data, False)
        elif motion_entity_id == 'binary_sensor.presence_upstairs' and not is_upstairs_dark:
            logger.debug("[StairsLight: NightLight]: Detected motion upstairs but it's not dark enough")
    elif to_state == 'on' and light_stairs_state == 'on':
        logger.debug("[StairsLight: NightLight]: Detected motion upstairs but the stairs light is on")
    elif to_state == 'off' and light_stairs_state == 'on' and (light_stairs.attributes["effect"] == 'EndLight' or light_stairs.attributes["effect"] == 'StartLight' or light_stairs.attributes["effect"] == 'NightLight'):
        logger.debug("[StairsLight: NightLight]: Turn off the stairs light")
        hass.services.call('light', 'turn_off', {'entity_id':'light.stairs'}, False)
