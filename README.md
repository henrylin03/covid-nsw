# COVID-19 in NSW: Dashboard

This is a Streamlit dashboard for exploring and visualising the impact of the COVID-19 pandemic in New South Wales (NSW), Australia. The dashboard allows users to interactively explore daily reported cases from [NSW Health](https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q=), and gain insights into the pandemic's impact on NSW.

## Project Overview

This project includes the following components

- **Data Pipeline Building**: The data pipeline is built in Python and automates fetching, cleaning, and analysing the data.
- **Data Cleaning & Preparation**: The raw data is cleaned and transformed to remove duplicates, missing values, and other inconsistencies that would affect the analysis.
- **Data Exploration & Analysis**: The exploratory data analysis (EDA) is done in a Jupyter notebook using SQL and Python libraries such as `pandas`, `seaborn` and `matplotlib`. The notebook is included in this repository as `analysis.ipynb`.
- **Data Visualisations**: The dashboard includes several visualisations using `seaborn` and `matplotlib` libraries to communicate key findings and insights from the data.
- **Interactive Dashboard**: The interactive `streamlit` dashboard is located in `dashboard.py`. It allows users to explore NSW's COVID-19 data, including adjusting visualisation parameters to gain insights.

## Technologies Used

- **`streamlit`**: for building the interactive dashboard
- **`seaborn` & `matplotlib`**: for data visualisation and exploration
- **`pandas`**: for data cleaning, preparation, and analysis
- **`wikipedia`**: for downloading tables from Wikipedia pages
- **SQL (`sqlite`)**: for data cleaning, preparation, and manipulation

## How to Use the Project

To access the Streamlit dashboard and explore the COVID-19 data for NSW:

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your_username/covid-nsw.git
   ```
2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the streamlit app:
   ```bash
   streamlit run dashboard.py
   ```

To replicate my EDA, please open and run the `analysis.ipynb` Jupyter notebook to see the results of the analysis:

```bash
jupyter notebook
```

## Conclusion

Through this project, I have expanded my skills in building interactive data dashboards, including building its composite data visualisations, data transformations, and data pipeline.

Please feel free to raise a [GitHub Issue](https://github.com/henrylin03/covid-nsw/issues) if you have any questions or feedback. Thank you!
