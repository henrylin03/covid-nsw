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
    CSV_URL = "https://data.nsw.gov.au/data/dataset/aefcde60-3b0c-4bc0-9af1-6fe652944ec2/resource/5d63b527-e2b8-4c42-ad6f-677f14433520/download/confirmed_cases_table1_location_agg.csv"
    df = pd.read_csv(CSV_URL)
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
    DATA_NSW_URL = "https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q="
    DRIVER.get(DATA_NSW_URL)
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

    sns.set_style("dark", {"axes.facecolor": "0.994"})
    sns.set_palette("dark")

    fig, ax = plt.subplots(figsize=(7, 1.3), dpi=1000)
    sns.lineplot(
        x="date",
        y="cases_count",
        data=daily_cases,
        ax=ax,
        linewidth=0.65,
        color="#1f77b4",
    )
    plt.fill_between(x=daily_cases.date, y1=daily_cases.cases_count, color="#c9e5ff")

    ax.xaxis.set_minor_locator(md.MonthLocator(bymonth=range(13)))
    ax.xaxis.set_minor_formatter(md.DateFormatter("%b"))
    ax.xaxis.set_major_locator(md.YearLocator(month=7, day=2))
    ax.xaxis.set_major_formatter(md.DateFormatter("\n\n%Y"))
    plt.setp(ax.xaxis.get_minorticklabels(), rotation=90)
    ax.tick_params(axis="x", which="minor", labelsize=4.5)

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
        saturation=1,
        color="#c9e5ff",
        edgecolor="#1f77b4",
        linewidth=0.8,
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


def impute_zero_days_by_lga(input_df: pd.DataFrame) -> pd.DataFrame:
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

    df_for_imputing = dates_df.merge(lgas_df, on="key", how="outer").drop("key", axis=1)

    input_df.date = pd.to_datetime(input_df.date)
    zero_days_imputed_by_lgas = (
        df_for_imputing.merge(input_df, how="left").fillna(0).sort_values("date")
    )
    return zero_days_imputed_by_lgas


def find_zero_day_stats(input_df: pd.DataFrame) -> dict:
    res_dict = {}

    zero_days_imputed_by_lgas = impute_zero_days_by_lga(input_df)
    zero_days_imputed_all_lgas = (
        zero_days_imputed_by_lgas.groupby("date").cases_count.sum().reset_index()
    )

    res_dict["latest_zero_day"] = zero_days_imputed_all_lgas["date"][
        zero_days_imputed_all_lgas.cases_count == 0
    ].max()

    # # calculate streaks
    # zero_days_imputed_all_lgas["zero_days_streak"] = zero_days_imputed_all_lgas.groupby(
    #     (zero_days_imputed_all_lgas.cases_count != 0).cumsum()
    # ).cumcount()

    # res_dict["streak"] = (
    #     zero_days_imputed_all_lgas.loc[
    #         zero_days_imputed_all_lgas.date == pd.to_datetime(day_before_date),
    #         "zero_days_streak",
    #     ]
    #     .iloc[0]
    #     .astype(int)
    # )
    # if not res_dict["streak"]:
    #     res_dict["latest_zero_day"] = zero_days_imputed_all_lgas[
    #         zero_days_imputed_all_lgas.cases_count == 0
    #     ].date.max()
    # else:
    #     date_zero_day_streak_started = day_before_date - datetime.timedelta(
    #         days=(int(res_dict["streak"]) - 1)
    #     )
    #     res_dict["start_of_latest_zero_day_streak"] = date_zero_day_streak_started

    latest_date = zero_days_imputed_all_lgas.date.max()
    res_dict["days_since_last_zero"] = (
        res_dict["latest_zero_day"].date() - latest_date.date()
    ).days

    return res_dict


def main():
    st.set_page_config(
        page_title="COVID in NSW", page_icon=":chart_with_upwards_trend:", layout="wide"
    )

    covid_df = load_and_clean_csv()
    dataset_start_date = get_start_date()
    dataset_last_updated_date = get_last_updated_date()
    dataset_last_updated_date_formatted = dataset_last_updated_date.strftime("%d %b %Y")

    zero_day_imputed_df = impute_zero_days_by_lga(covid_df)

    st.title(":chart_with_upwards_trend: COVID in NSW")
    st.write(f"_Last updated: **{dataset_last_updated_date_formatted}**_")

    st.sidebar.header("Filters")
    covid_df = filter_df_by_lga(zero_day_imputed_df)

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

    zero_day_dict = find_zero_day_stats(covid_df)
    last_zero_day_m.metric(
        label='Last "Zero" Day',
        value=datetime.datetime.strftime(zero_day_dict["latest_zero_day"], "%#d %b %Y"),
        delta=f"{zero_day_dict['days_since_last_zero']} days since",
        delta_color="off",
    )

    # visualisations
    st.markdown("**Daily Cases**")
    daily_cases_area_chart = plot_daily_cases_area_chart(zero_day_imputed_df)
    st.pyplot(daily_cases_area_chart)

    st.markdown("**Top 10 LGAs by Total Cases**")
    cases_by_lga_barplot = plot_total_cases_by_lga(zero_day_imputed_df)
    st.pyplot(cases_by_lga_barplot)

    # dataframe
    st.dataframe(covid_df, use_container_width=True)


main()
