from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.by import By

def get_url(country, star):
    # we fetch from booking
    base_url = "https://www.booking.com/"
    # go to search
    search_url = "searchresults.en-gb.html?"
    # query parameter for country
    country_parameter = f"ss={country}"
    # query parameter for hotel stars
    star_parameter = f"&nflt=ht_id%3D204%3Bclass%3D{star}"
    # final url
    complete_url = base_url + search_url + country_parameter + star_parameter
    return complete_url

def fetch_hotel_names(url):
    # Open browser
    driver = webdriver.Edge()
    driver.maximize_window()
    # Open the url
    driver.get(url)

    ### 1. ACCEPT COOKIES
    # Wait for the content to load
    sleep(2)
    
    # Accept the cookie consent if the specific button is found
    try:
        accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        accept_button.click()
    except NoSuchElementException:
        pass

    ### 2. Close Pop Ups (i.e. the login for 10% discount pop up)
    # Wait for the page to load fully
    sleep(3)

    # JavaScript to find elements with 'popup' or similar in class or id attributes, or fixed/absolute positioning
    identify_popups_js = """
    return Array.from(document.querySelectorAll('*')).filter(element => {
        const style = getComputedStyle(element);
        return (style.position === 'fixed' || style.position === 'absolute') &&
                (element.id.toLowerCase().includes('popup') ||
                element.className.toLowerCase().includes('popup') ||
                element.className.toLowerCase().includes('modal') ||
                element.id.toLowerCase().includes('modal')) &&
                style.display !== 'none' && style.visibility !== 'hidden';
    });
    """

    # Execute the JavaScript and get the list of identified pop-ups
    popups = driver.execute_script(identify_popups_js)

    # Close each identified pop-up if it has a close button
    for popup in popups:
        try:
            # Try to find a button within the pop-up to close it
            close_button = popup.find_element(By.XPATH, ".//button[contains(text(), 'Close') or contains(text(), 'close')]")
            close_button.click()
            print("Closed a pop-up")
        except NoSuchElementException:
            pass

    ### 3. SCROLL UNTIL ALL THE HOTELLS WILL APPEAR

    # Pause between scrolls to allow content to load
    scroll_pause_time = 1
    # Scroll increment in pixels
    scroll_increment = 1000  

    while True:
        ### 3.1. TRY TO SCROLL
        # Scroll down by a small increment
        driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_increment)
        
        # Wait for content to load
        sleep(scroll_pause_time)
        
        # Check if we are at the bottom of the page
        # new_height is the current height after scrolling
        # max_height is the max_height of the page
        new_height = driver.execute_script("return window.scrollY + window.innerHeight")
        max_height = driver.execute_script("return document.body.scrollHeight")

        ### 3.2. TRY TO LOAD MORE WITH BUTTON
        # we abstract 600 because the footer is around 800 pixels
        # that means that if we are currently on max_height - 600, we are on the
        # footer. So we will try the "Load more results" button
        if new_height >= max_height - 600:
            
            print("No more scroll")
            print("Will try to 'Load more results'")
            
            try:
                # Attempt to find and click the "Load more results" button
                load_more_button = driver.find_element(By.XPATH, "//button[.//span[text()='Load more results']]")
                load_more_button.click()
                print("Loaded!!")
                
                # Wait for new content to load
                sleep(2)
                
            except NoSuchElementException:
                # If the "Load more results" button is not found
                # Then there's no more hotels in this page
                # exit the while loop
                break
            
    ### 4. GET THE NAMES OF ALL THE HOTELS
    # Find all div elements with data-testid="title" after fully loading the page
    div_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='title']")

    names = []
    # Extract and print the inner text of each div element
    for div in div_elements:
        names.append(div.text)
    
    # Close the webdriver
    driver.quit()
    
    return names