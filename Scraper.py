import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

class JobScraper:
    def __init__(self, position, location):
        self.position = position
        self.location = location
        self.driver = self.setup_driver()
        self.scraped_jobs = []
        self.scraped_urls = set()
        self.page_count = 0

    def setup_driver(self):
        options = Options()
        options.use_chromium = True
        service = Service(r"C:\Users\gokul karthik\Music\New folder\msedgedriver.exe")  # Adjust path as needed
        return webdriver.Edge(service=service, options=options)

    def get_url(self):
        """Generate URL from position and location."""
        template = 'https://www.indeed.com/jobs?q={}&l={}'
        return template.format(self.position.replace(' ', '+'), self.location.replace(' ', '+'))

    def extract_job_data(self, card):
        """Extract job data from a single card."""
        try:
            job_title = card.find_element(By.CSS_SELECTOR, '.jobTitle').text
            location = card.find_element(By.CSS_SELECTOR, '.company_location').text
            extract_date = datetime.today().strftime('%Y-%m-%d')
            job_url = card.find_element(By.CSS_SELECTOR, '.jobTitle a').get_attribute('href')
            return job_title, location, extract_date, job_url
        except NoSuchElementException:
            return None
        except TimeoutException:
            return None

    def get_page_records(self, cards):
        """Extract job records from the page."""
        for card in cards:
            record = self.extract_job_data(card)
            if record and record[-1] not in self.scraped_urls:
                self.scraped_jobs.append(record)
                self.scraped_urls.add(record[-1])

    def save_data_to_file(self):
        """Save data to CSV file."""
        with open('results.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['JobTitle', 'Location', 'ExtractDate', 'JobUrl'])
            writer.writerows(self.scraped_jobs)

    def scrape_jobs(self):
        """Main job scraping logic."""
        url = self.get_url()
        self.driver.get(url)
        self.driver.implicitly_wait(10)

        while self.page_count < 2:  # Limit to 2 pages
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'job_seen_beacon'))
                )
                cards = self.driver.find_elements(By.CLASS_NAME, 'job_seen_beacon')
                if not cards:
                    break

                self.get_page_records(cards)

                if self.click_next_page():
                    self.page_count += 1  # Increment page count
                else:
                    break

            except TimeoutException:
                print("Timed out waiting for job cards to load.")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                break

        self.driver.quit()
        self.save_data_to_file()
        print("Data saved to results.csv")

    def click_next_page(self):
        """Click the next page button if available."""
        try:
            next_button = self.driver.find_element(By.XPATH, '//a[@data-testid="pagination-page-next"]')
            if next_button.is_enabled():
                next_button.click()
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'job_seen_beacon'))
                )
                return True
        except NoSuchElementException:
            print("Next button not found.")
        return False

if __name__ == "__main__":
    scraper = JobScraper('python developer', 'charlotte nc')
    scraper.scrape_jobs()
