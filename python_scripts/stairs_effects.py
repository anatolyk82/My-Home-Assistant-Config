
to_state = 'on' #By default. It will be checked below wether it's true

m_upstairs = hass.states.get('binary_sensor.motion_upstairs')
m_downstairs = hass.states.get('binary_sensor.motion_downstairs')

# Get current states of the sensors
m_upstairs_state = m_upstairs.state
m_downstairs_state = m_downstairs.state

# Get information about last updates on the motion sensors
m_upstairs_last_updated = hass.states.get('binary_sensor.motion_upstairs').last_updated
m_downstairs_last_updated = hass.states.get('binary_sensor.motion_downstairs').last_updated


# Get information how dark it is
lightlevel_threshold = 10
lightlevel_upstairs = float(hass.states.get('sensor.lightlevel_upstairs').state)
lightlevel_livingroom = float(hass.states.get('sensor.lightlevel_livingroom').state)
lightlevel_kitchen = float(hass.states.get('sensor.lightlevel_kitchen').state)
is_upstairs_dark = lightlevel_upstairs < lightlevel_threshold 
is_downstairs_dark = (lightlevel_livingroom < lightlevel_threshold) and (lightlevel_kitchen < lightlevel_threshold)


# Get the light object
light_stairs = hass.states.get('light.stairs')


def dimDown(hass):
    service_data = { 'entity_id':'light.stairs', 'effect':'DimDown' }
    hass.services.call('light', 'turn_on', service_data, False)

def dimUp(hass):
    service_data = { 'entity_id':'light.stairs', 'effect':'DimUp' }
    hass.services.call('light', 'turn_on', service_data, False)


if m_downstairs_last_updated > m_upstairs_last_updated:
    to_state = m_downstairs_state
    trigger_entity_id = 'binary_sensor.motion_downstairs'
else:
    to_state = m_upstairs_state
    trigger_entity_id = 'binary_sensor.motion_upstairs'

logger.debug("[StairsLight]: %s is turning %s", trigger_entity_id, to_state)

# Define light effects
future_effect_to_on = 'LightUp'
future_effect_to_off = 'DimUp'
if trigger_entity_id == 'binary_sensor.motion_upstairs':
    future_effect_to_on = 'LightDown'
    future_effect_to_off = 'DimDown'


# Choose color and brightness
now = datetime.datetime.now()
today_23_30 = now.replace(hour=23, minute=30, second=0, microsecond=0)
today_07_30 = now.replace(hour=6, minute=30, second=0, microsecond=0)

brightness = 255
rgb_color = [255, 255, 0]
if now > today_23_30 and now < today_07_30:
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
        if trigger_entity_id == 'binary_sensor.motion_downstairs':
            logger.debug("[StairsLight] Apply the DimDown effect to turn off the light")
            dimDown(hass)

        elif trigger_entity_id == 'binary_sensor.motion_upstairs':
            logger.debug("[StairsLight] Apply the DimUp effect to turn off the light")
            dimUp(hass)


