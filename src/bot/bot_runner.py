from dataclasses import dataclass, field
from enum import Enum, auto
from adb.interfaces.i_adb_controller import IAdbController
# from adb.interfaces.i_adb_device_client import IAdbDeviceClient

from bot.bot_service import BotService

from logger.logger import setup_logger, logging
logger = setup_logger(__name__, level=logging.ERROR)

class GamePageState(Enum):
    UNKNOWN = auto()
    AIRPORT = auto()
    CLAIM_REWARDS = auto()
    SHOP = auto()
    PHONE_MAIN = auto()
    GAME_LOGIN = auto()
    AIRPORT_SELECTION = auto()
    LOADING = auto()


class SelectedPlaneStatus(Enum):
    NO_ACTIONS_REQUIRED = auto()
    UNKOWN = auto()

    # Arrival
    ARRIVAL_SELECT_STAND = auto()
    ARRIVAL_CLEAR_TO_LAND = auto()

    # Ground
    GROUND_HANDLING_CREW = auto()
    GROUND_CLAIM_REWARDS = auto()

    # Departure
    DEPARTURE_PUSHBACK = auto()
    DEPARTURE_LINE_UP_RUNWAY = auto()
    DEPARTURE_TAKEOFF = auto()
    DEPARTURE_DEICING = auto()
    
    
class PlaneCategoryFilter(Enum):
    NONE = auto()
    MY_AIRPLANES = auto()
    OTHERS_AIRPLANES = auto()
    UNIQUE_AIRPLANES = auto()

class PlaneStatusFilter(Enum):
    NONE = auto()
    ARRIVAL = auto()
    GROUND = auto()
    DEPARTURE = auto()

class FilterTags(Enum):
    REQUIRING_ACTIONS = auto()
    OVERTIME = auto()
    FAVOURITE = auto()

@dataclass
class FilterState:
    expanded: bool = False
    filter_plane_category: PlaneCategoryFilter = PlaneCategoryFilter.NONE
    plane_status_filter: PlaneStatusFilter = PlaneStatusFilter.NONE
    filter_tags: set[FilterTags] = field(default_factory=lambda: set[FilterTags]())

@dataclass
class AirportState:
    max_workers: int = 0
    used_workers: int = 0
    gold: int = 0
    silver: int = 0
    currency: int = 0
    
    filter_state: FilterState = field(default_factory=FilterState)
    is_plane_selected: bool = False
    selected_plane_status: SelectedPlaneStatus = SelectedPlaneStatus.UNKOWN

@dataclass
class GameState:
    current_page: GamePageState = GamePageState.PHONE_MAIN
    airport_state: AirportState = field(default_factory=AirportState)


class BotRunner():
    def __init__(self, adb_controller: IAdbController):
        self.adb_controller = adb_controller
        self.bot_service = BotService(adb_controller)
        self.game_state = GameState()

    def run_bot(self):
        # Check current game page
        self.game_state.current_page = self.check_current_game_page()

        match self.game_state.current_page:
            case GamePageState.AIRPORT:
                self.handle_game_page_airport()
            case GamePageState.CLAIM_REWARDS:
                self.handle_game_page_claim_rewards()
            case GamePageState.SHOP:
                self.handle_game_page_shop()
            case GamePageState.PHONE_MAIN:
                self.handle_game_page_phone_main()
            case GamePageState.LOADING:
                self.handle_game_page_loading()
            case GamePageState.GAME_LOGIN:
                self.handle_game_page_game_login()
            case GamePageState.AIRPORT_SELECTION:
                self.handle_game_page_airport_selection()
            case GamePageState.UNKNOWN:
                self.handle_game_page_unknown()

    def check_current_game_page(self) -> GamePageState:
        # Placeholder for game page checking
        # TODO
        return GamePageState.AIRPORT

    # -------------------------------
    #             HANDLERS
    # -------------------------------

    def handle_game_page_airport(self):
        # TODO
        pass

    def handle_game_page_claim_rewards(self):
        # TODO
        pass

    def handle_game_page_shop(self):
        # TODO
        pass

    def handle_game_page_phone_main(self):
        # TODO
        pass

    def handle_game_page_loading(self):
        # TODO
        pass

    def handle_game_page_game_login(self):
        # TODO
        pass

    def handle_game_page_airport_selection(self):
        # TODO
        pass

    def handle_game_page_unknown(self):
        # TODO
        pass
