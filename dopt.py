from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd

from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Selenium webdriver
driver = webdriver.Chrome()  # You need to have Chrome driver installed
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=driver)
base_url = "https://www.uppcl.org/uppcl/en/archivecirculars"
driver.get(base_url)

link = 'https://www.uppcl.org/'
# Function to extract PDF links
def extract_links_from_page(url):
    driver.implicitly_wait(3)  # Wait for the page to load after selection
    soup = BeautifulSoup(url, 'html.parser')
    links = []
    for a in soup.find_all('a', href=True):
        if a['href'].endswith('.pdf'):
            links.append(link + a['href'][5:])
    print(len(links))
    return links


# Main function to iterate through all pages and extract links
def extract_all_links(base_url):
    all_links = []
    page = 0
    next_page = driver.current_url
    while next_page:
        page+=1
        links_on_page = extract_links_from_page(driver.page_source)
        all_links.extend(links_on_page)
        next_page_element = driver.find_element("xpath", f"//a[text()='{page}']")
        next_page_element.click()
        driver.implicitly_wait(3)  # Wait for the page to load after selection
        next_page = driver.current_url
    return all_links

if __name__ == "__main__":
    all_pdf_links = extract_all_links(base_url)
    print("Total PDF links extracted:", len(list(set(all_pdf_links))))
    # print(all_pdf_links)
    # Create a DataFrame
    df = pd.DataFrame(list(set(all_pdf_links)), columns=['PDF Links'])

    # Save the DataFrame to a CSV file (optional)
    df.to_csv('pdf_links.csv', index=False)

    # Display the DataFrame
    print(df)

# Close the browser after extraction
driver.quit()
