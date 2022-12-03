import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": os.path.abspath("./inputs")}
    options.add_experimental_option("prefs", prefs)

    # removes printing of "usb_device_handle" error in terminal
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


DRIVER = setup_driver()


def download():
    print("Downloading...", end=" ", flush=True)
    csv_download_button = DRIVER.find_element(
        By.XPATH,
        '//*[@id="content"]/div/div/div[2]/div/div[2]/div/div[1]/div/div[1]/div[2]/span[2]/span[1]/a',
    )
    csv_download_button.click()

    # only complete once the .csv exists in the folder
    csv_path = os.path.abspath("./inputs/confirmed_cases_table1_location_agg.csv")
    while not os.path.exists(csv_path):
        time.sleep(0.5)
    print("✅ Done!")
    DRIVER.close()
    return


def remove_old_file():
    csv_path = os.path.abspath("./inputs/confirmed_cases_table1_location_agg.csv")
    if os.path.exists(csv_path):
        print("\nRemoving previous .csv file...", end=" ", flush=True)
        os.remove(csv_path)
        print("✅ Done!")
    return


def main():
    DRIVER.get(
        "https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q="
    )
    remove_old_file()
    download()


if __name__ == "__main__":
    main()
