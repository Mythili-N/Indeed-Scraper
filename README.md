# IndeedScraper

A web scraper that extracts job listings from Indeed for specified job titles and locations using Selenium. The scraped data includes job titles, locations, extraction dates, and job URLs, which are saved to a CSV file.

## Features

- Scrapes job listings from Indeed for specified positions and locations.
- Supports pagination (limited to 2 pages in the current implementation).
- Saves scraped job data to a CSV file.
- Prevents duplicate entries by tracking already scraped job URLs.

## Prerequisites

- Python 3.x
- Selenium library
- Microsoft Edge WebDriver (ensure compatibility with your version of Microsoft Edge)
- An active internet connection

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/job-scraper.git
   cd job-scraper
   ```

2. **Install the required Python packages:**

   ```bash
   pip install selenium
   ```

3. **Download the Edge WebDriver:**

   Ensure the Edge WebDriver is installed and the path is correctly set in the script. Download it from [Microsoft's Edge WebDriver page](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/).

## Usage

1. **Modify the Script:**
   Change the job position and location in the `if __name__ == "__main__":` section:

   ```python
   scraper = JobScraper('python developer', 'charlotte nc')
   ```

2. **Run the Script:**

   ```bash
   python job_scraper.py
   ```

3. **Output:**
   The scraped job listings will be saved to `results.csv` in the same directory. 

## Customization

- **Number of Pages:** The scraper currently limits scraping to 2 pages. You can modify this by changing the condition in the `while self.page_count < 2:` loop in the `scrape_jobs` method.

