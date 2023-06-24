from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

columns = ["Ad Type", "Agent Type", "Property Type", "Price", "Details", "Service Type", "Address", "Bedrooms", "Bathrooms", "Area (sqft)", "Listed on", "Agent Name", "Agent Position", "Total Properties", "Spoken Languages by Agent", "Reference Number", "Broker ORN", "Agent BRN"]

def get_property_details(row, driver):
    details = row.text.split('\n')
    print("Details:", details)
    contents = {}
    
    if "SUPERAGENT" in details[1].upper() and "VERIFIED" in details[0].upper():
        contents["Ad Type"] = details[0]
        contents["Agent Type"] = details[1]
        contents["Property Type"] = details[2]
        contents["Price"] = details[3].split()[0].replace(",", "")
        contents["Details"] = details[4]
        contents["Service Type"] = details[5]
        contents["Address"] = details[6]
        contents["Bedrooms"] = details[7].split()[0]
        contents["Bathrooms"] = details[8].split()[0]
        contents["Area (sqft)"] = details[9].split()[0].replace(",", "")
        contents["Listed on"] = details[10]
    elif "VERIFIED" in details[0].upper():
        contents["Ad Type"] = details[0]
        contents["Agent Type"] = "REGULAR"
        contents["Property Type"] = details[1]
        contents["Price"] = details[2].split()[0].replace(",", "")
        contents["Details"] = details[3]
        contents["Service Type"] = details[4]
        contents["Address"] = details[5]
        contents["Bedrooms"] = details[6].split()[0]
        contents["Bathrooms"] = details[7].split()[0]
        contents["Area (sqft)"] = details[8].split()[0].replace(",", "")
        contents["Listed on"] = details[9]
    elif "SUPERAGENT" in details[0].upper():
        contents["Ad Type"] = "UNVERIFIED"
        contents["Agent Type"] = details[0]
        contents["Property Type"] = details[1]
        contents["Price"] = details[2].split()[0].replace(",", "")
        contents["Details"] = details[3]
        contents["Service Type"] = details[4]
        contents["Address"] = details[5]
        contents["Bedrooms"] = details[6].split()[0]
        contents["Bathrooms"] = details[7].split()[0]
        contents["Area (sqft)"] = details[8].split()[0].replace(",", "")
        contents["Listed on"] = details[9]
    elif "SUPERAGENT" not in details[1].upper() and "VERIFIED" not in details[0].upper():
        contents["Ad Type"] = "UNVERIFIED"
        contents["Agent Type"] = "REGULAR"
        contents["Property Type"] = details[0]
        contents["Price (AED)"] = details[1].split()[0].replace(",", "")
        contents["Details"] = details[2]
        contents["Service Type"] = details[3]
        contents["Address"] = details[4]
        contents["Bedrooms"] = details[5].split()[0]
        contents["Bathrooms"] = details[6].split()[0]
        contents["Area (sqft)"] = details[7].split()[0].replace(",", "")
        contents["Listed on"] = details[8]
   
    property_url = row.find_element(By.TAG_NAME, "a").get_attribute("href")
    driver.execute_script("window.open(arguments[0]);", property_url)
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(5)  # Delay to allow the property page to load

    # Locate and extract additional information from the property page
    try:
        property_info_element = driver.find_element(By.CLASS_NAME, "property-agent")
        property_info = property_info_element.text
        agent_details = property_info.split("\n")
        
        contents["Agent Name"] = agent_details[1]
        contents["Agent Position"] = agent_details[2]
        contents["Total Properties"] = agent_details[3].split()[0]
        contents["Spoken Languages by Agent"] = agent_details[4].split()
    except NoSuchElementException:
        print("Error occurred: Unable to locate property agent information")
    try:
        property_id_elements = driver.find_element(By.CLASS_NAME, "property-page__legal-list-area")
        property_id_info = property_id_elements.find_element(By.TAG_NAME, "li").text
        id_details = property_id_info.split("\n")

        if len(id_details) >= 4:
            contents["Reference Number"] = id_details[0]
            contents["Broker ORN"] = id_details[2]
            contents["Agent BRN"] = id_details[3]
        else:
            print("Error occurred: Unable to extract complete property id information")
    except NoSuchElementException:
            print("Error occurred: Unable to locate property id information")


    driver.close()  # Close the property page
    driver.switch_to.window(driver.window_handles[0])  # Switch back to the homepage
    
    return contents

def main():
    webdriver_path = r"C:\Users\mmdip\Downloads\Compressed\chromedriver_win32\new\chromedriver.exe"
    property_data = []

    page_id = 1
    count = 0

    while True:
        driver = webdriver.Chrome(webdriver_path)
        url = f"https://www.propertyfinder.ae/en/buy/properties-for-sale.html?page={page_id}"
        driver.get(url)
        time.sleep(5)

        try:
            item_id = driver.find_element(By.CLASS_NAME, "card-list--property")
            rows = item_id.find_elements(By.TAG_NAME, "article")
            for idx, row in enumerate(rows):
                try:
                    property_details = get_property_details(row, driver)
                    property_data.append(property_details)
                    count += 1
                    print(f"Property {count} index: {count-1}")
                    print(f"Property {idx+1} details: {property_details}")

                except NoSuchElementException:
                    print(f"Error occurred for Property {idx+1}: Unable to locate property details. Skipping...")

        except NoSuchElementException:
            print(f"Error occurred while fetching property listings: Unable to locate property elements. Exiting...")
            break

        driver.quit()

        if count == 50:
            break

        page_id += 1

    df = pd.DataFrame(property_data, columns=columns)
    df.head(50).to_csv("property_data1.csv", index=False)
    print("property_data1.csv")

if __name__ == "__main__":
    main()
