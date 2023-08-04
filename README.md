# Real Estate Market Analysis of UAE

## Table of Contents

- [Description](#description)
- [Insights](#insights)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Description

This project focused on data analysis and visualization using Tableau and Python, incorporating data scraped from the website PropertyFinder.ae. The objective was to analyze and gain insights from a dataset containing information about properties, agents, companies, amenities, and language. The dataset included various attributes such as property type, price, area, agent details, company information, and amenity names.

We performed several tasks throughout the project and implemented various visualization techniques to better explore and understand the Real Estate Market of UAE. To achieve that, we collected the data from scraping the PropertyFinder.ae website and then carefully cleaned the data. After that we implemented some additional segmentation of the data to help with our analysis.

Step-by-step description of the key tasks and accomplishments are as follows:

**Data Scraping:**

  1. Developed a web scraping script to extract property data from PropertyFinder.ae.
  2. Gathered property details such as property type, price, area, bedrooms, bathrooms, and location.

**Data Cleaning and Segmentation:**

  1. Imported the scraped data into Python and loaded it into a pandas DataFrame.
  2. Conducted data cleaning, including handling missing values, removing duplicates, and formatting columns.
  3. Performed data transformations and created derived columns to enhance the analysis.
  
**Data Visualization in Tableau:**

  1. Created interactive dashboards in Tableau to provide a comprehensive view of the data.
  2. Developed multiple visualizations, including bar charts, line charts, scatter plots, maps, and heat maps, to showcase different aspects of the data.
  3. Implemented filters, tooltips, and context filters to enable interactivity and allow users to dynamically explore and analyze the data.
  4. Designed dashboards with multiple sheets and coordinated actions to provide a cohesive and intuitive user experience.

**Analysis and Insights:**

  1. Explored the relationship between property prices and various factors such as area, bedrooms, and property type using various plots.
  2. Analyzed the distribution of property types listed by agents using stacked bar charts and treemaps.
  3. Visualized the price range distribution across different property types and emirates using several plots.

**Interesting Findings:**

  1. There is a general trend toward the availability of expensive properties. We observed a compelling trend indicating a higher abundance of expensive properties. As property values decrease, their availability also declines.
  2. Apartments are the predominant property type, followed by villa and townhouse.
  3. Jumeirah Village Circle, Downtown Dubai and Dubai Marina are the best place for finding a property within lowest price range.

  **Please note that the dashboards are interactive and can lead to multiple insights by clicking on different area of the chart.**

## Insights
1. Property Insights - https://public.tableau.com/app/profile/mehrab.mashrafi/viz/RealEstateMarketAnalysisofUAE/PropertyInsights?publish=yes
2. Agent and Company Performance Insights - https://public.tableau.com/app/profile/mehrab.mashrafi/viz/RealEstateMarketAnalysisofUAE/AgentPerformance?publish=yes


## Installation

1. Clone the repo
```bash
git clone https://github.com/2mdipro7/Real-Estate-Market-Analysis-UAE.git
```
2. Initialize and activate the virtual environment
```bash
virtualenv --no-site-packages venv
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

1. Download Chrome web driver from - (https://chromedriver.chromium.org/downloads)

2. Run the scraper
```bash
python scraper.py
```
3. You will get a file named 'property_data.csv' containing all the raw data.
4. Make sure to import the scraped data as df in the data cleaning notebook.

5. Initiate data cleaning
```bash
jupyter nbconvert --execute data_cleanup.ipynb
```
You will get 7 separate CSV files, that represent separate tables.
Combine all the files into a single Excel Worksheet.

5. Initiate data segments
```bash
jupyter nbconvert --execute data_segmentation.ipynb
```
6. You will get a new properties table with its segmented data. Replace all the data in the property sheet with these new segmented data.
7. Load this dataset into Tableau.

## Contributing

If you come up with some interesting findings, add the Tableau dashboard link to the repo.

## License

All Rights of this data belong to PropertyFinder.ae

