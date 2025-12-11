
import time
from typing import Optional
from adbutils import adb, AdbDevice # type: ignore
from PIL.Image import Image

from logger.logger import setup_logger, logging
logger = setup_logger(__name__, level=logging.ERROR)

class AdbDeviceClientError(Exception):
    pass

class AdbDeviceClientConnectionTimeoutError(Exception):
    pass

class AdbDeviceClient:
    def __init__(self, addr: str, timeout: Optional[float] = None, retry: int = 3):
        """
        Initialize the ADB device by serial.
        If serial is None, selects the first connected device.
        """
        self.addr = addr
        self.timeout = timeout
        self.retry = retry
        self.adb_device: Optional[AdbDevice] = None

    def connect(self) -> bool:
        for _ in range(self.retry):
            try:
                adb_connect_res: str = str(adb.connect(self.addr, self.timeout)) # type: ignore
                logger.info(adb_connect_res)
                temp_device = adb.device(self.addr) # type: ignore
                # adb.device may raise error, catched by try except block
                state = temp_device.get_state() # type: ignore
                if state != "device":
                    raise ConnectionError(f"Connected device with state '{state}'")
                self.adb_device = temp_device
                logger.info(f"Adb device connection is established at {self.addr}")
                return True
            except Exception:
                logger.warning("Adb connection timeout. Retry...")
                time.sleep(1)
                continue
        raise AdbDeviceClientConnectionTimeoutError(f"Adb connection cannot be established after {self.retry} tries.")
    
    def disconnect(self):
        adb.disconnect(self.addr) # type: ignore
        self.adb_device = None

    def reconnect(self) -> bool:
        self.disconnect()
        self.connect()
        return True

    def check_connection(self) -> bool:
        try:
            state = self.adb_device.get_state() # type: ignore
        except Exception:
            logger.warning('Checked connection - no connection.')
            return False
        if state == 'device':
            return True
        logger.warning('Checked connection - no connection.')
        return False
    
    def maintain_connection(self) -> bool:
        is_connected = self.check_connection()
        if not is_connected:
            self.reconnect()
        return True

    def shell_exc(self, cmd: str) -> str:
        """
        Run shell command, always return str.
        Handles stream=False case.
        """
        self.maintain_connection()
        return self.device.shell(cmd, stream=False) # type: ignore
    
    def screenshot(self) -> Image:
        self.maintain_connection()
        return self.device.screenshot() # type: ignore