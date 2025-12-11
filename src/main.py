import time


from config.settings import Settings

from adb.interfaces.i_adb_device_client import IAdbDeviceClient
from adb.interfaces.i_adb_controller import IAdbController
from adb.adb_device_client import AdbDeviceClient, AdbDeviceClientConnectionTimeoutError
from adb.adb_controller import AdbController

from bot.bot_runner import BotRunner

from logger.console import console
from logger.logger import setup_logger, logging
logger = setup_logger(__name__, level=logging.ERROR)




def main_loop(adb_device_client: IAdbDeviceClient, adb_controller: IAdbController):
    was_connected:bool = True
    while True:
        try:
            adb_device_client.maintain_connection()
            if was_connected:
                logger.info("Connection stable.")
                console.print("[pink3]Starting bot services.[/pink3]")
            else:
                logger.info("Connection stable - reconnected.")
                console.print("[green]Reconnected![/green]")
                was_connected = True
            
            # Bot Loging
            bot_runner = BotRunner(adb_controller)
            bot_runner.run_bot()

            console.print(f"[pink3]Finished bot services. Next cycle starts in {Settings.CYCLE_SECONDS} seconds[/pink3]")
            time.sleep(Settings.CYCLE_SECONDS)
            continue

        except AdbDeviceClientConnectionTimeoutError as e:
            logger.warning(e)
        except Exception:
            logger.error("Unexpected error in adb connection:", exc_info=True)

        # Connection dropped
        if was_connected:
            logger.warning("Connection lost.")
            console.print("[red]Connection lost![/red]")
            was_connected = False

        logger.warning(f"Retrying in {Settings.CYCLE_SECONDS} seconds...")
        console.print(f"[red]Retrying in {Settings.CYCLE_SECONDS} seconds...[/red]")
        time.sleep(Settings.CYCLE_SECONDS)
    

# main
if __name__ == "__main__":
    try:
        adb_device_client = AdbDeviceClient(addr=Settings.ADDR)
        adb_device_client.connect()
        adb_controller = AdbController(adb_device_client)
        console.print("[green]Connected![/green]")
    except AdbDeviceClientConnectionTimeoutError as e:
        logger.error(f"Exiting.. {e}")
        quit()
    except Exception:
        logger.error("Exting.. Failed initial connection to adb device with unexpected error:", exc_info=True)
        quit()

    try:
        main_loop(adb_device_client, adb_controller) # type: ignore
    except Exception:
        logger.error("Exiting.. Unexpected error in main loop:", exc_info=True)
        quit()