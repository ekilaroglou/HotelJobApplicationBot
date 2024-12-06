import os
import json
from time import time
import itertools
from tools.fetchHotelNames import get_url, fetch_hotel_names
from tools.fetchHotelEmails import get_hotel_emails
from tools.fetchHotelWebsites import fetch_hotel_websites

config_path = "./Data/Config/"
hotel_names_path = "./Data/HotelNames/"
hotel_emails_path = "./Data/HotelEmails/"
hotel_websites_path = "./Data/HotelWebsites/"
hotel_done_processing_path = "./Data/HotelDoneProcessing/"

### 1. GET THE BASIC DATA
# Get countries that we want to apply
file_path = config_path + "Countries.txt"
with open(file_path, 'r') as f:
    countries = [line.strip() for line in f]

# Get stars of hotels that we want to apply
# i.e. if value is [3,4,5] then we get the 3* hotels, 4* hotels and 5* hotels
file_path = config_path + "config.json"
with open(file_path, 'r') as json_file:
    data = json.load(json_file)
    hotel_stars = data['hotel_stars']
    override_hotel_names = False if 'false' in data['override_hotel_names'].lower() else True
    override_hotel_websites = False if 'false' in data['override_hotel_websites'].lower() else True
    override_hotel_emails = False if 'false' in data['override_hotel_emails'].lower() else True
    email_method = data.get('email_method', 'smtp')  # Default to 'smtp' if not specified

# Conditionally import the appropriate send_email function
if email_method == 'smtp':
    from tools.send_email_smtp import send_email
else:
    from tools.send_email import send_email

### 2. GET THE HOTEL NAMES
# The reason that we get a different url for each star and we don't combine all
# together is because we can not get more than 1000 hotels in a single page
# is because the
# For each country and hotel star
# Fetch the hotel names
for country, star in itertools.product(countries, hotel_stars):
    hotel_name_file = f'{country}_{star}_stars.txt'
    file_path = hotel_names_path + hotel_name_file
    # If we don't have the file or if we want to override
    if not os.path.exists(file_path) or override_hotel_names:
        url = get_url(country, star)
        hotel_names = fetch_hotel_names(url)
        # Writing the list to the file
        with open(file_path, 'w') as f:
            for name in hotel_names:
                f.write(f"{name}\n")

### 3. GET THE HOTEL WEBSITES
for country, star in itertools.product(countries, hotel_stars):
    hotel_website_file = f'w_{country}_{star}_stars.txt'
    file_path = hotel_websites_path + hotel_website_file
    # If we don't have the file or if we want to override
    if not os.path.exists(file_path) or override_hotel_websites:
        # Get the hotel names
        hotel_name_file = f'{country}_{star}_stars.txt'
        hotel_name_path = hotel_names_path + hotel_name_file
        # Reading the list from the file
        with open(hotel_name_path, 'r') as f:
            hotel_names = [line.strip() for line in f]
        # Get the websites based on the names
        hotel_websites = fetch_hotel_websites(hotel_names)
        # Writing the list to the file
        with open(file_path, 'w') as f:
            for website in hotel_websites:
                f.write(f"{website}\n")

### 4. GET THE HOTEL EMAILS
for country, star in itertools.product(countries, hotel_stars):
    hotel_email_file = f'e_{country}_{star}_stars.txt'
    file_path = hotel_emails_path + hotel_email_file
    # If we don't have the file or if we want to override
    if not os.path.exists(file_path) or override_hotel_emails:
        # Get the hotel names
        hotel_website_file = f'w_{country}_{star}_stars.txt'
        hotel_website_path = hotel_websites_path + hotel_website_file
        # Reading the list from the file
        with open(hotel_website_path, 'r') as f:
            hotel_websites = [line.strip() for line in f]
         
        # Get the emails based on the names
        hotel_emails = get_hotel_emails(hotel_websites)
        # Writing the list to the file
        with open(file_path, 'w') as f:
            for email in hotel_emails:
                f.write(f"{email}\n")


## 5. SEND EMAILS
# for country, star in itertools.product(countries, hotel_stars):
#     hotel_done_processing_file = f'done_{country}_{star}_stars.txt'
#     file_path = hotel_done_processing_path + hotel_done_processing_file
#     # If we don't have the file then we send the emails
#     if not os.path.exists(file_path):
#         # Get the hotel emails
#         hotel_email_file = f'e_{country}_{star}_stars.txt'
#         hotel_email_path = hotel_emails_path + hotel_email_file

#         # Reading the list from the file
#         with open(hotel_email_path, 'r') as f:
#             hotel_emails= [line.strip() for line in f]
        
#         t0 = time()
#         # Send the emails
#         emails_was_sent = send_email(hotel_emails)
#         dt = time() - t0
#         print(f'Send {len(hotel_emails)} emails in {int(dt)} seconds.')
        
#         # If all was sent successfully only then write the file
#         if emails_was_sent:
#             with open(file_path, 'w') as f:
#                 f.write("Done processing all the emails\n")

# 0.4. Already sent emails
already_sent_path = "./Data/Config/emails_sent.txt"
# currently 2033 rows

counter = 0
max_value = 500

for country, star in itertools.product(countries, hotel_stars):
    hotel_done_processing_file = f'done_{country}_{star}_stars.txt'
    file_path = hotel_done_processing_path + hotel_done_processing_file
    # If we don't have the file then we send the emails
    if not os.path.exists(file_path):
        # Get the hotel emails
        hotel_email_file = f'e_{country}_{star}_stars.txt'
        hotel_email_path = hotel_emails_path + hotel_email_file

        # Reading the list from the file
        with open(hotel_email_path, 'r') as f:
            hotel_emails= [line.strip() for line in f]
        
        with open(already_sent_path, 'r') as f:
            already_sent = [line.strip() for line in f]
        hotel_emails = [e for e in hotel_emails if e not in already_sent]
        
        if counter + len(hotel_emails) > max_value:
            n_send = max_value - counter
            hotel_emails = hotel_emails[:n_send]
        
        
        t0 = time()
        # Send the emails
        emails_was_sent = send_email(hotel_emails)
        dt = time() - t0
        print(f'Send {len(hotel_emails)} emails in {int(dt)} seconds.')
        
        # If all was sent successfully only then write the file
        if emails_was_sent:
            with open(file_path, 'w') as f:
                f.write("Done processing all the emails\n")
                
        counter += len(hotel_emails)
        
        if counter >= max_value:
            break
        
        
