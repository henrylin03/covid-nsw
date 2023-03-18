from datetime import datetime
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def setup_chromedriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


def load_csv() -> pd.DataFrame:
    csv_url = "https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/5d63b527-e2b8-4c42-ad6f-677f14433520/download/confirmed_cases_table1_location_agg.csv"
    df = pd.read_csv(csv_url)
    df = df[["notification_date", "lga_name19", "confirmed_cases_count"]]
    df.columns = ["date", "lga", "cases_count"]
    df = df.groupby(["date", "lga"]).cases_count.sum().reset_index()
    df["lga"] = df.lga.str.rstrip(" (A)").str.rstrip(" (C)").str.rstrip(" (NSW)")
    return df


def get_last_updated_date() -> str:
    DRIVER = setup_chromedriver()
    data_nsw_url = "https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q="
    DRIVER.get(data_nsw_url)
    last_updated_date = DRIVER.find_element(
        By.XPATH, "//span[@itemprop='dateModified']"
    ).text
    DRIVER.close()

    return datetime.strptime(last_updated_date, "%d/%m/%Y").strftime("%d %b %Y")


def get_lgas() -> tuple:
    covid_df = load_csv()
    lgas_set = sorted(set(covid_df.lga.dropna()))
    return tuple(lgas_set)


st.title("COVID in NSW")
st.write(f"_Last updated: **{get_last_updated_date()}**_")

# test lgas
lga_name = st.sidebar.selectbox(
    "Select Local Government Area (LGA)",
    get_lgas(),
)
