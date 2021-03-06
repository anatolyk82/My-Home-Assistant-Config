all_covers = [
        {
            "cover": "cover.blinds_workroom",                                            # Blinds id
            "close_automation_switch": "input_boolean.workroom_close_blinds_automation", # Switch which enables automation for this cover
            "open_automation_switch": "input_boolean.workroom_open_blinds_automation",   # Switch which enables automation for this cover
            "position_to_open": 100,                                                      # Set this position when the cover is open:   100 - fully open
            "position_to_close": 0                                                       # Set this position when the cover is closed: 0 - fully closed
        },
        {
            "cover": "cover.blinds_guestroom",
            "close_automation_switch": "input_boolean.guestroom_close_blinds_automation",
            "open_automation_switch": "input_boolean.guestroom_open_blinds_automation",
            "position_to_open": 100,
            "position_to_close": 0
        },    
        {
            "cover": "cover.blinds_bedroom_left",
            "close_automation_switch": "input_boolean.guestroom_close_blinds_automation",
            "open_automation_switch": "input_boolean.guestroom_open_blinds_automation",
            "position_to_open": 100,
            "position_to_close": 0
        },    
    ]

def utc2local(utc_td):
    now = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    offset_sec = (now - utcnow).total_seconds()
    local_td = datetime.datetime.strptime(utc_td, '%Y-%m-%dT%H:%M:%S+00:00') + datetime.timedelta(seconds=offset_sec)
    return local_td

def setCoverPosition(cover_id, position):
    service_data = { 'entity_id': cover_id, 'position': position }
    hass.services.call('cover', 'set_cover_position', service_data, False)


# Get time
now = datetime.datetime.now()
utcnow = datetime.datetime.utcnow()
offset_sec = (now - utcnow).total_seconds()

# Intention: 'open' or 'close'
intention = data.get('intention')
if intention == None:
    today_15_00 = now.replace(hour=15, minute=0, second=0, microsecond=0)
    if now > today_15_00:
        intention = 'close'
    else:
        intention = 'open'
    logger.debug('[Blinds Control] The intention is unknown but it assumes to %s the blinds', intention)
else:
    logger.debug('[Blinds Control] The intention is to %s the blinds', intention)



# Get the state of the sun
sun = hass.states.get('sun.sun')
sunrise = utc2local(sun.attributes['next_rising'])
sunset = utc2local(sun.attributes['next_setting'])
logger.debug('[Blinds Control] Sun is %s. Next rising: %s, Next setting: %s', sun.state, sunrise, sunset)

delta_sunrise = (sunrise - now).total_seconds() / 60
logger.debug('[Blinds Control] Sunrise in %d minutes', delta_sunrise)

# Get state of all_in_bed
all_in_bed = hass.states.get('binary_sensor.all_in_bed').state


for i in range(0, len(all_covers)):
    cover_id = all_covers[ i ]["cover"]
    open_automation = hass.states.get( all_covers[i]["open_automation_switch"] ).state
    close_automation = hass.states.get( all_covers[i]["close_automation_switch"] ).state
    
    current_position = 100 # Assume that this cover is fully open

    cover = hass.states.get( cover_id )

    # Fetch the current position
    if 'current_position' in cover.attributes:
        current_position = int(cover.attributes['current_position'])
        logger.debug("[Blinds Control]: Current position of %s is %d", cover_id, current_position)
    else:
        logger.error("[Blinds Control]: Failed to fetch the current position of %s. Assume that current_position is %d", cover_id, current_position)

    position_to_open = all_covers[i]["position_to_open"]
    position_to_close = all_covers[i]["position_to_close"]

    # Logic to open/close a cover
    if intention == 'open' and open_automation == 'on':
        setCoverPosition(cover_id, position_to_open)

    elif intention == 'close' and close_automation == 'on':
        setCoverPosition(cover_id, position_to_close)
