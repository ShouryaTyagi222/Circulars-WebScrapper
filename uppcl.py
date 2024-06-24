from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import pandas as pd
import time
base = 'https://www.uppcl.org/'

def get_pdf_links(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    pdf_links = []
    for link in soup.find_all('a', href=True):
        if '.pdf' in link['href'] or '.PDF' in link['href']:
            pdf_links.append(base+link['href'][6:])
            print(base+link['href'][6:])
    return pdf_links

def get_total_pages(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    pagination_links = soup.find_all('a', href=True, text=re.compile(r'\d+'))
    if pagination_links:
        return max([int(link.text) for link in pagination_links if link.text.isdigit()])
    return 1

def scrape_all_pdfs(base_url):
    pdf_links = []

    # Set up the Selenium WebDriver (using Chrome in this example)
    driver = webdriver.Chrome()
    driver.get(base_url)

    total_pages = 72

    for page_number in range(1, total_pages + 1):
        print(f"Scraping page {page_number}")
        pdf_links.extend(get_pdf_links(driver))
        
        # If it's not the last page, click the next page link
        try:
            if page_number < total_pages:
                next_page_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, str(page_number + 1)))
                )
                next_page_button.click()
                time.sleep(2)
        except:
            ellipsis_buttons = driver.find_elements(By.XPATH, "//a[text()='...']")
            for btn in ellipsis_buttons:
                continue
            btn.click()
            time.sleep(2)

    driver.quit()
    return pdf_links

if __name__ == "__main__":
    base_url = 'https://www.uppcl.org/uppcl/en/archivecirculars'
    all_pdf_links = scrape_all_pdfs(base_url)
    
    df = pd.DataFrame(list(set(all_pdf_links)), columns=['PDF Links'])
    df.to_csv('pdf_links.csv', index=False)
    print(df)
    
    print(f"Total {len(all_pdf_links)} PDF links scraped and saved to pdf_links.txt")