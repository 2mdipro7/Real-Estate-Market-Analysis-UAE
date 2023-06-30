# Real-Estate-UAE

## Build From Sources
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
4. Download Crome webdriver from - (https://chromedriver.chromium.org/downloads)

5. Run the scraper
```bash
python final.py
```
6. You will get a file named 'property_data.csv' containing all the raw data.

7. Initiate data cleaning
```bash
python data_cleanup.ipynb
```
8. Initiate data segments
```bash
python data_segmentation.ipynb
```

Tableau Public View - https://public.tableau.com/trusted/1rlXLxVgTkWVoxBIw_-jFw==:KWk0bXthU1l4ySFlO7GdFT5W?:redirUrl=%2Fprofile%2Fapi%2Fpublish%2FRealEstateMarketInsigtsofDubai%2FDashboard1
