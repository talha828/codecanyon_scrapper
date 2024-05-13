import csv
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

option = Options()
option.add_experimental_option("detach",True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=option)

search = "beauty salon"

driver.get(f"https://codecanyon.net/search/{search}")

# Function to create a directory if it doesn't exist

# Find all card elements
cards = driver.find_element("xpath","//div[contains(@class, 'shared-item_cards-card_component__root')]")

img_src = cards.find_elements("xpath","//a[contains(@class, 'shared-item_cards-item_name_component__itemNameLink')]")

hrefs = [link.get_attribute("href") for link in img_src]

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Create a directory to save CSV files
csv_directory = "output"
create_directory(csv_directory)

csv_file = os.path.join(csv_directory, f"{search}_results.csv")
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Index","Title", "Image Link", "Description", "Price", "Sales Count","Product Link"])

    for index,i in enumerate(hrefs):

        print(f"product link saved {index}: {i}")

        driver.get(i)

        title = driver.find_element("xpath", "//h1[contains(@class , 't-heading -color-inherit -size-l h-m0 is-hidden-phone')]").text
        try:
            image_link = driver.find_element("xpath", f"//img[contains(@alt , '{title} - CodeCanyon Item for Sale')]").get_attribute("src")
        except:
            image_link = f"No Link : {i}"

        price = driver.find_element("xpath", "//span[contains(@class , 'js-purchase-price')]").text.replace("$","")
        description = driver.find_element("xpath", "//div[contains(@class , 'js-item-description item-description')]").text
        try:
            sales_count = driver.find_element("xpath", "//div[contains(@class , 'item-header__sales-count')]").text.replace("sales", "").replace("Cart" ,"")
        except:
            sales_count = 0

        writer.writerow([index,title, image_link, description, price, sales_count,i])
        print(index,title)

file.close()

driver.quit()