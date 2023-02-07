# Imports
from __future__ import annotations
from pprint import pformat
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from risegardenapi import RiseGardenAPI


class Garden:
    """
    Class that represets a Rise Garden.

    Attributes
    ----------
    id: The ID of the garden
    name: The name of the garden
    type: The type of the garden
    api: The API object used to communicate with the garden
    status: The status of the garden
    last_reading: The last reading from the garden
    kit: The kit type of the garden
    Mainboard: The mainboard information for the garden
    wifi: The wifi information for the garden
    tank: The tank information for the garden
    temperature: The temperature of the garden

    Methods
    -------
    """

    # Initialize the class
    def __init__(self, id: int, name: str, type: str, api: RiseGardenAPI):
        self.id = id
        self.name = name
        self.type = type
        self.api = api
        self.status = None
        self.last_reading = None
        self.kit = None
        self.mainboard = None
        self.wifi = None
        self.tank = None
        self.temperature = None
        self.lamp = None

    def _update_status(self, status: dict) -> None:
        """
        PRIVATE: Update the garden status.
        :param status: dict. The garden status.
        """
        self.status = status['status']
        self.last_reading = status['last_reading']
        self.kit = status['kit']
        self.mainboard = Garden.Mainboard(status['serial_number'], status['firmware'], status['control_board_id'])
        self.wifi = Garden.Wifi(status['ip'], status['wifi_signal_strength'], status['wifi_rssi'])
        self.tank = Garden.Tank(status['water_distance'], status['water_depth'], status['water_led_index'],
            status['current_water_volume_gallons'])
        self.lamp = Garden.Lamp(status['lamp_state'], status['lamp_level'], self)
        self.temperature = status['at']

    def __str__(self) -> str:
        """
        Return a string representation of the garden.
        :return: str. The name and type of the garden.
        """
        return pformat(self.__dict__)

    def temp_in_c(self) -> float:
        """
        Return the temperature in Celsius.
        :return: float. The temperature in Celsius.
        """
        return self.temperature

    def temp_in_f(self) -> float:
        """
        Return the temperature in Fahrenheit.
        :return: float. The temperature in Fahrenheit.
        """
        return self.temperature * 1.8 + 32

    def update(self) -> bool:
        """
        Update the garden information.
        :return: bool. True if the update was successful; false if the update failed.
        """
        status = self.api.get_garden_status(self.id)
        self._update_status(status)
        return True

    class Wifi:
        """
        Class that represents the wifi settings for a Rise Garden.

        Attributes
        ----------
        ip : str - The IP address of the garden
        strength : str - The strength of the wifi signal
        rssi : int - The RSSI of the wifi signal
        """

        def __init__(self, ip: str, strength: str, rssi: int):
            self.ip = ip
            self.strength = strength
            self.rssi = rssi

        def __str__(self) -> str:
            """
            Return a string representation of the wifi.
            """
            return pformat(self.__dict__)

    class Mainboard:
        """
        Class that represents the mainboard settings for a Rise Garden.

        Attributes
        ----------
        serial_number : str - The serial number of the mainboard
        firmware : str - The firmware version of the mainboard
        control_board_id : str - The control board ID of the mainboard
        """

        def __init__(self, serial_number: str, firmware: str, control_board_id: str):
            self.serial_number = serial_number
            self.firmware = firmware
            self.control_board_id = control_board_id

        def __str__(self) -> str:
            """
            Return a string representation of the mainboard.
            """
            return pformat(self.__dict__)

    class Tank:
        """
        Class that represents the water tank for a Rise Garden.

        Attributes
        ----------
        distance : int - The distance from the tank to the sensor
        depth : float - The depth of the water in the tank
        led_index : int - The LED index of the tank
        volume : float - The volume of water in the tank

        Methods
        -------
        volume_gallons() -> float - Return the water level of the tank in gallons
        volume_liters() -> float - Return the water level of the tank in liters
        """
        def __init__(self, distance: int, depth: float, led_index: int, volume: float):
            self.distance = distance
            self.depth = depth
            self.led_index = led_index
            self.volume = volume

        def __str__(self) -> str:
            """
            Return a string representation of the tank.
            """
            return pformat(self.__dict__)

        def volume_gallons(self) -> float:
            """
            Return the water level of the tank in gallons.
            :return: float. The water level of the tank in gallons.
            """
            return self.volume

        def volume_liters(self) -> float:
            """
            Return the water level of the tank in liters.
            :return: float. The water level of the tank in liters.
            """
            return self.volume * 3.78541

    class Lamp:
        """
        Class that represents the lamp settings for a Rise Garden.
        """
        def __init__(self, on: bool, level: int, garden: Garden):
            self.on = on
            self.level = level
            self.garden = garden

        def __str__(self) -> str:
            """
            Return a string representation of the lamp.
            """
            return pformat(self.__dict__)

        def set_level(self, level: int):
            """
            Set the lamp level.
            :param level: int. The level to set the lamp to.
            """
            self.garden.api.set_lamp_level(self.garden.id, level)
