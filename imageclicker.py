import pyautogui
import cv2
import numpy as np
import time
import os

def locate_image_on_screen(image_path):
    try:
        # Take a screenshot
        screenshot = pyautogui.screenshot()
    except pyautogui.PyAutoGUIException as e:
        print(f"Error taking screenshot: {e}")
        return None

    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Load the target image
    if not os.path.exists(image_path):
        print(f"Image path {image_path} does not exist.")
        return None

    target_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if target_image is None:
        print(f"Failed to load image {image_path}.")
        return None

    # Convert the target image to grayscale
    target_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Match the template (target image) with the screenshot
    result = cv2.matchTemplate(screenshot_gray, target_gray, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Define a threshold for a match
    threshold = 0.8
    if max_val >= threshold:
        return max_loc
    return None

def click_on_image(image_path):
    location = locate_image_on_screen(image_path)
    if location:
        target_image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        # Calculate the center of the matched region
        center_x = location[0] + target_image.shape[1] // 2
        center_y = location[1] + target_image.shape[0] // 2
        # Move the mouse to the center of the matched region and click
        pyautogui.moveTo(center_x, center_y)
        pyautogui.click()
        print(f"Clicked on location: ({center_x}, {center_y})")
    else:
        print("Image not found on screen.")

def main(image_path):
    while True:
        click_on_image(image_path)
        time.sleep(3)

if __name__ == "__main__":
    # Path to the image you want to match
    image_path = "image.png"
    main(image_path)