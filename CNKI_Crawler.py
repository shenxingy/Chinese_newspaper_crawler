import os
import time
import argparse
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

parser = argparse.ArgumentParser(description='CNKI Crawler')
parser.add_argument('--keyword', type=str, default='疫情', help='keyword to search')
parser.add_argument('--start_date', type=str, default='2022-04-01', help='start date')
parser.add_argument('--end_date', type=str, default='2022-06-01', help='end date')
parser.add_argument('--start_page', type=int, default=15, help='start page')
parser.add_argument('--end_page', type=int, default=31, help='end page')
parser.add_argument('--newpaper_url', type=str, default='https://navi.cnki.net/knavi/newspapers/JFRB/detail?uniplatform=NZKPT', help='newpaper url')
args = parser.parse_args()

def go_to_page(driver, page_num):
    # Wait for the page box to become visible
    page_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "pagebox")))
    
    i = 1
    while True:
        try:
            # Find and click on the page link
            page = page_box.find_element(By.LINK_TEXT, str(page_num))
            page.click()
            time.sleep(1)
            break
        except:
            i += 4
            # Find and click on the page link
            page = page_box.find_element(By.LINK_TEXT, str(i))
            page.click()
            time.sleep(1)

def search_keyword(driver, keyword):
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "J_searchTxt"))
    )
    
    search_box.send_keys(keyword)
    time.sleep(2)

    # press enter
    search_box.send_keys(Keys.ENTER)
    time.sleep(1)

def sort_by_date(driver):
    # hover over the sorting options dropdown
    sort_dropdown = driver.find_element(By.CLASS_NAME, "sort_select_default")
    ActionChains(driver).move_to_element(sort_dropdown).perform()

    # select the date option and then click on it
    date_option = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@name="DT"]'))
    )
    date_option.click()
    time.sleep(1)

def login(driver):
    go_to_page(driver, 1)
    # Find the <tbody> element within the table (assuming there is only one table)
    tbody = driver.find_element(By.XPATH, "//table/tbody")

    # Find all <tr> elements within the <tbody>
    rows = tbody.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        link = row.find_element(By.XPATH, ".//td[@class='name']/a").get_attribute("href")
        # click on the link
        driver.get(link)
        html_link = driver.find_element(By.CLASS_NAME, "btn-html")
        html_link.click()
        time.sleep(1.1)
        break
    while True:
        user_input = input("Please login manually, and then press 'y' to continue: ")
        if user_input == 'y':
            return
        else:
            print("Invalid input. Please try again.")

# download the page
def download_page(driver, page_num):
    go_to_page(driver, page_num)
    
    # Find the <tbody> element within the table (assuming there is only one table)
    tbody = driver.find_element(By.XPATH, "//table/tbody")
    # Find all <tr> elements within the <tbody>
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    links = []
    contents = []
    keywords = []
    for row in rows:
        link = row.find_element(By.XPATH, ".//td[@class='name']/a").get_attribute("href")
        links.append(link)
        driver.get(link)
        keyword = driver.find_element(By.CLASS_NAME, "keywords").text
        keywords.append(keyword)
        time.sleep(1.2)
        html_link = driver.find_element(By.CLASS_NAME, "btn-html")
        html_link.click()
        time.sleep(1.5)
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        elements = driver.find_elements(By.XPATH, ".//*[contains(@class, 'p1') or contains(@class, 'anchor-tag')]")
        text = ""
        for element in elements:
            text += element.text
            text += "\n"
        contents.append(text)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        driver.back()
        time.sleep(1)

    tbody_text = tbody.text
    tbody_text = tbody_text.split("\n")

    for i in range(len(tbody_text)):
        if i % 2 == 0:
            # split by the first space
            tbody_text[i] = tbody_text[i].split(" ", 1)
        else:
            if ";" not in tbody_text[i]:
                for k in range(len(tbody_text[i])):
                    if tbody_text[i][k].isnumeric():
                        tbody_text[i] = tbody_text[i][k:]
                        tbody_text[i] = 'NA; ' + tbody_text[i]
                        break
            tbody_text[i] = tbody_text[i].split(" ")
            if len(tbody_text[i]) == 3:
                tbody_text[i].append('0')

    # combine the odd and even rows to a large list
    tbody_text = [item for sublist in tbody_text for item in sublist]
    tbody_text = np.array(tbody_text).reshape(-1, 6)
    tbody_text = pd.DataFrame(tbody_text, columns=["Number", "Title", "Author", "banHao", "Date", "Download"])
    tbody_text["Links"] = links
    tbody_text["Contents"] = contents
    tbody_text["Keywords"] = keywords
    page_df = tbody_text.copy()
    return page_df

def combine_pages(folder_name):
    # Get a list of all CSV files in the folder
    page_files = [f for f in os.listdir(folder_name) if f.endswith('.csv')]

    # Initialize an empty list to store DataFrames
    pages = []

    # Loop through the CSV files and read them into DataFrames
    for page in page_files:
        file_path = os.path.join(folder_name, page)
        df = pd.read_csv(file_path)
        pages.append(df)
        os.remove(file_path)
        
    os.rmdir(folder_name)
    pages = pd.concat(pages)
    
    # keep unique rows
    pages = pages.drop_duplicates()
    pages = pages.reset_index(drop=True)
    return pages

def main():
    driver = webdriver.Chrome()
    driver.get(args.newpaper_url)
    search_keyword(driver, args.keyword)
    sort_by_date(driver)
    login(driver)
    
    # go to the initial page
    driver.minimize_window()
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.back()
    
    start = args.start_page
    end = args.end_page
    folder_name = "pages"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    for i in range(start, end + 1):
        df_current = download_page(driver, i)
        file_name = os.path.join(folder_name, "page" + str(i) + ".csv")
        df_current.to_csv(file_name, index=False, encoding="utf-8-sig")
        
    
    pages = combine_pages(folder_name)
    
    # filter by date
    pages["Date"] = pd.to_datetime(pages["Date"])
    pages = pages.sort_values(by="Date")
    pages = pages[(pages["Date"] >= args.start_date) & (pages["Date"] <= args.end_date)]
    pages = pages.reset_index(drop=True)
    pages.to_csv("CNKI.csv", index=False, encoding="utf-8-sig")
    driver.quit()
    
if __name__ == '__main__':
    main()