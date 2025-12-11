from adb.interfaces.i_adb_controller import IAdbController
# from adb.interfaces.i_adb_device_client import IAdbDeviceClient

from bot.bot_service import BotService

from logger.logger import setup_logger, logging
logger = setup_logger(__name__, level=logging.ERROR)

class BotRunner():
    def __init__(self, adb_controller: IAdbController):
        # self.adb_device_client = adb_device_client
        self.adb_controller = adb_controller
        self.bot_service = BotService(adb_controller)

    def run_bot(self):
        pass