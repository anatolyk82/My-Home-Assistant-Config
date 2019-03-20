"""
This component provides basic support for Foscam IP cameras.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/camera.foscam/
"""
import logging

import voluptuous as vol

from homeassistant.components.camera import (Camera, PLATFORM_SCHEMA, CAMERA_SERVICE_SCHEMA, DOMAIN)
from homeassistant.const import (
    CONF_NAME, CONF_USERNAME, CONF_PASSWORD, CONF_PORT)
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['libpyfoscam==1.0']

CONF_IP = 'ip'

DEFAULT_NAME = 'My Foscam Camera'
DEFAULT_PORT = 88

FOSCAM_COMM_ERROR = -8

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_IP): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a Foscam IP Camera."""
    camera = MyFoscamCam(config)

    def turn_on_infra(call):
        _LOGGER.debug("Calling turn on infra %s. This is %s", call.data.get('entity_id'), camera.entity_id)
        if call.data.get('entity_id') == camera.entity_id:
            camera.enable_infra_led()
            return True
        else:
            return False

    def turn_off_infra(call):
        _LOGGER.debug("Calling turn off infra %s. This is %s", call.data.get('entity_id'), camera.entity_id)
        if call.data.get('entity_id') == camera.entity_id:
            camera.disable_infra_led()
            return True
        else:
            return False

    hass.services.register( DOMAIN, 'turn_on_infra', turn_on_infra, schema=CAMERA_SERVICE_SCHEMA)
    hass.services.register( DOMAIN, 'turn_off_infra', turn_off_infra, schema=CAMERA_SERVICE_SCHEMA )
    _LOGGER.debug("Registering turn_on_infra and turn_off_infra services for %s", camera.entity_id)
    
    add_entities([camera])


class MyFoscamCam(Camera):
    """An implementation of a Foscam IP camera."""

    def __init__(self, device_info):
        """Initialize a Foscam camera."""
        from custom_components.myfoscam.libmyfoscam import FoscamCamera

        super(MyFoscamCam, self).__init__()

        ip_address = device_info.get(CONF_IP)
        port = device_info.get(CONF_PORT)
        self._username = device_info.get(CONF_USERNAME)
        self._password = device_info.get(CONF_PASSWORD)
        self._name = device_info.get(CONF_NAME)
        self._motion_status = False
        self._infra_status = True

        self._foscam_session = FoscamCamera(
            ip_address, port, self._username, self._password, verbose=False)

    def camera_image(self):
        """Return a still image response from the camera."""
        # Send the request to snap a picture and return raw jpg data
        # Handle exception if host is not reachable or url failed
        result, response = self._foscam_session.snap_picture_2()
        if result == FOSCAM_COMM_ERROR:
            return None

        return response

    @property
    def infra_led_enabled(self):
        """Infrared led Status."""
        return self._infra_status

    def enable_infra_led(self):
        """Enable Infrared led in camera."""
        try:
            ret = self._foscam_session.open_infra_led()
            self._infra_status = ret == FOSCAM_COMM_ERROR
        except TypeError:
            _LOGGER.debug("Communication problem")
            self._infra_status = False

    def disable_infra_led(self):
        """Disable Infrared led in camera."""
        try:
            ret = self._foscam_session.close_infra_led()
            self._infra_status = ret == FOSCAM_COMM_ERROR
        except TypeError:
            _LOGGER.debug("Communication problem")
            self._infra_status = False

    @property
    def motion_detection_enabled(self):
        """Camera Motion Detection Status."""
        return self._motion_status

    def enable_motion_detection(self):
        """Enable motion detection in camera."""
        try:
            ret = self._foscam_session.enable_motion_detection()
            self._motion_status = ret == FOSCAM_COMM_ERROR
        except TypeError:
            _LOGGER.debug("Communication problem")
            self._motion_status = False

    def disable_motion_detection(self):
        """Disable motion detection."""
        try:
            ret = self._foscam_session.disable_motion_detection()
            self._motion_status = ret == FOSCAM_COMM_ERROR
        except TypeError:
            _LOGGER.debug("Communication problem")
            self._motion_status = False

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name
