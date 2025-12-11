from __future__ import annotations
from typing import Protocol
from PIL.Image import Image

from adbutils import AdbDevice  # type: ignore


class IAdbDeviceClient(Protocol):
    """
    Interface for an ADB device client.
    Defines the expected methods and behavior for device interaction.
    """

    adb_device: AdbDevice | None

    def connect(self) -> bool:
        """
            Connect to the device. 
            Returns True if successful, 
            raises Raise AdbDeviceClientConnectionTimeoutError on timeout.
        
        """
        ...

    def disconnect(self) -> None:
        """Disconnect from the device."""
        ...

    def reconnect(self) -> bool:
        """Disconnect & connect to the device."""
        ...

    def check_connection(self) -> bool:
        """Check if the device is currently connected."""
        ...

    def maintain_connection(self) -> bool:
        """
            Maintain connection of the current device - reconnect() if disconnected. 
            Raise AdbDeviceClientConnectionTimeoutError() from connect() on timetout
        """
        ...

    def shell_exc(self, cmd: str) -> str:
        """Execute a shell command on the device and return its output as string."""
        ...

    def screenshot(self) -> Image:
        """Get Screenshot from the current device"""
        ...