import logging

import voluptuous as vol
import socket
import time
import errno

# Import the device class from the component that you want to support
from homeassistant.components.light import (ATTR_BRIGHTNESS, Light, PLATFORM_SCHEMA, SUPPORT_COLOR, SUPPORT_BRIGHTNESS, ATTR_HS_COLOR)
from homeassistant.const import CONF_HOST, CONF_NAME
import homeassistant.helpers.config_validation as cv
import homeassistant.util.color as color_util

# Home Assistant depends on 3rd party packages for API specific code.
#REQUIREMENTS = ['awesome_lights==1.2.3']

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_NAME): cv.string,
})

# https://developers.home-assistant.io/docs/en/creating_platform_example_light.html

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Magic Home platform."""
    hub = []
    hub.append(MagicHome(config))
    add_devices(hub)



class MagicHome(Light):
    """Representation of an Magic Home light."""

    def __init__(self, config):
        """Initialize an MagicHome."""
        self._host = config.get(CONF_HOST)    
        self._port = 5577
        self._name = config.get(CONF_NAME)    
        self._state = None
        self._hs = (0, 0)
        self._brightness = 100
        self._red = None
        self._green = None
        self._blue = None
        self._available = None
        self._attemptToConnect = 0
        self.__connectToLED()

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_BRIGHTNESS | SUPPORT_COLOR

    @property
    def name(self):
        """Return the display name of this light."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the light."""
        return int(255 * self._brightness / 100)

    @property
    def hs_color(self):
        """Return the hs color value."""
        return self._hs

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._state

    @property
    def available(self) -> bool:
        """Return if light is available."""
        return self._available

    def turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        msg = bytearray([0x71, 0x23, 0x0f])
        self.__write(msg)

        if ATTR_HS_COLOR in kwargs:
            self._hs = kwargs[ATTR_HS_COLOR]

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = int(100 * kwargs[ATTR_BRIGHTNESS] / 255)
        else:
            self._brightness = 100

        (self._red, self._green, self._blue) = color_util.color_hs_to_RGB(*self._hs)
        r = int(self._red * self._brightness / 100)
        g = int(self._green * self._brightness / 100)
        b = int(self._blue * self._brightness / 100)
        self.set_rgb(r, g, b)
        self._state = True

    def turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        msg = bytearray([0x71, 0x24, 0x0f])
        self.__write(msg)
        self._state = False


    def update(self):
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """
        msg = bytearray([0x81, 0x8a, 0x8b])
        self.__write(msg)
        rx = self.__readResponse(14)

        power_state = rx[2]
        if power_state == 0x23:
            self._state = True
        elif power_state == 0x24:
            self._state = False

        self._red = rx[6]
        self._green = rx[7]
        self._blue = rx[8]

        self._hs = color_util.color_RGB_to_hs(self._red, self._green, self._blue)

    def set_rgb(self, r, g, b) -> None:
        """Set bulb's color."""
        _LOGGER.debug("Setting RGB: %s,%s,%s", r, g, b)
        msg = bytearray([0x31])
        msg.append(r)
        msg.append(g)
        msg.append(b)
        msg.append(0x00)
        msg.append(0x00)
        msg.append(0xf0)
        msg.append(0x0f)
        self.__write(msg)


    def __writeRaw(self, bytes):
        try:
            self._socket.send(bytes)
            self._available = True
        except IOError as ioe:
            _LOGGER.error("IOError: %s %s", self._name, ioe)
            if ioe.errno == errno.EPIPE:
                self.__connectToLED()
        except Exception as ex:
            _LOGGER.error("Failed to send data to led %s, %s: %s", self._host, self._name, ex)
            self._available = False

    def __write(self, bytes):
        """Calculate checksum of byte array and add to end"""
        csum = sum(bytes) & 0xFF
        bytes.append(csum)
        self.__writeRaw(bytes)

    def __readResponse(self, expected):
        remaining = expected
        rx = bytearray()
        while remaining > 0:
            chunk = self.__readRaw(remaining)
            remaining -= len(chunk)
            rx.extend(chunk)
        return rx

    def __readRaw(self, byte_count=1024):
        rx = 0
        try:
            rx = self._socket.recv(byte_count)
            self._available = True
        except IOError as ioe:
            _LOGGER.error("IOError: %s %s", self._name, ioe)
            if ioe.errno == errno.EPIPE:
                self.__connectToLED()
        except Exception as ex:
            _LOGGER.error("Failed to receive data from led %s, %s: %s", self._host, self._name, ex)
            self._available = False
        return rx


    def __connectToLED(self):
        while self._attemptToConnect < 10:
            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.connect((self._host, self._port))
                self._available = True
                self._attemptToConnect = 0
                return
            except Exception as ex:
                _LOGGER.error("Failed (%s) to connect to led %s, %s: %s",self._attemptToConnect, self._host, self._name, ex)
                self._available = False
                self._attemptToConnect += 1
                time.sleep(5)
