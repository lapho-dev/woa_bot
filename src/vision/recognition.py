from typing import Any, cast
import numpy as np
from numpy.typing import NDArray
import cv2



class RecognitionError(Exception):
    pass

def classify_is_ramp_agent_toggle_switch_on_using_cropped_image(toggle_switch_img: NDArray[np.uint8]) -> bool:
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
        # Resize for consistency
        resized = cv2.resize(toggle_switch_img, (100, 50))

        # Convert to HSV for better color segmentation
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

        # Define HSV color ranges
        green_lower = np.array([40, 50, 50])
        green_upper = np.array([80, 255, 255])

        grey_lower = np.array([0, 0, 50])
        grey_upper = np.array([180, 50, 200])

        # Create masks
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        grey_mask = cv2.inRange(hsv, grey_lower, grey_upper)

        green_pixels = cv2.countNonZero(green_mask)
        grey_pixels = cv2.countNonZero(grey_mask)

        if green_pixels > grey_pixels and green_pixels > 100:
            return True
        elif grey_pixels > green_pixels and grey_pixels > 100:
            return False
        else:
            raise ValueError("Unrecognized ramp agent toggle switch img: unrecognized color or insufficient color dominance. Saved image to temp/error.png")
    except Exception as e:
        raise RecognitionError("Error classifying ramp agent toggle switch.") from e

def recognise_filter_icon_circles(filter_column_img: NDArray[np.uint8]) -> NDArray[np.uint8]:
    try:
        grey_img = cv2.cvtColor(filter_column_img, cv2.COLOR_BGR2GRAY)

        circles_res: np.ndarray[Any, np.dtype[np.integer | np.floating]] | None = cv2.HoughCircles(
            grey_img,
            cv2.HOUGH_GRADIENT,
            dp=1.2,
            minDist=60,
            param1=80,
            param2=28,
            minRadius=18,
            maxRadius=45
        )
        circles_res = cast(np.ndarray[Any, np.dtype[np.integer | np.floating]] | None, circles_res)
        if circles_res is None:
            raise ValueError("The given image has no cirles.")
        
        circles_res = cast(NDArray[np.floating], circles_res)
        circles_2d: NDArray[np.floating] = circles_res[0]
        circles_int: NDArray[np.uint8] = np.rint(circles_2d).astype(np.uint8)
        sorted_circles: NDArray[np.uint8] = circles_int[circles_int[:, 1].argsort()]
        return sorted_circles
    except Exception as e:
        raise RecognitionError("Error in recognising circles in filter column.") from e
    
def classify_is_filter_icon_clicked(filter_icon_img: NDArray[np.uint8]) -> bool:
    """
    Determines whether a single filter icon is clicked or not.
    
    Args:
        cv_img (np.ndarray): Input image in BGR forma: Cropped for each icon.
    
    Returns:
        bool: True if clicked (darker grey background), False if not clicked (light grey in background)
    
    Raises:
        ValueError: If the image doesn't match either expected state clearly.
    """
    return False