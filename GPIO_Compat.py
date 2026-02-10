"""
GPIO Abstraction Layer for Maximum Hardware Compatibility

Supports both lgpio (modern, Pi 5 compatible) and RPi.GPIO (legacy) backends.
Automatically selects the best available backend.
"""
import logging

logger = logging.getLogger(__name__)

# Try lgpio first (Pi 5 support, modern), fall back to RPi.GPIO (legacy)
try:
    import lgpio
    BACKEND = 'lgpio'
    logger.info("Using lgpio backend (Pi 5 compatible, recommended)")
except ImportError:
    try:
        import RPi.GPIO as GPIO
        BACKEND = 'RPi.GPIO'
        logger.warning("Using RPi.GPIO backend (legacy, no Pi 5 support)")
    except ImportError:
        raise ImportError(
            "No GPIO library available. Install lgpio or RPi.GPIO:\n"
            "  sudo apt install python3-lgpio\n"
            "  or\n"
            "  sudo apt install python3-rpi.gpio"
        )


class GPIOInterface:
    """Unified GPIO interface supporting multiple backends"""

    # Mode constants
    BCM = 'BCM'
    BOARD = 'BOARD'

    # Level constants
    HIGH = 1
    LOW = 0

    # Direction constants
    IN = 'IN'
    OUT = 'OUT'

    # Pull-up/down constants
    PUD_OFF = 'PUD_OFF'
    PUD_UP = 'PUD_UP'
    PUD_DOWN = 'PUD_DOWN'

    def __init__(self):
        """Initialize GPIO backend"""
        self.backend = BACKEND

        if self.backend == 'lgpio':
            # Open GPIO chip (gpiochip0 is standard for all Pi models)
            try:
                self.handle = lgpio.gpiochip_open(0)
                logger.info("lgpio: Successfully opened GPIO chip 0")
            except Exception as e:
                logger.error(f"lgpio: Failed to open GPIO chip: {e}")
                raise
        else:
            # RPi.GPIO initialization
            GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
            GPIO.setwarnings(False)  # Suppress warnings
            logger.info("RPi.GPIO: Initialized in BCM mode")

    def setup(self, pin, mode, pull_up_down=None):
        """
        Setup a GPIO pin

        Args:
            pin: GPIO pin number (BCM numbering)
            mode: GPIO.IN or GPIO.OUT
            pull_up_down: Optional pull resistor (PUD_UP, PUD_DOWN, or PUD_OFF)
        """
        if self.backend == 'lgpio':
            if mode == self.IN:
                # Configure as input with optional pull resistor
                flags = 0
                if pull_up_down == self.PUD_UP:
                    flags = lgpio.SET_PULL_UP
                elif pull_up_down == self.PUD_DOWN:
                    flags = lgpio.SET_PULL_DOWN
                lgpio.gpio_claim_input(self.handle, pin, flags)
                logger.debug(f"lgpio: Pin {pin} configured as INPUT with flags {flags}")
            else:
                # Configure as output
                lgpio.gpio_claim_output(self.handle, pin)
                logger.debug(f"lgpio: Pin {pin} configured as OUTPUT")
        else:
            # RPi.GPIO setup
            pud = GPIO.PUD_OFF
            if pull_up_down == self.PUD_UP:
                pud = GPIO.PUD_UP
            elif pull_up_down == self.PUD_DOWN:
                pud = GPIO.PUD_DOWN

            gpio_mode = GPIO.IN if mode == self.IN else GPIO.OUT
            GPIO.setup(pin, gpio_mode, pull_up_down=pud)
            logger.debug(f"RPi.GPIO: Pin {pin} configured as {'INPUT' if mode == self.IN else 'OUTPUT'}")

    def input(self, pin):
        """
        Read GPIO pin state

        Args:
            pin: GPIO pin number (BCM numbering)

        Returns:
            0 or 1 (LOW or HIGH)
        """
        if self.backend == 'lgpio':
            return lgpio.gpio_read(self.handle, pin)
        else:
            return GPIO.input(pin)

    def output(self, pin, value):
        """
        Set GPIO pin state

        Args:
            pin: GPIO pin number (BCM numbering)
            value: 0/1, LOW/HIGH, False/True
        """
        if self.backend == 'lgpio':
            lgpio.gpio_write(self.handle, pin, int(value))
        else:
            GPIO.output(pin, value)

    def cleanup(self):
        """Clean up GPIO resources"""
        if self.backend == 'lgpio':
            try:
                lgpio.gpiochip_close(self.handle)
                logger.info("lgpio: GPIO chip closed")
            except Exception as e:
                logger.error(f"lgpio: Error during cleanup: {e}")
        else:
            try:
                GPIO.cleanup()
                logger.info("RPi.GPIO: Cleanup complete")
            except Exception as e:
                logger.error(f"RPi.GPIO: Error during cleanup: {e}")

    def setmode(self, mode):
        """
        Set pin numbering mode (for compatibility)

        Note: This implementation always uses BCM mode internally.
        This method exists for API compatibility but doesn't change behavior.

        Args:
            mode: BCM or BOARD (only BCM is supported)
        """
        if mode != self.BCM:
            logger.warning(f"Only BCM mode is supported, ignoring mode={mode}")

    def setwarnings(self, enabled):
        """
        Enable/disable warnings (for compatibility with RPi.GPIO)

        Args:
            enabled: True to enable warnings, False to disable
        """
        if self.backend == 'RPi.GPIO':
            GPIO.setwarnings(enabled)
        # lgpio doesn't have warnings to control
