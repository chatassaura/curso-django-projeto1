import os
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager  # <--- New import

ROOT_DIR = Path(__file__).parent.parent
# We no longer need the hardcoded CHROMEDRIVER_PATH constants


def make_chrome_browser(*options):
    chrome_options = webdriver.ChromeOptions()

    if options is not None:
        for option in options:
            chrome_options.add_argument(option)

    if os.environ.get('SELENIUM_HEADLESS') == '1':
        chrome_options.add_argument('--headless')

    # This line downloads the version that matches your Chrome 143
    # automatically
    driver_path = ChromeDriverManager().install()
    chrome_service = Service(executable_path=driver_path)

    browser = webdriver.Chrome(service=chrome_service, options=chrome_options)
    return browser


if __name__ == '__main__':
    # Test it works
    browser = make_chrome_browser('--headless')
    browser.get('https://google.com.br')
    print(f"Title: {browser.title}")
    sleep(2)
    browser.quit()
