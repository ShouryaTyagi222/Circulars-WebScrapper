import time
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
# driver.get(base_url)
# URL of the website
url = 'https://revenuedepartment.gujarat.gov.in/circulars'
base = 'https://revenuedepartment.gujarat.gov.in/'

# Function to load more PDF links by clicking 'Show More'
def load_more_pdfs(driver):
    c = 1
    while True:
        try:
            show_more_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Show More')]")
            if show_more_button:
                show_more_button.click()
                time.sleep(4)  # Adjust sleep time if necessary
                # time.sleep(2)  # Adjust sleep time if necessary
            else:
                break
            c+=1
        except Exception as e:
            print(f'No more "Show More" button found: {e}')
            break

# Function to extract PDF links
def extract_pdf_links(driver):
    pdf_links = []
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        href = link['href']
        if href.endswith('.pdf') or href.endswith('.PDF'):
            pdf_links.append(base+href)
    return pdf_links

# Main execution
def main():
    driver.get(url)
    
    # Load more PDF links
    load_more_pdfs(driver)
    
    # Extract all PDF links
    pdf_links = extract_pdf_links(driver)
    
    # Save to CSV
    df = pd.DataFrame(pdf_links, columns=['PDF Links'])
    df.to_csv('pdf_links.csv', index=False)
    
    driver.quit()
    print(f'Successfully saved {len(pdf_links)} PDF links to pdf_links.csv')

if __name__ == '__main__':
    main()
