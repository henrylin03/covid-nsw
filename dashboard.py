import sys
import datetime
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as mtick
import seaborn as sns


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


def setup_chromedriver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--start-maximized")
    return webdriver.Chrome(
        options=options, service=Service(ChromeDriverManager().install())
    )


@st.cache_data
def get_lgas() -> tuple:
    covid_df = load_and_clean_csv()
    all_lgas = set(covid_df.lga.dropna())
    non_lgas = {"Correctional settings", "Hotel Quarantine"}

    lgas_filtered_sorted = sorted(all_lgas - non_lgas)
    lgas_filtered_sorted.insert(0, "All")
    return tuple(lgas_filtered_sorted)


def plot_daily_cases_area_chart(input_df: pd.DataFrame):
    daily_cases = input_df.groupby("date").sum(numeric_only=True).reset_index()
    daily_cases.date = pd.to_datetime(daily_cases.date, format="%Y-%m-%d")

    sns.set_style("dark", {"axes.facecolor": "0.95"})
    sns.set_palette("dark")

    fig, ax = plt.subplots(figsize=(7, 1.3), dpi=1000)
    sns.lineplot(x="date", y="cases_count", data=daily_cases, ax=ax, linewidth=0.8)
    plt.fill_between(x=daily_cases.date, y1=daily_cases.cases_count, alpha=0.2)

    ax.xaxis.set_minor_locator(md.MonthLocator(bymonth=range(13)))
    ax.xaxis.set_minor_formatter(md.DateFormatter("%b"))
    ax.xaxis.set_major_locator(md.YearLocator(month=7, day=2))
    ax.xaxis.set_major_formatter(md.DateFormatter("\n\n%Y"))
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)
    ax.tick_params(axis="x", which="minor", labelsize=5)

    y_axis_fmt = "{x:,.0f}"
    y_ticks = mtick.StrMethodFormatter(y_axis_fmt)
    ax.yaxis.set_major_formatter(y_ticks)
    ax.tick_params(axis="both", which="major", labelsize=6)

    ax.set_ylabel("Reported Cases", fontsize=6, labelpad=6)
    ax.set_xlabel(None)

    return fig


def plot_total_cases_by_lga(input_df: pd.DataFrame):
    df = total_cases_by_lga(input_df)
    fig, ax = plt.subplots(figsize=(7, 1.3), dpi=1000)
    sns.barplot(
        x="cases_count",
        y="lga",
        data=df.head(10),
        orient="h",
        saturation=10,
        color="#ef5675",
        edgecolor="black",
        linewidth=0.7,
        ax=ax,
    )
    ax.set_xlabel("Total Cases ('000s)", fontsize=5)
    ax.set_ylabel("LGA", fontsize=5)
    ax.tick_params(axis="both", labelsize=5)
    ax.xaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, _: "{:,.0f}".format(x / 1000))
    )
    return fig


def total_cases_by_lga(input_df: pd.DataFrame) -> pd.DataFrame:
    totalled_df = (
        input_df.groupby("lga")
        .sum(numeric_only=True)
        .reset_index()
        .sort_values("cases_count", ascending=False)
    )
    return totalled_df


def filter_df_by_lga(input_df: pd.DataFrame) -> pd.DataFrame:
    res_df = input_df.copy()
    lga_name = st.sidebar.selectbox(
        "Local Government Area (LGA)",
        get_lgas(),
    )
    if lga_name == "All":
        return res_df
    return res_df[res_df.lga == lga_name]


def find_last_cont_zero_day(input_df: pd.DataFrame):
    impute_df = generate_lga_date_combination_df(input_df)
    input_df.date = pd.to_datetime(input_df.date)
    zero_days_imputed_df = (
        impute_df.merge(input_df, how="left").fillna(0).sort_values("date")
    )

    last_zero_day = (
        zero_days_imputed_df.date[zero_days_imputed_df.cases_count == 0]
    ).max()
    last_zero_day_formatted = datetime.datetime.strftime(last_zero_day, "%#d %b %Y")
    return last_zero_day_formatted


def generate_lga_date_combination_df(input_df: pd.DataFrame) -> pd.DataFrame:
    # generate every day's date
    dataset_start_date = get_start_date()
    dataset_last_updated_date = get_last_updated_date()
    day_before_date = dataset_last_updated_date - datetime.timedelta(days=1)

    d_range = pd.date_range(dataset_start_date, day_before_date, freq="d")
    dates_df = pd.DataFrame(d_range, columns=["date"])

    # merge every LGA
    lgas_list = list(get_lgas())
    lgas_list.remove("All")
    lgas_df = pd.DataFrame(lgas_list, columns=["lga"])
    lgas_df["key"] = 0
    dates_df["key"] = 0

    return dates_df.merge(lgas_df, on="key", how="outer").drop("key", axis=1)


def main():
    st.set_page_config(
        page_title="COVID in NSW", page_icon=":chart_with_upwards_trend:", layout="wide"
    )

    covid_df = load_and_clean_csv()
    dataset_start_date = get_start_date()
    dataset_last_updated_date = get_last_updated_date()
    dataset_last_updated_date_formatted = dataset_last_updated_date.strftime("%d %b %Y")

    st.title(":chart_with_upwards_trend: COVID in NSW")
    st.write(f"_Last updated: **{dataset_last_updated_date_formatted}**_")

    st.sidebar.header("Filters")
    covid_df = filter_df_by_lga(covid_df)

    # metrics
    total_cases_m, last_zero_day_m = st.columns(2)
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

    total_cases_m.metric(
        label="Total Cases",
        value=f"{int(covid_df.cases_count.sum()):,}",
        delta=f"{latest_daily_cases - two_days_before_cases:,} daily",
        delta_color="inverse",
        help='Due to time-lag in reporting, cases are reported up to the "Last updated" date',
    )

    last_zero_day = find_last_cont_zero_day(
        covid_df,
        start_date=dataset_start_date,
        end_date=day_before_date,
    )
    last_zero_day_formatted = datetime.datetime.strptime(
        last_zero_day, "%d %b %Y"
    ).date()
    days_since_last_zero_day = abs((day_before_date - last_zero_day_formatted).days)
    last_zero_day_m.metric(
        label='Last "Zero" Day',
        value=last_zero_day,
        delta=f"{days_since_last_zero_day} days",
        delta_color="off",
    )

    # visualisations
    st.markdown("**Daily Cases**")
    daily_cases_area_chart = plot_daily_cases_area_chart(covid_df)
    st.pyplot(daily_cases_area_chart)

    st.markdown("**Top 10 LGAs by Total Cases**")
    cases_by_lga_barplot = plot_total_cases_by_lga(covid_df)
    st.pyplot(cases_by_lga_barplot)

    # dataframe
    st.dataframe(covid_df, use_container_width=True)


main()
