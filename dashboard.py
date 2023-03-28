import sys
import datetime
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def setup_chromedriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


@st.cache_data
def load_and_clean_csv() -> pd.DataFrame:
    csv_url = "https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/5d63b527-e2b8-4c42-ad6f-677f14433520/download/confirmed_cases_table1_location_agg.csv"
    df = pd.read_csv(csv_url)
    df = df[["notification_date", "lga_name19", "confirmed_cases_count"]]
    df.columns = ["date", "lga", "cases_count"]
    df = df.groupby(["date", "lga"]).cases_count.sum().reset_index()
    df["lga"] = (
        df.lga.str.replace(" (A)", "", regex=False)
        .str.replace(" (C)", "", regex=False)
        .str.replace(" (NSW)", "", regex=False)
    )
    # df["date"] = pd.to_datetime(df.date, format="%Y-%m-%d")
    return df


@st.cache_data
def get_start_date() -> datetime.date:
    covid_df = load_and_clean_csv()
    first_case_date = min(covid_df.date)
    first_case_date_datetime = datetime.datetime.strptime(first_case_date, "%Y-%m-%d")
    return first_case_date_datetime.date()


@st.cache_data
def get_last_updated_date() -> datetime.date:
    DRIVER = setup_chromedriver()
    data_nsw_url = "https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q="
    DRIVER.get(data_nsw_url)
    last_updated_date_str = DRIVER.find_element(
        By.XPATH, "//span[@itemprop='dateModified']"
    ).text
    DRIVER.close()

    return datetime.datetime.strptime(last_updated_date_str, "%d/%m/%Y").date()


@st.cache_data
def get_lgas() -> tuple:
    covid_df = load_and_clean_csv()
    all_lgas = set(covid_df.lga.dropna())
    non_lgas = {"Correctional settings", "Hotel Quarantine"}
    lgas_filtered = all_lgas - non_lgas
    return tuple(sorted(lgas_filtered))


def main():
    st.set_page_config(
        page_title="COVID in NSW", page_icon=":adhesive_bandage:", layout="wide"
    )

    covid_df = load_and_clean_csv()
    dataset_start_date = get_start_date()
    dataset_last_updated_date = get_last_updated_date()
    dataset_last_updated_date_formatted = dataset_last_updated_date.strftime("%d %b %Y")

    st.title(":adhesive_bandage: COVID in NSW")
    st.write(f"_Last updated: **{dataset_last_updated_date_formatted}**_")

    st.sidebar.header("Filters")
    lga_name = st.sidebar.selectbox(
        "Local Government Area (LGA)",
        get_lgas(),
    )

    ## CAN I CHANGE FORMAT OF THE DATES?
    date_range = st.sidebar.date_input(
        "Date Range",
        min_value=dataset_start_date,
        max_value=dataset_last_updated_date,
        value=[dataset_start_date, dataset_last_updated_date],
    )

    ## ADD COLUMNS AND VISUALISATIONS (MAYBE WIREFRAME FIRST?)
    total_cases_metric, total_daily_cases_metric = st.columns(2)
    total_cases = int(covid_df.cases_count.sum())
    total_cases_metric.metric(label="Total Cases", value=f"{total_cases:,}")

    # one day lag in reporting
    day_before_date = dataset_last_updated_date - datetime.timedelta(days=1)
    latest_day_filtered_df = covid_df[
        covid_df["date"] == day_before_date.strftime("%Y-%m-%d")
    ]
    latest_daily_cases = int(latest_day_filtered_df.cases_count.sum())
    two_days_before_date = dataset_last_updated_date - datetime.timedelta(days=2)
    two_days_before_cases = int(
        covid_df[
            covid_df.date == two_days_before_date.strftime("%Y-%m-%d")
        ].cases_count.sum()
    )

    total_daily_cases_metric.metric(
        label="Daily Cases",
        value=f"{latest_daily_cases:,}",
        delta=f"{latest_daily_cases - two_days_before_cases:,}",
        delta_color="inverse",
        help='Due to time-lag in reporting, cases are reported up to and including the day before the "Last updated" date',
    )

    st.dataframe(covid_df, use_container_width=True)


main()
