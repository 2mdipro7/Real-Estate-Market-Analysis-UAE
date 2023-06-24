from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

columns = ["World Rank", "National Rank", "Name", "Image URLs", "Affiliation", "Country", "#DBLP", "Citations", "D-Index"]

def get_scholar_details(row):
    details = row.text.split('\n')
    contents = {}
    contents['World Rank'] = details[0]
    contents['National Rank'] = details[1]
    contents['Name'] = details[2]
    contents['Image URLs'] = row.find_element(By.CLASS_NAME, 'lazyload').get_attribute('src')
    contents['Affiliation'] = details[3].split(',')[0]
    contents['Country'] = details[3].split(',')[1].strip()
    contents['#DBLP'] = details[4]
    contents['Citations'] = details[5].replace(',', '')
    contents['D-Index'] = details[6]
    return contents

def main():
    webdriver_path = r"C:\Users\mmdip\Downloads\Compressed\chromedriver_win32\chromedriver.exe"
    scholar_data = []
    page_id = 1

    while True:
        driver = webdriver.Chrome(webdriver_path)
        url = f"https://research.com/scientists-rankings/computer-science?page={page_id}"
        driver.get(url)
        time.sleep(5)

        rankings = driver.find_element(By.ID, "rankingItems")
        rows = rankings.find_elements(By.CLASS_NAME, 'cols')
        for idx, row in enumerate(rows):
            if idx % 4 == 0:
                scholar_data.append(get_scholar_details(row))
        
        driver.quit()
        
        if not rows:
            break  # Break the loop if there are no more rows on the page
        page_id += 1

    df = pd.DataFrame(data=scholar_data, columns=columns)
    df.to_csv("CSE Scientist Data.csv", index=False)
    
if __name__ == "__main__":
    main()
