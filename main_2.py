from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

# Function to scrape LinkedIn profiles
def scrape_linkedin_data(username, password):
    # Set up the Chrome WebDriver
    service = Service('C:/Users/user/Downloads/chromedriver.exe')  # Update with the correct path
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 10)

    try:
        # Navigate to LinkedIn and log in
        driver.get('https://www.linkedin.com/login')

        # Enter username and password
        wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys(username)
        driver.find_element(By.ID, 'password').send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Verify login success
        if 'feed' not in driver.current_url:
            raise Exception("Login failed. Please check your credentials.")

        # Define a list of profiles to scrape (URLs of IIT graduate profiles)
        profile_urls = [
            'https://www.linkedin.com/in/sample-profile-1/',
            'https://www.linkedin.com/in/sample-profile-2/'
            # Add more profile URLs here
        ]

        # Initialize a list to store scraped data
        data = []

        # Iterate through each profile
        for url in profile_urls:
            driver.get(url)
            time.sleep(3)  # Allow time for the page to load

            try:
                # Extract job title, company, and industry
                name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.text-heading-xlarge'))).text
                job_title = driver.find_element(By.CSS_SELECTOR, '.text-body-medium.break-words').text
                company = driver.find_element(By.CSS_SELECTOR, '.pv-entity__secondary-title').text
                industry = driver.find_element(By.CSS_SELECTOR, '.pv-top-card--list-bullet > li').text

                # Append the data
                data.append({
                    'Name': name,
                    'Job Title': job_title,
                    'Company': company,
                    'Industry': industry
                })
            except NoSuchElementException:
                print(f"Some data missing for profile: {url}")

        # Save data to a CSV file
        df = pd.DataFrame(data)
        df.to_csv('linkedin_data.csv', index=False)
        print("Data saved to linkedin_data.csv")

    except TimeoutException:
        print("Error: Page took too long to load.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        driver.quit()

# Example usage
username = 'your_linkedin_email@example.com'
password = 'your_password'
scrape_linkedin_data(username, password)
