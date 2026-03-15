from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time

# Optional: Run Chrome in headless mode
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Uncomment to run in background
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the app
    driver.get("http://localhost:3000")
    wait = WebDriverWait(driver, 15)

    # Find the first file input
    file_input = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
    )
    print("Found file input.")

    # Set the path to your image (adjust as needed)
    image_path = os.path.abspath(os.path.join("test-images", "before_growth.png"))

    # Upload the image
    file_input.send_keys(image_path)
    print("Uploaded image:", image_path)

    # Click the analyze/predict button
    analyze_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(., 'Analyze') or contains(., 'Predict')]")
        )
    )
    analyze_button.click()
    print("Clicked analyze button.")

    # Wait for the result
    result_element = wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(., 'Growth') or contains(., 'Prediction') or contains(., 'Result')]")
        )
    )
    print("Result text:", result_element.text)
    assert result_element.text.strip() != "", "No result text found"

    time.sleep(3)

finally:
    driver.quit()
