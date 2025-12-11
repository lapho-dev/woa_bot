import numpy as np
from numpy.typing import NDArray
import cv2

class ImageUtilsError(Exception):
    pass


def save_image(cv_img:NDArray[np.uint8], file_path:str):
    """
    Save cv_image (np.array, colour BGR) to file_path.
    
    Args:
        cv_image (np.array): The source image (from cv2.imread or capture).
        fil_path (str): The path of the file to save the image to.
    """
    try:
        cv2.imwrite(file_path, cv_img)
        print(f"Image saved to {file_path}.")
    except Exception as e:
        raise ImageUtilsError(f"Cannot save image to {file_path}.") from e

def save_image_list(cv_img_list:list[NDArray[np.uint8]], file_path:str):
    for i, img in enumerate(cv_img_list):
        try:
            save_image(img, file_path.replace('.', f'_{i}.'))
        except Exception as e:
            raise ImageUtilsError(f"Cannot save list of images to {file_path}.") from e

