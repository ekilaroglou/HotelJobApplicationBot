import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
import multiprocessing

# Headers to mimic a real browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

# Set up Edge driver options
edge_options = EdgeOptions()
edge_options.add_argument("--headless")

def run_with_timeout(func, args=(), kwargs={}, timeout=10):
    # Create a Process to run the function
    process = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
    # Start the process
    process.start()
    # Wait for the process to finish or for the timeout
    process.join(timeout)
    
    if process.is_alive():
        print(f"{func.__name__} took too long to complete, terminating...")
        print(f"The processing url was {args[0]}")
        process.terminate()
        process.join()

def email_from_url(url, driver):  
    # Go to the page
    driver.get(url)
    
    # Extract all text content
    text = driver.page_source
    
    # Regex to match email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Find all email addresses in the text
    emails = re.findall(email_pattern, text)
    
    # Return the last one because usually the contact mail is on footer
    return emails[-1] if emails else None

def contact_page(url, driver):
    driver.get(url)
    
    # Find all links that contain 'contact' in the href attribute
    contact_page_url = None
    for link in driver.find_elements("tag name", "a"):
        href = link.get_attribute("href")
        # check if it's a path on the site
        if href and ("contact" in href.lower() or "support" in href.lower()or "contact" in link.text.lower()):
            if href.startswith('/'):
                full_url = urljoin(url, href)
                contact_page_url = full_url.lower()
                break
            elif href.startswith('http'):
                contact_page_url = href
                break
            
    return contact_page_url

def get_hotel_emails(hotel_websites):
    # open the webdriver
    driver = webdriver.Edge(options = edge_options)
    
    hotel_emails = []
    for url in hotel_websites:
        try:
            # Get email from url
            email = email_from_url(url, driver)

            # If there's not email
            if not email:
                print(f'No email found in {url}')
                # Get the contact page
                contact_page_url = contact_page(url, driver)

                # If there's contact page
                if contact_page_url:
                    # Get the email from the contact page
                    email = email_from_url(contact_page_url, driver)

                    if not email:
                        print(f' No email found in {contact_page_url}')
            
            # if we have email from url or from contact_page_url
            # append it to the email list
            if email:
                hotel_emails.append(email)
                print(f'Email fetched from: {url}')
        except:
            continue
        
    # close the web driver
    driver.quit()
    
    return hotel_emails
        
