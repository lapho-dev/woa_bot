from __future__ import annotations
from typing import Protocol
from PIL.Image import Image
from core.point import Point
from adb.interfaces.i_adb_device_client import IAdbDeviceClient

class IAdbController(Protocol):
    """
    Interface for the AdbController.
    Defines the expected methods and behavior for device interactions
    through a higher-level abstraction using an IAdbDeviceClient.
    """

    adb_device_client: IAdbDeviceClient

    # -------------------------
    # Screen
    # -------------------------
    def get_raw_screenshot(self) -> Image:
        """Return screenshot as PIL image - requires preprocessing."""
        ...

    # -------------------------
    # Tap
    # -------------------------
    def tap(self, pt: Point, debounce: float = 0.2) -> None:
        """Tap on the device screen at the specified point."""
        ...

    def tap_multiple(self, pt: Point, number_of_clicks: int = 1, debounce: float = 0.5) -> None:
        """Tap multiple times on the specified point."""
        ...

    # -------------------------
    # Swipe
    # -------------------------
    def swipe(self, start_pt: Point, end_pt: Point, duration: int = 500, debounce: float = 0.5) -> None:
        """Swipe from start_pt to end_pt over the specified duration in milliseconds."""
        ...
