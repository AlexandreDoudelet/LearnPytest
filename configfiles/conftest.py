import os
import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="class")
def browser(request):
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))# You can specify the path to your chromedriver if needed
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version="114.0.5735.90").install()))
    driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to appear
    # Simulate human-like delays
    #time.sleep(1.3)  # wait for 2 seconds
    driver.maximize_window()
    request.cls.browser = driver
    yield driver
    driver.quit()

#Create a directory to store the screenshots
SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR,exist_ok=True) 

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item,call):
    #Execute all the others hooks to obtain the report object
    outcome=yield
    rep = outcome.get_result()

    #We only care about failure and errors
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("browser")
        if driver:
            #Construct the screenshot file path
            screenshot_file = os.path.join(SCREENSHOT_DIR,f"{item.name}.png")

            #Take screenshot

            driver.save_screenshot(screenshot_file)

            print(f"Screenshot saved to {screenshot_file}") 

            # # Attach the screenshot to the report
            # if "extra" not in rep.__dict__:
            #     rep.__dict__["extra"] = []
            # rep.__dict__["extra"].append(pytest_html.extras.png(screenshot_file))

