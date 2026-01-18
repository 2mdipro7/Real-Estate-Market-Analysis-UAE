"""
Property Finder UAE Web Scraper
A professional scraper for extracting real estate data from propertyfinder.ae
"""

import logging
import time
import argparse
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException
)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Property:
    """Data class representing a property listing"""
    ad_type: str = ""
    agent_type: str = ""
    property_type: str = ""
    price_aed: str = ""
    details: str = ""
    service_type: str = ""
    address: str = ""
    bedrooms: str = ""
    bathrooms: str = ""
    area_sqft: str = ""
    listed_on: str = ""
    agent_name: str = ""
    agent_position: str = ""
    total_properties: str = ""
    spoken_languages: str = ""
    reference: str = ""
    broker_orn: str = ""
    agent_brn: str = ""
    amenities: List[str] = field(default_factory=list)
    dld_permit_number: str = ""

    def to_dict(self) -> Dict:
        """Convert Property to dictionary"""
        data = asdict(self)
        data['amenities'] = ', '.join(data['amenities']) if data['amenities'] else ""
        return data


class PropertyFinderConfig:
    """Configuration for the Property Finder scraper"""

    BASE_URL = "https://www.propertyfinder.ae/en/search"

    #SEARCH_PARAMS = "?c=2&fu=0&rp=y"  # Buy, Residential, Ready properties
    SEARCH_PARAMS = "?l=6&c=1&fu=0&ob=mr" # Buy c=1,  Rent c=2

    # CSS Selectors - Updated for current Property Finder website
    PROPERTY_CARD = "article[data-testid='property-card']"
    PROPERTY_LINK = "a[data-testid='property-card-link']"
    PROPERTY_PRICE = "span[data-testid='property-card-price']"
    PROPERTY_TITLE = "h2[data-testid='property-card-title']"
    PROPERTY_LOCATION = "div[data-testid='property-card-location']"
    PROPERTY_SPECS = "div[data-testid='property-card-spec']"
    AGENT_SECTION = "div[data-testid='agent-info']"
    AMENITIES_SECTION = "div[data-testid='amenities-section']"

    # Timeouts
    PAGE_LOAD_TIMEOUT = 10
    ELEMENT_TIMEOUT = 5

    # Scraping limits
    MAX_PROPERTIES = 1500
    PAGE_DELAY = 2


class PropertyParser:
    """Handles parsing of property data from page elements"""

    @staticmethod
    def parse_card_details(card_text: str) -> Dict[str, str]:
        """Parse property card text into structured data"""
        details = card_text.split('\n')
        parsed = {}

        try:
            # Determine property type based on badges
            parsed['ad_type'] = "VERIFIED" if "VERIFIED" in card_text.upper() else "UNVERIFIED"
            parsed['agent_type'] = "SUPERAGENT" if "SUPERAGENT" in card_text.upper() else "REGULAR"

            # Find price (contains "AED")
            for idx, line in enumerate(details):
                if "AED" in line or line.replace(',', '').replace('.', '').isdigit():
                    parsed['price_aed'] = line.split()[0].replace(",", "")
                    break

            # Extract basic property info
            for line in details:
                if any(ptype in line.lower() for ptype in ['apartment', 'villa', 'townhouse', 'penthouse', 'duplex']):
                    parsed['property_type'] = line
                elif 'bedroom' in line.lower() or 'bed' in line.lower():
                    parsed['bedrooms'] = line.split()[0]
                elif 'bathroom' in line.lower() or 'bath' in line.lower():
                    parsed['bathrooms'] = line.split()[0]
                elif 'sqft' in line.lower() or 'sq.ft' in line.lower():
                    parsed['area_sqft'] = line.split()[0].replace(",", "")
                elif 'premium' in line.lower():
                    parsed['service_type'] = line

        except (IndexError, ValueError) as e:
            logger.warning(f"Error parsing card details: {e}")

        return parsed

    @staticmethod
    def extract_text_safe(driver, by: By, selector: str, default: str = "") -> str:
        """Safely extract text from element"""
        try:
            element = WebDriverWait(driver, PropertyFinderConfig.ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((by, selector))
            )
            return element.text.strip()
        except (NoSuchElementException, TimeoutException):
            return default

    @staticmethod
    def extract_elements_text(driver, by: By, selector: str) -> List[str]:
        """Extract text from multiple elements"""
        try:
            elements = driver.find_elements(by, selector)
            return [elem.text.strip() for elem in elements if elem.text.strip()]
        except NoSuchElementException:
            return []


class PropertyDetailsScraper:
    """Handles scraping of detailed property information"""

    def __init__(self, driver):
        self.driver = driver
        self.parser = PropertyParser()

    def scrape_property_page(self, property_url: str) -> Dict[str, str]:
        """Scrape detailed information from property page"""
        details = {}
        original_window = self.driver.current_window_handle

        try:
            # Open property page in new tab
            self.driver.execute_script("window.open(arguments[0]);", property_url)
            self.driver.switch_to.window(self.driver.window_handles[-1])

            # Wait for page load
            WebDriverWait(self.driver, PropertyFinderConfig.PAGE_LOAD_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)

            # Extract agent information
            details.update(self._extract_agent_info())

            # Extract property details
            details.update(self._extract_property_details())

            # Extract amenities
            details['amenities'] = self._extract_amenities()

        except Exception as e:
            logger.error(f"Error scraping property page {property_url}: {e}")
        finally:
            # Close tab and switch back
            try:
                self.driver.close()
                self.driver.switch_to.window(original_window)
            except WebDriverException:
                pass

        return details

    def _extract_agent_info(self) -> Dict[str, str]:
        """Extract agent information from property page"""
        info = {}

        try:
            # Look for agent section with various possible selectors
            selectors = [
                "div.property-agent",
                "div[class*='agent']",
                "section[class*='agent']"
            ]

            agent_text = ""
            for selector in selectors:
                agent_text = self.parser.extract_text_safe(self.driver, By.CSS_SELECTOR, selector)
                if agent_text:
                    break

            if agent_text:
                agent_lines = agent_text.split('\n')
                if len(agent_lines) > 1:
                    info['agent_name'] = agent_lines[1] if len(agent_lines) > 1 else ""
                    info['agent_position'] = agent_lines[2] if len(agent_lines) > 2 else ""
                    info['total_properties'] = agent_lines[3].split()[0] if len(agent_lines) > 3 else ""
                    info['spoken_languages'] = agent_lines[4] if len(agent_lines) > 4 else ""
        except Exception as e:
            logger.warning(f"Error extracting agent info: {e}")

        return info

    def _extract_property_details(self) -> Dict[str, str]:
        """Extract property reference and legal details"""
        details = {}

        # Try multiple XPath strategies for property details
        detail_mappings = {
            'reference': ["Reference", "Ref No", "Property ID"],
            'broker_orn': ["Broker ORN", "ORN"],
            'agent_brn': ["Agent BRN", "BRN"],
            'dld_permit_number': ["DLD Permit Number", "Permit No", "RERA"]
        }

        for key, labels in detail_mappings.items():
            for label in labels:
                try:
                    xpath = f"//div[contains(text(),'{label}')]/following-sibling::div"
                    element = self.driver.find_element(By.XPATH, xpath)
                    details[key] = element.text.strip()
                    break
                except NoSuchElementException:
                    continue

            if key not in details:
                details[key] = ""

        # Try alternative selectors for DLD permit
        if not details.get('dld_permit_number'):
            dld_selectors = [
                "div.property-page__legal-list-rera-number",
                "div[class*='rera']",
                "span[class*='permit']"
            ]
            for selector in dld_selectors:
                details['dld_permit_number'] = self.parser.extract_text_safe(
                    self.driver, By.CSS_SELECTOR, selector
                )
                if details['dld_permit_number']:
                    break

        return details

    def _extract_amenities(self) -> List[str]:
        """Extract property amenities"""
        amenities_selectors = [
            "div.property-amenities li",
            "div[class*='amenities'] li",
            "ul[class*='amenities'] li"
        ]

        for selector in amenities_selectors:
            amenities = self.parser.extract_elements_text(self.driver, By.CSS_SELECTOR, selector)
            if amenities:
                return amenities

        return []


class PropertyFinderScraper:
    """Main scraper class for Property Finder UAE"""

    def __init__(self, chromedriver_path: Optional[str] = None, headless: bool = False):
        """
        Initialize the scraper

        Args:
            chromedriver_path: Path to chromedriver executable
            headless: Run browser in headless mode
        """
        self.chromedriver_path = chromedriver_path
        self.headless = headless
        self.driver = None
        self.properties: List[Property] = []
        self.parser = PropertyParser()

        logger.info("PropertyFinderScraper initialized")

    def _setup_driver(self):
        """Setup Chrome WebDriver with options"""
        options = Options()

        if self.headless:
            options.add_argument('--headless')

        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        try:
            if self.chromedriver_path:
                service = Service(self.chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
            else:
                self.driver = webdriver.Chrome(options=options)

            logger.info("WebDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def _scrape_property_card(self, card_element, index: int) -> Optional[Property]:
        """Scrape a single property card"""
        try:
            # Get card text for initial parsing
            card_text = card_element.text

            # Parse basic details from card
            parsed_data = self.parser.parse_card_details(card_text)

            # Get property URL
            try:
                link = card_element.find_element(By.TAG_NAME, "a")
                property_url = link.get_attribute("href")
            except NoSuchElementException:
                logger.warning(f"Property {index}: No link found")
                return None

            # Get detailed information from property page
            details_scraper = PropertyDetailsScraper(self.driver)
            detailed_info = details_scraper.scrape_property_page(property_url)

            # Merge all data
            parsed_data.update(detailed_info)

            # Create Property object
            property_obj = Property(
                ad_type=parsed_data.get('ad_type', ''),
                agent_type=parsed_data.get('agent_type', ''),
                property_type=parsed_data.get('property_type', ''),
                price_aed=parsed_data.get('price_aed', ''),
                details=parsed_data.get('details', ''),
                service_type=parsed_data.get('service_type', ''),
                address=parsed_data.get('address', ''),
                bedrooms=parsed_data.get('bedrooms', ''),
                bathrooms=parsed_data.get('bathrooms', ''),
                area_sqft=parsed_data.get('area_sqft', ''),
                listed_on=parsed_data.get('listed_on', ''),
                agent_name=parsed_data.get('agent_name', ''),
                agent_position=parsed_data.get('agent_position', ''),
                total_properties=parsed_data.get('total_properties', ''),
                spoken_languages=parsed_data.get('spoken_languages', ''),
                reference=parsed_data.get('reference', ''),
                broker_orn=parsed_data.get('broker_orn', ''),
                agent_brn=parsed_data.get('agent_brn', ''),
                amenities=parsed_data.get('amenities', []),
                dld_permit_number=parsed_data.get('dld_permit_number', '')
            )

            logger.info(f"Property {index} scraped successfully: {property_obj.property_type} at {property_obj.address}")
            return property_obj

        except Exception as e:
            logger.error(f"Error scraping property {index}: {e}", exc_info=True)
            return None

    def _scrape_page(self, page_number: int) -> int:
        """Scrape a single page of listings"""
        url = f"{PropertyFinderConfig.BASE_URL}{PropertyFinderConfig.SEARCH_PARAMS}&page={page_number}"
        logger.debug(url)
        self.driver.get(url)
        time.sleep(PropertyFinderConfig.PAGE_LOAD_TIMEOUT)
        logger.info(f"Scraping page {page_number}: {url}")

        try:
            self.driver.get(url)
            logger.info("Sleep after getting url")
            time.sleep(PropertyFinderConfig.PAGE_DELAY)

            # Wait for property cards to load
            logger.info("Waiting for page to load")
            WebDriverWait(self.driver, PropertyFinderConfig.PAGE_LOAD_TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )


            # Find all property cards
            logger.info("Finding elements by tag name")
            cards = self.driver.find_elements(By.TAG_NAME, "article")

            if not cards:
                logger.warning(f"No property cards found on page {page_number}")
                return 0

            logger.info(f"Found {len(cards)} properties on page {page_number}")

            # Scrape each card
            scraped_count = 0
            for idx, card in enumerate(cards, 1):
                if len(self.properties) >= PropertyFinderConfig.MAX_PROPERTIES:
                    logger.info(f"Reached maximum properties limit: {PropertyFinderConfig.MAX_PROPERTIES}")
                    return scraped_count

                property_obj = self._scrape_property_card(card, len(self.properties) + 1)
                if property_obj:
                    self.properties.append(property_obj)
                    scraped_count += 1

            return scraped_count

        except TimeoutException:
            logger.error(f"Timeout loading page {page_number}")
            return 0
        except Exception as e:
            logger.error(f"Error scraping page {page_number}: {e}", exc_info=True)
            return 0

    def scrape(self, start_page: int = 1, max_pages: Optional[int] = None) -> List[Property]:
        """
        Start scraping process

        Args:
            start_page: Page number to start from
            max_pages: Maximum number of pages to scrape

        Returns:
            List of scraped Property objects
        """
        self._setup_driver()

        page_number = start_page
        pages_scraped = 0

        try:
            while len(self.properties) < PropertyFinderConfig.MAX_PROPERTIES:
                if max_pages and pages_scraped >= max_pages:
                    logger.info(f"Reached maximum pages limit: {max_pages}")
                    break

                scraped_count = self._scrape_page(page_number)

                if scraped_count == 0:
                    logger.warning(f"No properties scraped from page {page_number}. Stopping.")
                    break

                page_number += 1
                pages_scraped += 1

                logger.info(f"Progress: {len(self.properties)}/{PropertyFinderConfig.MAX_PROPERTIES} properties scraped")

        except KeyboardInterrupt:
            logger.info("Scraping interrupted by user")
        except Exception as e:
            logger.error(f"Unexpected error during scraping: {e}", exc_info=True)
        finally:
            self.cleanup()

        logger.info(f"Scraping completed. Total properties scraped: {len(self.properties)}")
        return self.properties

    def save_to_csv(self, filename: str = "property_data.csv"):
        """Save scraped properties to CSV file"""
        if not self.properties:
            logger.warning("No properties to save")
            return

        try:
            df = pd.DataFrame([prop.to_dict() for prop in self.properties])
            df.to_csv(filename, index=False)
            logger.info(f"Data saved to {filename} ({len(self.properties)} properties)")
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")

    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
            except Exception as e:
                logger.error(f"Error closing WebDriver: {e}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Property Finder UAE Web Scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '--chromedriver',
        type=str,
        help="Path to chromedriver executable (optional if in PATH)"
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help="Run browser in headless mode"
    )
    parser.add_argument(
        '--output',
        type=str,
        default='property_data.csv',
        help="Output CSV filename (default: property_data.csv)"
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        help="Maximum number of pages to scrape"
    )
    parser.add_argument(
        '--start-page',
        type=int,
        default=1,
        help="Page number to start from (default: 1)"
    )

    args = parser.parse_args()

    # Initialize scraper
    scraper = PropertyFinderScraper(
        chromedriver_path=args.chromedriver,
        headless=args.headless
    )

    # Start scraping
    logger.info("=" * 50)
    logger.info("Property Finder UAE Scraper Started")
    logger.info("=" * 50)

    properties = scraper.scrape(
        start_page=args.start_page,
        max_pages=args.max_pages
    )

    # Save results
    scraper.save_to_csv(args.output)

    logger.info("=" * 50)
    logger.info("Scraping Completed")
    logger.info(f"Total properties scraped: {len(properties)}")
    logger.info("=" * 50)


if __name__ == "__main__":
    main()
