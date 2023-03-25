import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

def random_delay(start=2, end=5):
    return random.uniform(start, end)

def scroll_page_up_down(driver, pause_time=1):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause_time)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(pause_time)

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView();", element)

def search_property_owner(driver, address):
    driver.get("https://portal.assessor.lacounty.gov/")
    time.sleep(random_delay())

    try:
        search_box = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.NAME, 'basicsearchterm'))
        )
    except TimeoutException:
        print(f"Couldn't find search box for address: {address}")
        return None

    search_box.send_keys(address)
    search_box.submit()
    time.sleep(random_delay())

    try:
        owner_name_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//span[contains(@class, "OwnerName")]'))
        )
        owner_name = owner_name_element.text
        return owner_name
    except TimeoutException:
        print(f"Couldn't find owner information for address: {address}")
        return None

chrome_driver_path = 'C:\\Users\\15622\\Downloads\\chromedriver_win32\\chromedriver.exe'
chrome_service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service)

url = 'https://www.trulia.com/CA/Buena_Park/'
driver.get(url)
time.sleep(random_delay())

wait = WebDriverWait(driver, 20)
property_listings = wait.until(
    EC.visibility_of_all_elements_located((By.XPATH, '//div[contains(@class, "PropertyCard__PropertyCardContainer")]'))
)

properties = []
actions = ActionChains(driver)
for listing in property_listings:
    scroll_to_element(driver, listing)
    time.sleep(random_delay())

    actions.move_to_element(listing).perform()
    time.sleep(random_delay())

    address = listing.find_element(By.XPATH, './/div[@data-testid="property-address"]').text
    price = listing.find_element(By.XPATH, './/div[@data-testid="property-price"]').text
    details_xpath = './/div[@class="FlexContainers__Columns-sc-a0824eb3-2 lehSFb"]'
    details = listing.find_element(By.XPATH, details_xpath).text.replace(' bd', 'Beds').replace(' ba', 'Baths').replace(' sqft', 'SqFt').split(' · ')

    properties.append({
        'address': address,
        'price': price,
        'details': details
    })

    scroll_page_up_down(driver)

for property in properties:
    print(f"Address: {property['address']}\nPrice: {property['price']}\nDetails: {property['details']}\n")
    owner_name = search_property_owner(driver, property['address'])
    if owner_name:
        print(f"Owner: {owner_name}\n")

driver.quit()
