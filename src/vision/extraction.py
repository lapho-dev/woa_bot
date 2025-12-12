from typing import Sequence, Tuple
import numpy as np
from numpy.typing import NDArray

from core.interfaces.i_point import IPoint
from core.point import Point
from core.region import Region

from config.settings import Settings

from . import preprocessing, recognition

class ExtractionError(Exception):
    pass



def classify_is_ramp_agent_toggle_switch_on(cv_img: NDArray[np.uint8]) -> bool:
    """
    Classify a toggle switch image as 'on' (green) or 'off' (grey).

    Parameters:
        cv_img (np.ndarray): Input image in BGR format. Cropped for the toggle switch.

    Returns:
        bool: True if green (on), False if grey (off).

    Raises:
        ValueError: If the image does not match expected toggle switch colors.
    """
    try:
        toggle_switch_img = preprocessing.crop_image(cv_img, Settings.CURRENT_SELECTED_PLANE_HANDLING_CREW_EXTRA_RAMP_AGENT_REGION)
        return recognition.classify_is_ramp_agent_toggle_switch_on_using_cropped_image(toggle_switch_img)
    except Exception as e:
        raise ExtractionError("Error classifying ramp agent toggle switch.") from e

def extract_filter_column_img_and_icon_ctr_coor(cv_img:NDArray[np.uint8]) -> Tuple[list[NDArray[np.uint8]], Sequence[IPoint]]:
    try:
        # Extract Filter Column Cropped Image (very right hand column)
        filter_column_image = preprocessing.crop_image(cv_img, Settings.PLANE_FILTER_REGION)

        # Recognise circles (filter tag icon) in the filter column
        circles = recognition.recognise_filter_icon_circles(filter_column_image)
        if len(circles) == 1:
            # Only one circle found, check its position.
            filter_icon_crop_region = Region(Point(0, 0), Point(110, 90))
            # filter_icon_crop_region = (0, 0), (110, 90)
            filter_icon_circle_centre = Point(circles[0, 0], circles[0, 1])
            if not filter_icon_crop_region.contains(filter_icon_circle_centre):
                raise ValueError("Filter Icon not in recognized position.")

            # Filter Icon Recognized
            filter_icon_crop_img  = preprocessing.crop_image(filter_column_image, filter_icon_crop_region)
            filter_column_icon_crop_img_list = [filter_icon_crop_img]
            # save_image(filter_icon_crop_img, f"{TEMP_DIR}/filter_icon_crop.png")
        elif len(circles) == 10:
            # Ten Filter Icon Recongnized, Crop individual
            filter_column_icon_crop_img_list: list[NDArray[np.uint8]] = []
            for circle in circles:
                icon_crop_region = Region(Point(0, max(0, circle[1]-45)), Point(110, min(1080, circle[1]+35)))
                icon_crop_img = preprocessing.crop_image(filter_column_image, icon_crop_region)
                filter_column_icon_crop_img_list.append(icon_crop_img)
                # save_image(icon_crop_img, f"{TEMP_DIR}/icon_crop_{circle[1]}.png")
        else:
            raise ValueError(f"Number of filter column's icon isn't considered: {len(circles)}.")
        
        # Get the center coordinates (hitbox) for each icon.
        icon_ctr_coordinates_list: list[Point] = [Point(Settings.PLANE_FILTER_REGION.corner1.x+circle[0], circle[1]) for circle in circles]

        return filter_column_icon_crop_img_list, icon_ctr_coordinates_list
    except Exception as e:
        raise ExtractionError("Error occured when extracting filter icons' images and their center coordinates in filter column,") from e
    

