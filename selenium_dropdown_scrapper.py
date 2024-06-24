import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run headless browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Target website URL
url = "https://www.epfindia.gov.in/site_en/circulars.php"
base_url = "https://www.epfindia.gov.in/"
driver.get(url)

try:
    # Locate the dropdown element
    dropdown = Select(driver.find_element("id", "dd"))  # Replace "dd" with the actual dropdown ID or selector

    # Directory to save PDFs
    links = []

    for index in range(len(dropdown.options)):
        dropdown.select_by_index(index)
        driver.implicitly_wait(3)  # Wait for the page to load after selection

        # Get the current page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all PDF links (assumes PDF links have a specific pattern, e.g., ending with '.pdf')
        pdf_links = soup.find_all('a', href=lambda href: href and href.endswith('.pdf'))

        for link in pdf_links:
            pdf_url = link['href']
            if not pdf_url.startswith('http'):
                pdf_url = base_url + pdf_url[3:]  # Handle relative URLs
            links.append(pdf_url)
            # # Download the PDF
            # response = requests.get(pdf_url)
            # pdf_name = os.path.join("pdfs", os.path.basename(pdf_url))
            # with open(pdf_name, 'wb') as pdf_file:
            #     pdf_file.write(response.content)
            # print(f"Downloaded {pdf_name}")

    # Print out all found PDF links
    # Create a DataFrame
    df = pd.DataFrame(list(set(links)), columns=['PDF Links'])

    # Save the DataFrame to a CSV file (optional)
    df.to_csv('pdf_links.csv', index=False)

    # Display the DataFrame
    print(df)

except NoSuchElementException as e:
    print(f"Error: {e}. The dropdown element was not found. Please check the ID or selector.")

finally:
    # Clean up and close the browser
    driver.quit()
