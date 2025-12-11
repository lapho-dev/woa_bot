from typing import Optional
from adb.interfaces.i_adb_controller import IAdbController
import numpy as np
from numpy.typing import NDArray

from config.settings import Settings

import vision.preprocessing as vision_pre
import vision.extraction as vision_ext

from logger.logger import setup_logger, logging
logger = setup_logger(__name__, level=logging.ERROR)

class AirportControllerActionsError(Exception):
    pass

class ScreenshotEmptyError(Exception):
    pass


class BotService:
    def __init__(self, adb_controller: IAdbController):
        self.adb_controller = adb_controller
        self.latest_screenshot:Optional[NDArray[np.uint8]] = None

    def update_screenshot(self):
        raw_screenshot = self.adb_controller.get_raw_screenshot()
        screenshot = vision_pre.process_raw_screenshot(raw_screenshot)
        self.latest_screenshot = screenshot

    # Airport Actions
    def perform_ground_service_instruction(self, no_of_crew:int=13):
        """
            For current selected plane, 
            add handling crew to the max (param: no_of_crew),
            add ramp agent,
            click assign crew.
        """
        # Check if the current screen has a current plane for operations
        if not self.latest_screenshot:
            raise ScreenshotEmptyError()
        # TODO

        # Add worker to max
        self.adb_controller.tap_multiple(
            Settings.CURRENT_SELECTED_PLANE_HANDLING_CREW_PLUS_WORKER_COORDINATES,
            number_of_clicks=no_of_crew
        )

        
        # Add Ramp Agent
        try:
            if not vision_ext.classify_is_ramp_agent_toggle_switch_on(self.latest_screenshot):
                self.adb_controller.tap(
                    Settings.CURRENT_SELECTED_PLANE_HANDLING_CREW_EXTRA_RAMP_AGENT_COORDINATES,
                )
        except Exception as e:
            raise AirportControllerActionsError("Error occured when performing ground service instructions.") from e

        # Click Assign Crew
        self.adb_controller.tap(
            Settings.CURRENT_SELECTED_PLANE_CLICK_COORDINATES
        )

    def perform_deicing(self):
        # Check if the current screen has a current plane for operations
        if not self.latest_screenshot:
            raise ScreenshotEmptyError()
        # TODO

        # Click De-icing Button
        try:
            self.adb_controller.tap(
            Settings.CURRENT_SELECTED_PLANE_CLICK_COORDINATES
            )
        except Exception as e:
            raise AirportControllerActionsError("Error occured when perfomring deicing.") from e
    
    def check_filter_column(self):
        pass

    def check_arrival(self):
        """Input list of planes (image / info) return a list of plane that requires arrival clearance"""
        pass

    def check_departure(self):
        """Input list of planes (image / info) return a list of plane that requires departure clearance"""
        pass

    def check_on_airport_claim_rewards(self):
        pass

    def check_on_airport_ground_service(self):
        """Input list of planes (image / info) return a list of plane that requires ground service instruction"""
        # CHECK 
        # TODO
        pass

    def check_deicing(self):
        """Input list of planes (image / info) return a list of plane that requires deicing instruction"""
        pass

    def perform_arrival_clearance(self):
        pass

    def perform_departure_clearance(self):
        pass


    # Gamplay Actions
    def renew_tower_automation(self):
        """Buy tower automation periodically"""
        pass

    def shop(self):
        pass