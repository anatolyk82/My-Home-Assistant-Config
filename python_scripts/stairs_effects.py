
motion_entity_id = data.get('entity_id')
to_state = data.get('to_state')
#delayed_run = int(data.get('delayed'))

logger.debug("[StairsLight]: %s is turning %s", motion_entity_id, to_state)

# Get information about darkness
lightlevel_upstairs = float(hass.states.get('sensor.lightlevel_upstairs').state)
lightlevel_downstairs = float(hass.states.get('sensor.lightlevel_livingroom').state)
lightlevel_threshold = 8
is_upstairs_dark = lightlevel_upstairs < lightlevel_threshold 
is_downstairs_dark = lightlevel_downstairs < lightlevel_threshold

# Get information about last updates on the motion sensors
motion_upstairs_last_updated = hass.states.get('binary_sensor.motion_upstairs').last_updated
motion_downstairs_last_updated = hass.states.get('binary_sensor.motion_downstairs').last_updated

# Get the light object
light_stairs = hass.states.get('light.stairs')


def dimDown(hass):
    service_data = { 'entity_id':'light.stairs', 'effect':'DimDown' }
    hass.services.call('light', 'turn_on', service_data, False)

def dimUp(hass):
    service_data = { 'entity_id':'light.stairs', 'effect':'DimUp' }
    hass.services.call('light', 'turn_on', service_data, False)

# Define light effects
future_effect_to_on = 'LightUp'
future_effect_to_off = 'DimUp'
if motion_entity_id == 'binary_sensor.motion_upstairs':
    future_effect_to_on = 'LightDown'
    future_effect_to_off = 'DimDown'


# Choose color and brightness
now = datetime.datetime.now()
today_00_00 = now.replace(hour=0, minute=0, second=0, microsecond=0)
today_07_30 = now.replace(hour=6, minute=30, second=0, microsecond=0)

brightness = 255
rgb_color = [255, 255, 0]
if now > today_00_00 and now < today_07_30:
    brightness = 100
    rgb_color = [255, 0, 0]


# Check if it's dark enough to turn on the light
if to_state == 'on' and is_upstairs_dark and is_downstairs_dark:
    if light_stairs.state == 'on' and light_stairs.attributes["effect"] != 'StartLight' and light_stairs.attributes["effect"] != 'EndLight' and light_stairs.attributes["effect"] != 'NightLight':
        logger.debug("[StairsLight]: The light is already on")
    else:
        logger.debug("[StairsLight]: Turn on the light")
        service_data = {
                'entity_id':'light.stairs',
                'brightness':brightness,
                'rgb_color':rgb_color,
                'effect':future_effect_to_on,
                }
        hass.services.call('light', 'turn_on', service_data, False)
elif to_state == 'on':
    logger.debug("[StairsLight] It's not dark enough to turn on the light")


if to_state == 'off':
    if light_stairs.state == 'on' and (light_stairs.attributes["effect"] == "LightDown" or light_stairs.attributes["effect"] == "LightUp"):
        if motion_entity_id == 'binary_sensor.motion_downstairs' and motion_downstairs_last_updated > motion_upstairs_last_updated:
            logger.debug("[StairsLight] Apply the DimDown effect to turn off the light")
            dimDown(hass)

        elif motion_entity_id == 'binary_sensor.motion_upstairs' and motion_upstairs_last_updated > motion_downstairs_last_updated:
            logger.debug("[StairsLight] Apply the DimUp effect to turn off the light")
            dimUp(hass)




