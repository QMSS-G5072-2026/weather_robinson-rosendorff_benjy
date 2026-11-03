# read version from installed package
from importlib.metadata import version
__version__ = version("weather_br2844")

from .weather_br2844 import celsius_to_fahrenheit
from .weather_br2844 import summarize_temperatures
from .weather_br2844 import clean_readings