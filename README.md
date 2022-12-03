# covid-nsw

In this project, I analyse reported COVID-19 case numbers in New South Wales (NSW), Australia.

<p align="center">
    <img src="https://www.nsw.gov.au/sites/default/files/2020-06/covid-safe-logo.png" alt="" width="275">
</p>

## Description

### Analysis: `covid-nsw.ipynb`

In the `covid-nsw.ipynb` Jupyter Notebook, I provide analysis of reported COVID cases in NSW in a Python environment:

- For cleaning, querying and transforming data, I used:

  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/2560px-Pandas_logo.svg.png" alt="" width="250" align="center"> <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/SQLite370.svg/1280px-SQLite370.png" alt="" width="250" align="center">

- For visualising data, I primarily used:

  <img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_003.png" alt="" width="250" align="center"> <img src="https://miro.medium.com/max/819/1*5VKgpRUCInBKmWBXFvSvvA.png" alt="" width="225" align="center">

### Downloading input file: `download_csv.py`

`covid-nsw.ipynb` imports the `download_csv.py` script, which uses `selenium` to download the latest `.csv` input file from [NSW COVID-19 cases by location](https://data.nsw.gov.au/search/dataset/ds-nsw-ckan-aefcde60-3b0c-4bc0-9af1-6fe652944ec2/details?q=), as published by NSW Health.

## Feedback

Thank you for joining me on my journey to learn coding and data analysis! If you have any feedback, please let me know via a [GitHub Issue](https://github.com/henrylin03/COVID-NSW/issues).
