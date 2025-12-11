from typing import Optional
import numpy as np
from numpy.typing import NDArray
import cv2
from PIL.Image import Image

from core.interfaces import IPoint
from core.interfaces import IRegion

from . import image_utils

class ImageProcessingError(Exception):
    pass

# Image preprocessing

def convert_pil_image_2_np_array(pil_image: Image) -> NDArray[np.uint8]:
    return np.array(pil_image).astype(np.uint8)

def convert_RGB_2_BGR(cv_img_rgb: NDArray[np.uint8]) -> NDArray[np.uint8]:
    return cv2.cvtColor(cv_img_rgb, cv2.COLOR_RGB2BGR).astype(np.uint8)

def process_raw_screenshot(pil_image: Image) -> NDArray[np.uint8]:
    return convert_RGB_2_BGR(convert_pil_image_2_np_array(pil_image))




# Image Basic Actions

def crop_image(
    cv_img: NDArray[np.uint8],
    region: IRegion
) -> NDArray[np.uint8]:
    """
    Crops an image based on a region - two points (pt1 and pt2).
    
    Args:
        cv_img (np.array): The source image.
        region (Region): 2 corners of a rectangle region.
        
    Returns:
        np.array: The cropped image.
    """
    try:
        x1, y1 = region.corner1.to_tuple_x_y()
        x2, y2 = region.corner2.to_tuple_x_y()

        # 1. Determine the correct boundary coordinates
        # Find the smallest (start) and largest (end) X coordinate
        x_min = min(x1, x2)
        x_max = max(x1, x2)
        
        # Find the smallest (start) and largest (end) Y coordinate
        y_min = min(y1, y2)
        y_max = max(y1, y2)

        # 2. Perform the robust slicing
        # OpenCV slicing is always [row_start:row_end, col_start:col_end]
        # which corresponds to [y_min:y_max, x_min:x_max]
        cropped_img = cv_img[y_min:y_max, x_min:x_max]
        
        if cropped_img.size == 0:
            raise ImageProcessingError(f"⚠️ Cropped image is empty. Check input region: {region}.")
            
        return cropped_img
    except Exception as e:
        raise ImageProcessingError(f"Error when cropping image for region: {region}.") from e
  
def crop_image_and_save(
    cv_img: NDArray[np.uint8],
    region: IRegion, 
    file_path:str
)-> NDArray[np.uint8]:
    """
    Crops an image based on a region - two points (pt1 and pt2) and save to file as png.
    
    Args:
        cv_img (np.array): The source image.
        region (Region): 2 corners of a rectangle region.
        fil_path (str): The path of the file to save the image to.
    """
    try:
        cropped_img = crop_image(cv_img, region)
        image_utils.save_image(cropped_img, file_path)
        return cropped_img
    except Exception as e:
        raise ImageProcessingError("Failed to crop and save image.") from e

def draw_circles_on_image(cv_img: NDArray[np.uint8], circles: Optional[NDArray[np.uint8]], show_coor:bool=False) -> NDArray[np.uint8]:
    try:
        cv_img_copy = cv_img.copy()
        if circles is None: 
            raise ValueError("Trying to draw circles on image but cirles array is None.")
        
        for (x, y, r) in circles:
            # draw outer circle
            cv2.circle(cv_img_copy, (x, y), r, (0, 255, 0), 2)
            # draw center
            cv2.circle(cv_img_copy, (x, y), 2, (0, 0, 255), 3)
            
            # optional: show coordinates on image
            if show_coor:
                cv2.putText(cv_img_copy, f"{x},{y}", (x+10, y-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        return cv_img_copy
    except Exception as e:
        raise ImageProcessingError("Failed to draw circles on image.") from e

def draw_spot_on_image(cv_img: NDArray[np.uint8], pt:IPoint) -> NDArray[np.uint8]:
    try:
        cv_img_copy = cv_img.copy()
        cv2.circle(cv_img_copy, pt.to_int_tuple_x_y(), 2, (0, 0, 255), 3)
        return cv_img_copy
    except Exception as e:
        raise ImageProcessingError(f"Failed to draw spot on image at {pt}.") from e

def get_pixel_at_pt(cv_img: NDArray[np.uint8], pt:IPoint) -> NDArray[np.uint8]:
    """Return the (B, G, R) pixel at a given Point in the image."""
    try:
        return cv_img[*pt.to_int_tuple_y_x()]
    except Exception as e:
        raise ImageProcessingError(f"Failed to get the pixel on an image at {pt}.") from e
    

