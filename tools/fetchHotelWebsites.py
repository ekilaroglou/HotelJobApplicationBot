from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

# Get the first link that doesn't belong to booking or tripadvisor
def get_important_link(links):
    important_link = None
    for link in links:
        if not 'booking' in link and not 'tripadvisor' in link:
            important_link = link
            break
    return important_link

def fetch_hotel_websites(hotel_names):
    # Open browser
    driver = webdriver.Edge()
    driver.maximize_window()
    
    # Search on duckduckgo
    base_url = 'https://www.duckduckgo.com/?q='
    
    # list to put the websites
    hotel_websites = []
    for name in hotel_names:
        # create the query parameter and the url
        query_parameter = '+'.join(name.split())
        url = base_url + query_parameter
        
        # Open the url
        driver.get(url)
    
        # Wait for the page to load
        sleep(0.5)
        
        # Find all elements with data-testid="result-extras-url-link"
        nodes = driver.find_elements(By.XPATH, '//*[@data-testid="result-extras-url-link"]')
        
        # Get all the links
        links = [node.get_attribute('href') for node in nodes]
        
        website = get_important_link(links)
        if website:
            hotel_websites.append(website)
        
    # close the browser
    driver.quit()
    
    return hotel_websites