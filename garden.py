# Imports
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from gardenapi import Gardenapi

class Garden:
    """
    Class that represets a Rise Garden.
    
    Attributes
    ----------
    
    Methods
    -------
    """

    # Initialize the class
    def __init__(self, id: int, name: str, type: str, api: Gardenapi):
        self.id = id
        self.name = name
        self.type = type
        self.api = api
        self.status = None
        self.last_reading = None
        self.kit = None
        self.Mainboard = None
        self.wifi = None
        self.tank = None
    
    def _update_status(self, status: dict) -> None:
        """
        PRIVATE: Update the garden status.
        :param status: dict. The garden status.
        """
        self.status = status['status']
        self.last_reading = status['last_reading']
        self.kit = status['kit']
        self.Mainboard = Garden.Mainboard(status['serial_number'], status['firmware'], status['control_board_id'])
        self.wifi = Garden.Wifi(status['ip'], status['wifi_signal_strength'], status['wifi_rssi'])
        self.tank = Garden.Tank(status['water_distance'], status['water_depth'], status['water_led_index'],
            status['current_water_volume_gallons'])

    def __str__(self) -> str:
        """
        Return a string representation of the garden.
        :return: str. The name and type of the garden.
        """
        return f'{self.name} ({self.type}) - {self.status}'

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
        """

        def __init__(self, ip: str, strength: str, rssi: int):
            self.ip = ip
            self.strength = strength
            self.rssi = rssi
    
    class Mainboard:
        """
        Class that represents the mainboard settings for a Rise Garden.
        """

        def __init__(self, serial_number: str, firmware: str, control_board_id: str):
            self.serial_number = serial_number
            self.firmware = firmware
            self.control_board_id = control_board_id

    class Tank:
        """
        Class that represents the water tank for a Rise Garden.
        """
        def __init__(self, distance: int, depth: float, led_index: int, volume: float):
            self.distance = distance
            self.depth = depth
            self.led_index = led_index
            self.volume = volume
        
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
