from datetime import datetime
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def get_last_updated_date() -> str:
    DRIVER = setup_chromedriver()
    data_nsw_url = "https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q="
    DRIVER.get(data_nsw_url)
    last_updated_date = DRIVER.find_element(
        By.XPATH, "//span[@itemprop='dateModified']"
    ).text
    DRIVER.close()

    return datetime.strptime(last_updated_date, "%d/%m/%Y").strftime("%d %b %Y")


def setup_chromedriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


st.title("COVID in New South Wales")
st.write(f"_Last updated: **{get_last_updated_date()}**_")

# test lgas
lga_name = st.sidebar.selectbox(
    "Select Local Government Area (LGA)",
    ("Canterbury-Bankstown", "Blacktown", "Northern Beaches", "Bayside"),
)
