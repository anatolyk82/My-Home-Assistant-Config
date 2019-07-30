# STAIRS NIGHT LIGHTS

to_state = data.get('to_state')

# Get information how dark it is
lightlevel_threshold = 10
lightlevel_upstairs = float(hass.states.get('sensor.lightlevel_upstairs').state)
lightlevel_livingroom = float(hass.states.get('sensor.lightlevel_livingroom').state)
lightlevel_kitchen = float(hass.states.get('sensor.lightlevel_kitchen').state)
is_upstairs_dark = lightlevel_upstairs < lightlevel_threshold 
is_downstairs_dark = (lightlevel_livingroom < lightlevel_threshold) and (lightlevel_kitchen < lightlevel_threshold)

light_stairs = hass.states.get('light.stairs')
light_stairs_state = light_stairs.state

# Check current time 
now = datetime.datetime.now()
today_23_00 = now.replace(hour=23, minute=0, second=0, microsecond=0)
today_07_00 = now.replace(hour=6, minute=30, second=0, microsecond=0)

if now > today_23_00 or now < today_07_00:
    if to_state == 'on' and light_stairs_state == 'off':
        if is_downstairs_dark and is_upstairs_dark:
            logger.debug("[StairsLight: NightLight]: Turn on NightLight")
            service_data = {
                    'entity_id':'light.stairs',
                    'brightness':255,
                    'rgb_color':[255, 0, 0],
                    'effect':'NightLight'
                    }
            hass.services.call('light', 'turn_on', service_data, False)
    elif to_state == 'on' and light_stairs_state == 'on':
        logger.debug("[StairsLight: NightLight]: Detected motion upstairs but the stairs light is on")
    elif to_state == 'off' and light_stairs_state == 'on' and (light_stairs.attributes["effect"] == 'EndLight' or light_stairs.attributes["effect"] == 'StartLight' or light_stairs.attributes["effect"] == 'NightLight'):
        logger.debug("[StairsLight: NightLight]: Turn off the stairs light")
        hass.services.call('light', 'turn_off', {'entity_id':'light.stairs'}, False)
