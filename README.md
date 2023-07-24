# COVID-19 in NSW: Dashboard

This is a Python dashboard visualising Covid's impact on New South Wales (NSW), Australia. Built on the [Streamlit](https://streamlit.io/) library, this dashboard allows users to interactively explore daily, reported cases from [NSW Health](https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q=).

## Project Overview

This project includes:

- **Interactive Dashboard**: The interactive `streamlit` dashboard is located in `dashboard.py`. It allows users to explore NSW's COVID-19 data, including adjusting visualisation parameters to gain insights.
- **Data Pipeline Building**: The data pipeline is built in `pandas`, automating data fetching, cleaning, and analysis.
- **Data Cleaning & Preparation**: The raw data is cleaned and transformed to remove duplicates, missing values, and other inconsistencies that would impact analyses.
- **Data Exploration & Analysis**: Exploratory data analysis (EDA) is done in a Jupyter notebook using SQL and Python libraries such as `pandas`, `seaborn` and `matplotlib`. The notebook is included in this repository as `analysis.ipynb`.
- **Data Visualisations**: The dashboard includes `seaborn` and `matplotlib` visualisations to highlight key patterns.

## Technologies Used

- **`streamlit`**: for building the interactive dashboard
- **`seaborn` & `matplotlib`**: for data visualisation and exploration
- **`pandas`**: for data cleaning, preparation, and analysis
- **`wikipedia`** : for data fetching using Wikipedia API
- **SQL (`sqlite`)**: for data cleaning, preparation, and manipulation

## How To Use

Access the dashboard via [covid-nsw.streamlit.app](https://covid-nsw.streamlit.app/).

To replicate my EDA, please open and run the `analysis.ipynb` Jupyter notebook to see the results of the analysis:

```bash
jupyter notebook
```

## Conclusion

Through this project, I have expanded my skills in building interactive data dashboards, including building its composite data visualisations, data transformations, and data pipeline.

Please feel free to raise a [GitHub Issue](https://github.com/henrylin03/covid-nsw/issues) if you have any questions or feedback. Thank you!
