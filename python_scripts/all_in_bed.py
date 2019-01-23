
all_in_bed = 'on'

# Check the alarm state
alarm_state = hass.states.get('alarm_control_panel.house').state
if alarm_state == 'armed_away':
    all_in_bed = 'off'
    logger.debug("AllInBed: Alarm is armed as 'armed_away'. Set the sensor to off")


# Check all illumination sensors if their values are below 10
# Illumination is checked only if the sensor is off. It allows to avoid
# unexpecting turning off in the morning whenn all are still in bed
all_in_bed_current_state = hass.states.get('binary_sensor.all_in_bed').state
if all_in_bed_current_state == 'off' and all_in_bed == 'on':
    for entity_id in hass.states.entity_ids('sensor'):
        if entity_id.find('illumination') >= 0:
            # Ignore Xiaomi gateway
            if entity_id.find('7811dcb7f720') >= 0:
                continue
            illumination_state = hass.states.get(entity_id)
            if illumination_state.state == 'unknown':
                continue
            if float(illumination_state.state) > 10:
                all_in_bed = 'off'
                logger.debug("AllInBed: Illumination for '%s' is above 10. Set the sensor to off", entity_id)
                break


# Check some lamps if they are on
# Living room
if hass.states.get('light.bulb_16').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Living room light is on. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('light.bulb_14').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Living room light is on. Set the sensor to off")
    all_in_bed = 'off'

# Entrance
if hass.states.get('light.ikea_lamp_2').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Entrance light is on. Set the sensor to off")
    all_in_bed = 'off'

# Second floor
if hass.states.get('light.ikea_lamp_1').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Second floor light is on. Set the sensor to off")
    all_in_bed = 'off'

# Work room
if hass.states.get('light.bulb_15').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Workroom light is on. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('light.xiaomi_philips_desklamp').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Desktop lamp is on. Set the sensor to off")
    all_in_bed = 'off'

# Bedroom
if hass.states.get('light.bulb_13').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Bedroom light is on. Set the sensor to off")
    all_in_bed = 'off'

if hass.states.get('light.bed_led').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: BedLED light is on. Set the sensor to off")
    all_in_bed = 'off'

# Room
if hass.states.get('light.bulb_17').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Room light is on. Set the sensor to off")
    all_in_bed = 'off'

# Kitchen 1
if hass.states.get('light.kitchen_lights_1').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Kitchen lights 1 is on. Set the sensor to off")
    all_in_bed = 'off'

# Kitchen 2
if hass.states.get('light.kitchen_lights_2').state == 'on' and all_in_bed == 'on':
    logger.debug("AllInBed: Kitchen lights 2 is on. Set the sensor to off")
    all_in_bed = 'off'

# Check the media player
if hass.states.get('media_player.sirius').state != 'off' and all_in_bed == 'on':
    logger.debug("AllInBed: The media player 'Sirius' is on. Set the sensor to off")
    all_in_bed = 'off'


# Check if there is any motion except the bedroom
for entity_id in hass.states.entity_ids('binary_sensor'):
    if entity_id.find('motion_sensor') >= 0:
        # Ignore motion sensor in the bedroom  
        if entity_id.find('158d000236a59e') >= 0:
            continue
        motion_state = hass.states.get(entity_id)
        if motion_state.state == 'on':
            logger.debug("AllInBed: There is motion on %s. Set the sensor to off", entity_id)
            all_in_bed = 'off'
            break


logger.debug("AllInBed: Set binary_sensor.all_in_bed to %s", all_in_bed)
hass.states.set('binary_sensor.all_in_bed', all_in_bed, {
    'friendly_name': 'Everyone in bed',
    'icon': 'mdi:hotel'
})

