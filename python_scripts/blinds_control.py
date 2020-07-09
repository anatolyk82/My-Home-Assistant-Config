all_covers = [
        {
            "cover": "cover.blinds_workroom",                              # Blinds id
            "enable_switch": "input_boolean.workroom_blinds_auto",         # Switch which enables automation for this cover
            "enable_open": True,                                           # Can the automation open the cover
            "position_to_open": 25,                                        # Set this position when the cover is open:   100 - fully open
            "position_to_close": 0                                         # Set this position when the cover is closed: 0 - fully closed
        },
        {
            "cover": "cover.blinds_guestroom",
            "enable_switch":"input_boolean.guestroom_blinds_auto",
            "enable_open": True,
            "position_to_open": 25,
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


# Extra info of the intention
intention_info = data.get('intention_info')


# Get the state of the sun
sun = hass.states.get('sun.sun')
sunrise = utc2local(sun.attributes['next_rising'])
sunset = utc2local(sun.attributes['next_setting'])
logger.debug('[Blinds Control] Sun is %s. Next rising: %s, Next setting: %s', sun.state, sunrise, sunset)

delta_sunrise = (sunrise - now).total_seconds() / 60
logger.debug('[Blinds Control] Sunrise in %d minutes', delta_sunrise)

# Get state of all_in_bed
all_in_bed = hass.states.get('binary_sensor.all_in_bed').state

# Check cloudeness
cloudenessSensor = int(float(hass.states.get('sensor.yr_cloudiness').state))
isCloudy = False
if cloudenessSensor != 'unknown':
    isCloudy = cloudenessSensor > 35
    logger.debug('[Blinds Control] cloudeness=%d isCloudy=%s', cloudenessSensor, isCloudy)
else:
    isCloudy = False
    logger.debug('[Blinds Control] Cloudeness sensor is unavailable. Take isCloudy=%s', isCloudy)
    
# From which position a cover is considered as closed
# position = 0 - fully closed; position = 100 - fully open
thresholdCoverIsClosed = 100 #20
thresholdCoverIsOpen = 0 #80
        

for i in range(0, len(all_covers)):
    cover_id = all_covers[ i ]["cover"]
    automation_enabled = hass.states.get( all_covers[i]["enable_switch"] ).state
    logger.debug("[Blinds Control]: Automation of %s is %s", cover_id, automation_enabled )
    current_position = 100 # Assume that this cover is fully open
    if automation_enabled == "on":
        cover = hass.states.get( cover_id )

        # Fetch the current position
        if 'current_position' in cover.attributes:
            current_position = int(cover.attributes['current_position'])
            logger.debug("[Blinds Control]: Current position of %s is %d", cover_id, current_position)
        else:
            logger.error("[Blinds Control]: Failed to fetch the current position of %s. Assume that current_position is %d", cover_id, current_position)

        isOpenningEnabled = all_covers[i]["enable_open"]
        if isOpenningEnabled != True:
            logger.debug("[Blinds Control]: It is not allowed to open blinds %s", cover_id)

        position_to_open = all_covers[i]["position_to_open"]
        position_to_close = all_covers[i]["position_to_close"]

        # Logic to open/close a cover
        if intention == 'open' and isOpenningEnabled == True:
            if intention_info == 'before_sunrise_30' and isCloudy == False and current_position <= thresholdCoverIsClosed and all_in_bed == 'off':
                logger.debug("[Blinds Control]: The sky is clear. Open the cover %s 30 min before sunrise. Position: %d", cover_id, current_position)
                setCoverPosition(cover_id, position_to_open)

            if intention_info == 'before_sunrise_15' and current_position <= thresholdCoverIsClosed and all_in_bed == 'off':
                logger.debug("[Blinds Control]: Open the cover %s 15 min before sunrise. Position: %d", cover_id, current_position)
                setCoverPosition(cover_id, position_to_open)

            if intention_info == 'waken_up' and current_position <= thresholdCoverIsClosed and delta_sunrise < 30 and isCloudy == False:
                logger.debug("[Blinds Control]: The sky is clear, someone has waken up and it's %d minutes until sunrise. Open the cover %s. Position: %d", delta_sunrise, cover_id, current_position)
                setCoverPosition(cover_id, position_to_open)

            if intention_info == 'waken_up' and current_position <= thresholdCoverIsClosed and sun.state == 'above_horizon':
                logger.debug("[Blinds Control]: Someone has waken up and the sun has risen. Open the cover %s. Position: %d", cover_id, current_position)
                setCoverPosition(cover_id, position_to_open)

        elif intention == 'close':
            if intention_info == 'after_sunset_15' and isCloudy == True and current_position >= thresholdCoverIsOpen:
                logger.debug("[Blinds Control]: It's cloudy. Close the cover %s 15 min after sunset. Position: %d", cover_id, current_position)
                setCoverPosition(cover_id, position_to_close)

            if intention == 'close' and intention_info == 'after_sunset_30' and current_position >= thresholdCoverIsOpen:
                logger.debug("[Blinds Control]: Close the cover %s 30 min after sunset. Position: %d", cover_id, current_position)
                setCoverPosition(cover_id, position_to_close)
