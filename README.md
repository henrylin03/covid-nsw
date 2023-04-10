# Analysis of COVID Cases in NSW using SQL & Python

This is a personal project aimed at analysing reported COVID cases in New South Wales (NSW), Australia. The project involves data analysis, data pipeline creation, and data visualisation using a combination of SQL and Python.

The main goal of this project was to analyse COVID cases in NSW and gain insights into patterns and trends in its spread. The project involved cleaning and processing the data, analysing the data using SQL and Python, and visualising the data using various graphs and charts.

## Data Pipeline

1. Open _"NSW COVID-19 cases by location"_ `.csv` file directly from NSW Government's website via [URL](https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q=). This is updated by NSW Health weekly.
2. The data is processed and cleaned using Python (`pandas`) and SQL (`sqlite3`), storing the data in an SQLite database.
3. The data is queried using SQL, and visualised using Python libraries such as `seaborn` and `matplotlib`.

## Data Analysis

The data analysis involved querying the data using SQL and Python to obtain various statistics, including:

- Daily cases trends over time
- COVID cases by location
- Days where there were no COVID cases reported ("Zero Days")

## Data Visualisation

Various graphs and charts were created using Python (`seaborn`, `matplotlib`) to visualise the data obtained from the analysis and highlight trends. These included area charts, bar charts and donut charts to identify patterns in time-series data, comparisons between Local Government Areas (LGAs), and show proportions.

## Conclusion

Overall, this project helped me to develop my skills in data analysis, data pipeline creation, and data visualisation. I am confident that the skills I have gained through this project will be useful in my future endeavors in data science and related fields.

Thank you for considering this project. If you have any questions, feedback or other comments, please do not hesitate to let me know via a [GitHub Issue](https://github.com/henrylin03/COVID-NSW/issues).
