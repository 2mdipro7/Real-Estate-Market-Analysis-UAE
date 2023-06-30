# Real Estate UAE

## Description

This project focused on data analysis and visualization using Tableau and Python, incorporating data scraped from the website PropertyFinder.ae. The objective was to analyze and gain insights from a dataset containing information about properties, agents, companies, amenities, and language. The dataset included various attributes such as property type, price, area, agent details, company information, and amenity names.

We performed several tasks throughout the project and implemented various visualization techniques to better explore and understand the data. We also conducted web scraping from PropertyFinder.ae to gather the latest property data for our analysis.

Some of the key tasks and accomplishments include:
Data Scraping:

  Developed a web scraping script to extract property data from PropertyFinder.ae.
  Gathered property details such as property type, price, area, bedrooms, bathrooms, and location.

Data Cleaning and Preparation:

  Imported the scraped data into Python and loaded it into a pandas DataFrame.
  Conducted data cleaning, including handling missing values, removing duplicates, and formatting columns.
  Performed data transformations and created derived columns to enhance the analysis.
  
Data Visualization in Tableau:

  Created interactive dashboards in Tableau to provide a comprehensive view of the data.
  Developed multiple visualizations, including bar charts, line charts, scatter plots, maps, and heat maps, to showcase different aspects of the data.
  Implemented filters, tooltips, and context filters to enable interactivity and allow users to dynamically explore and analyze the data.
  Designed dashboards with multiple sheets and coordinated actions to provide a cohesive and intuitive user experience.

Analysis and Insights:

  Explored the relationship between property prices and various factors such as area, bedrooms, and property type using scatter plots and box plots.
  Analyzed the distribution of property types listed by agents using stacked bar charts and treemaps.
  Visualized the price range distribution across different property types and emirates using box plots and violin plots.


## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Clone the repo
```bash
git clone https://github.com/2mdipro7/Real-Estate-UAE.git
```
2. Initialize and activate the virtual environment
```bash
virtualenv --no-site-packages venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirement.txt
```

## Usage

1. Download Chrome web driver from - (https://chromedriver.chromium.org/downloads)

2. Run the scraper
```bash
python final.py
```
3. You will get a file named 'property_data.csv' containing all the raw data.
4. Make sure to import the scraped data as df in the data cleaning notebook.

5. Initiate data cleaning
```bash
python data_cleanup.ipynb
```
You will get 7 separate CSV files, that represent separate tables.
Combine all the files into a single Excel Worksheet.

5. Initiate data segments
```bash
python data_segmentation.ipynb
```
6. You will get a new properties table with its segmented data. Replace all the data in the property sheet with these new segmented data.
7. Load this dataset into Tableau.

## Contributing

If you come up with some interesting findings, add the Tableau dashboard link to the repo.

## License

All Rights of this data belong to PropertyFInder.ae

##Insights
https://public.tableau.com/app/profile/mehrab.mashrafi/viz/RealEstateMarketInsigtsofDubai/PropertyInsights?publish=yes

