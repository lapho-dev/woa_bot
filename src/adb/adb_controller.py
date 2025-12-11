from __future__ import annotations
from core.point import Point
import time
import numpy as np
from numpy.typing import NDArray
from PIL.Image import Image

from adb.interfaces.i_adb_device_client import IAdbDeviceClient

class AdbControllerError(Exception):
    pass

class AdbController:
    def __init__(self, adb_device_client: IAdbDeviceClient):
        self.adb_device_client = adb_device_client

    # --------------------------------
    # Screen
    # --------------------------------
    def get_raw_screenshot(self) -> Image:
        """Return screenshot as PIL image - requires preprocessing."""
        try:
            pil_image: Image = self.adb_device_client.screenshot()
            return pil_image
        except Exception as e:
            raise AdbControllerError from e
        

    # --------------------------------
    # Tap
    # --------------------------------
    def tap(self, pt: Point, debounce: float = 0.2):
        try:
            self.adb_device_client.shell_exc(f"input tap {pt.x} {pt.y}")
            time.sleep(debounce)   
        except Exception as e:
            raise AdbControllerError(f"Failed to tap at {pt}.") from e
        

    def tap_multiple(self, pt: Point, number_of_clicks: int = 1, debounce: float = 0.5):
        try:
            for _ in range(number_of_clicks):
                self.tap(pt, debounce=0)
            time.sleep(debounce)  
        except Exception as e:
            raise AdbControllerError(f"Filated to tap {number_of_clicks} times at {pt}.") from e
        
    

    # --------------------------------
    # Swipe
    # --------------------------------
    def swipe(self, start_pt: Point, end_pt: Point, duration: int = 500, debounce: float = 0.5):
        try:
            self.adb_device_client.shell_exc(f"input swipe {start_pt.x} {start_pt.y} {end_pt.x} {end_pt.y} {duration}")
            time.sleep(debounce)    
        except Exception as e:
            raise AdbControllerError(f"Failed to swipe from {start_pt} to {end_pt}.") from e