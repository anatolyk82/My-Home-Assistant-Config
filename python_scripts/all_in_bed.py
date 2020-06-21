
all_in_bed = 'on'

def utc2local(dt):
    return dt - datetime.timedelta(seconds = time.timezone)


# Check time (only between 22:00 - 10:00 it starts checking)
now = datetime.datetime.now()
today_10_00 = now.replace(hour=10, minute=0, second=0, microsecond=0)
today_22_00 = now.replace(hour=22, minute=0, second=0, microsecond=0)
if now > today_10_00 and now < today_22_00:
    all_in_bed = 'off'
    logger.debug("[All In Bed] Current time is between 10:00 and 22:00. Set the sensor to off")


# Check the alarm state
alarm_state = hass.states.get('alarm_control_panel.house').state
if alarm_state == 'armed_away':
    all_in_bed = 'off'
    logger.debug("[All In Bed] Alarm is armed as 'armed_away'. Set the sensor to off")


# Check all illumination sensors if their values are below 10
# Illumination is checked only if the sensor is off. It allows to avoid
# unexpecting turning off in the morning whenn all are still in bed
all_in_bed_current_state = hass.states.get('binary_sensor.all_in_bed').state
if hass.states.get('binary_sensor.all_in_bed') == None:
    all_in_bed_current_state = 'off'
if all_in_bed_current_state == 'off' and all_in_bed == 'on':
    for entity_id in hass.states.entity_ids('sensor'):
        if entity_id.find('lightlevel') >= 0:
            lightlevel_state = hass.states.get(entity_id)
            if entity_id == 'sensor.lightlevel_backyard':
                continue
            logger.debug("[All In Bed] Illumination for '%s' is %s", entity_id, lightlevel_state.state)
            if lightlevel_state.state == 'unknown' or lightlevel_state.state == 'unavailable':
                continue
            logger.debug("[All In Bed] Check for illumination for '%s'", entity_id)
            if float(lightlevel_state.state) > 10:
                all_in_bed = 'off'
                logger.debug("[All In Bed] Illumination for '%s' is above 10. Set the sensor to off", entity_id)
                break


# Check some lamps if they are on
# Living room
if hass.states.get('light.gledopto_lamp_1').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Living room light is on. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('light.gledopto_lamp_2').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Living room light is on. Set the sensor to off")
    all_in_bed = 'off'

# Entrance
if hass.states.get('light.ikea_lamp_2').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Entrance light is on. Set the sensor to off")
    all_in_bed = 'off'

# Second floor
if hass.states.get('light.ikea_lamp_1').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Second floor light is on. Set the sensor to off")
    all_in_bed = 'off'

# Work room
if hass.states.get('light.ikea_lamp_13').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Workroom light is on. Set the sensor to off")
    all_in_bed = 'off'

#if hass.states.get('light.xiaomi_philips_desklamp').state == 'on' and all_in_bed == 'on':
#    logger.debug("[All In Bed] Desktop lamp is on. Set the sensor to off")
#    all_in_bed = 'off'

# Bedroom
if hass.states.get('light.gledopto_lamp_4').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Bedroom light is on. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('light.bed_led').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] BedLED light is on. Set the sensor to off")
    all_in_bed = 'off'

# Room
if hass.states.get('light.gledopto_lamp_3').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Guest room light is on. Set the sensor to off")
    all_in_bed = 'off'

# Kitchen 1
if hass.states.get('light.kitchen_lights_1').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Kitchen lights 1 is on. Set the sensor to off")
    all_in_bed = 'off'

# Kitchen 2
if hass.states.get('light.kitchen_lights_2').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] Kitchen lights 2 is on. Set the sensor to off")
    all_in_bed = 'off'

# Check the media player
if hass.states.get('media_player.sirius').state != 'off' and all_in_bed == 'on':
    logger.debug("[All In Bed] The media player 'Sirius' is on. Set the sensor to off")
    all_in_bed = 'off'


# Check if all doors are closed. Nobody sleeps with open doors =)
# Check all doors manually to avoid mixing with window sensors in future
if hass.states.get('binary_sensor.openclose_entrance').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] The entrance door is open. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('binary_sensor.openclose_kitchen').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] The kitchen door is open. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('binary_sensor.openclose_livingroom').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] The living room door is open. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('binary_sensor.openclose_storehouse').state == 'on' and all_in_bed == 'on':
    logger.debug("[All In Bed] The store house door is open. Set the sensor to off")
    all_in_bed = 'off'


# Check if there is any motion except the bedroom
if all_in_bed == 'on':
    for entity_id in hass.states.entity_ids('binary_sensor'):
        if entity_id.find('presence') >= 0:
            # Ignore motion sensor in the bedroom  
            if entity_id.find('bedroom') >= 0:
                continue
            motion_state = hass.states.get(entity_id)
            if motion_state.state == 'on':
                logger.debug("[All In Bed] There is motion on %s. Set the sensor to off", entity_id)
                all_in_bed = 'off'
                break


# All motion sensors show last update more than 10 minutes ago
minutes_last_update = 10
if all_in_bed == 'on':
    for entity_id in hass.states.entity_ids('binary_sensor'):
        if entity_id.find('presence') >= 0:
            # Ignore motion sensor in the bedroom  
            if entity_id.find('bedroom') >= 0:
                continue
            entityState = hass.states.get(entity_id)
            lu = entityState.last_updated.replace(tzinfo=None)
            now = datetime.datetime.now()
            diff_secs = (now - lu).total_seconds() - 7200 #HACK: 7200 - 2 hours is the difference between stockholm and UTC times
            logger.debug("[All In Bed] Last update of the sensor %s was at %s. Now it's %s so it was %d seconds ago", entity_id, lu, now, diff_secs)
            if diff_secs < minutes_last_update * 60:
                logger.debug("[All In Bed] There was motion on %s less than %d minutes ago. Set the sensor to off", entity_id, minutes_last_update)
                all_in_bed = 'off'
                break


logger.debug("[All In Bed] Set binary_sensor.all_in_bed to %s", all_in_bed)
hass.states.set('binary_sensor.all_in_bed', all_in_bed, {
    'friendly_name': 'Everyone in bed',
    'icon': 'mdi:hotel'
})

