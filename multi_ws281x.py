# Adafruit NeoPixel library port to the rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)
import _rpi_ws281x as ws
import atexit

class mRGBW(int):
    def __new__(self, r, g=None, b=None, w=None):
        if (g, b, w) == (None, None, None):
            return int.__new__(self, r)
        else:
            if w is None:
                w = 0
            return int.__new__(self, (w << 24) | (r << 16) | (g << 8) | b)

    @property
    def r(self):
        return (self >> 16) & 0xff

    @property
    def g(self):
        return (self >> 8) & 0xff

    @property
    def b(self):
        return (self) & 0xff

    @property
    def w(self):
        return (self >> 24) & 0xff


def mColor(red, green, blue, white=0):
    return mRGBW(red, green, blue, white)


class mPixelStrip:
    def __init__(self, c0pin, c1pin, c0count, c1count):
        freq_hz=800000
        dma=10
        invert=False
        brightness=255
        strip_type=None
        gamma=None
        
        if gamma is None:
            if type(strip_type) is list and len(strip_type) == 256:
                gamma = strip_type
                strip_type = None
            else:
                gamma = list(range(256))

        if strip_type is None:
            strip_type = ws.WS2811_STRIP_GRB

        # Create ws2811_t structure and fill in parameters.
        self._leds = ws.new_ws2811_t()
        
        self._c0count = c0count
        self._c1count = c1count
        
        for channum in range(2):
            chan = ws.ws2811_channel_get(self._leds, channum)
            ws.ws2811_channel_t_count_set(chan, 0)
            ws.ws2811_channel_t_gpionum_set(chan, 0)
            ws.ws2811_channel_t_invert_set(chan, 0)
            ws.ws2811_channel_t_brightness_set(chan, 0)

        self._channels= []
        self._channels.append( ws.ws2811_channel_get(self._leds, 0))
        self._channels.append( ws.ws2811_channel_get(self._leds, 1))

        ws.ws2811_channel_t_gamma_set(self._channels[0], gamma)
        ws.ws2811_channel_t_count_set(self._channels[0], c0count)
        ws.ws2811_channel_t_gpionum_set(self._channels[0], c0pin)
        ws.ws2811_channel_t_invert_set(self._channels[0], 0 if not invert else 1)
        ws.ws2811_channel_t_brightness_set(self._channels[0], brightness)
        ws.ws2811_channel_t_strip_type_set(self._channels[0], strip_type)
        
        ws.ws2811_channel_t_gamma_set(self._channels[1], gamma)
        ws.ws2811_channel_t_count_set(self._channels[1], c1count)
        ws.ws2811_channel_t_gpionum_set(self._channels[1], c1pin)
        ws.ws2811_channel_t_invert_set(self._channels[1], 0 if not invert else 1)
        ws.ws2811_channel_t_brightness_set(self._channels[1], brightness)
        ws.ws2811_channel_t_strip_type_set(self._channels[1], strip_type)

        # Initialize the controller
        ws.ws2811_t_freq_set(self._leds, freq_hz)
        ws.ws2811_t_dmanum_set(self._leds, dma)

        # Substitute for __del__, traps an exit condition and cleans up properly
        atexit.register(self._cleanup)
        
    def _cleanup(self):
        # Clean up memory used by the library when not needed anymore.
        if self._leds is not None:
            ws.ws2811_fini(self._leds)
            ws.delete_ws2811_t(self._leds)
            self._leds = None
            self._channels[0] = None
            self._channels[1] = None
            self._channels = None

    def begin(self):
        resp = ws.ws2811_init(self._leds)
        if resp != 0:
            str_resp = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, str_resp))

    def show(self):
        """Update the display with the data from the LED buffer."""
        resp = ws.ws2811_render(self._leds)
        if resp != 0:
            str_resp = ws.ws2811_get_return_t_str(resp)
            raise RuntimeError('ws2811_render failed with code {0} ({1})'.format(resp, str_resp))

    def setPixelColor(self, ch, n, color):
        return ws.ws2811_led_set(self._channels[ch], n, color)
        
    def getPixelColor(self, ch, n):
        return ws.ws2811_led_get(self._channels[ch], n)

    def numPixels(self, ch):
        return ws.ws2811_channel_t_count_get(self._channels[ch])


# Shim for back-compatibility
class Adafruit_NeoPixel(mPixelStrip):
    pass
