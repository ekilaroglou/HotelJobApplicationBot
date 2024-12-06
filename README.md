# Hotel Email Automation Pipeline

This project automates the process of sending job applications to hotels by searching for their names, websites, and email addresses, then sending an email through SMTP or ProtonMail based on the configuration.

## Project Pipeline

1. **Search hotel names**: The project searches for hotel names on Booking.com.
2. **Search hotel websites**: Once hotel names are retrieved, the project searches for their websites using DuckDuckGo.
3. **Search hotel email**: The project scrapes the email addresses from the hotel websites.
4. **Send email**: The project sends an email either through SMTP (using Gmail) or ProtonMail, depending on the configuration.

## File Structure

- `Data/Config/Countries.txt`: Contains the countries to search, separated by a new line.
- `Data/Config/CoverLetter.txt`: Contains the cover letter for the email. HTML styling can be added in this file.
- `Data/Config/emails_sent.txt`: Contains the list of email addresses where emails have already been sent. If you want to exclude certain emails, add them here.
- `Data/Documents`: Contains the attachments for the email, such as your CV or other documents.
- `Data/Config/config.json`: The configuration file that defines various settings for the project (see below for details).

## Configuration (`config.json`)

The `config.json` file is where all the project settings are defined. Here is an example of the structure:

```json
{
	"hotel_stars": [3, 4, 5],
	"override_hotel_names": "False",
	"override_hotel_websites": "False",
	"override_hotel_emails": "False",
	"protonmail_username": "Your ProtonMail Username",
	"protonmail_password": "Your ProtonMail Password",
	"gmail_username": "Your Gmail",
	"gmail_app_password": "Your Gmail app Password",
	"email_subject": "Job Application",
	"email_method": "smtp"
}
```

### Configuration Fields

- **hotel_stars**: A list of hotel star ratings (e.g., [3, 4, 5]) to filter which hotels to search.
- **override_hotel_names**: Set to `"True"` to override the existing hotel names in the data or `"False"` to not override.
- **override_hotel_websites**: Set to `"True"` to override the existing hotel websites or `"False"` to not override.
- **override_hotel_emails**: Set to `"True"` to override the existing hotel emails or `"False"` to not override.
- **protonmail_username**: Your ProtonMail username (only required if using ProtonMail).
- **protonmail_password**: Your ProtonMail password (only required if using ProtonMail).
- **gmail_username**: Your Gmail address (only required if using Gmail-smtp).
- **gmail_app_password**: Your Gmail app password (only required if using Gmail-smtp).
- **email_subject**: The subject line of the email.
- **email_method**: The method used to send the email. Can be either `"smtp"` (for Gmail) or `"protonmail"`.

### Email Method Configuration

- **If `email_method` is set to `smtp`**:
  - The program will use Gmail's SMTP server to send the email.
  - **Required fields**: `gmail_username` and `gmail_app_password`.
  - **ProtonMail credentials are not needed**.

- **If `email_method` is set to `protonmail`**:
  - The program will use ProtonMail's SMTP server to send the email.
  - **Required fields**: `protonmail_username` and `protonmail_password`.
  - **Gmail credentials are not needed**.

## How to Run the Project

1. **Install dependencies**: Ensure you have the necessary dependencies installed:
    ```bash
    pip install -r requirements.txt
    ```

2. **Update configuration**: Edit the `config.json` file with your personal information, including Gmail or ProtonMail credentials.

3. **Prepare data files**:
   - Make sure the `Countries.txt` file lists the countries you want to search.
   - Write your cover letter in `CoverLetter.txt`. You can include HTML styling if desired.
   - Add any email addresses you want to exclude from the `emails_sent.txt` file.
   - Place any documents (e.g., your CV) in the `Data/Documents` folder.

4. **Run the pipeline**:
   ```bash
   python main.py
   ```
   This will start the pipeline, which will search for hotel names, websites, email addresses, and then send the email with the specified attachments.

## Notes

- The project uses web scraping to gather hotel information, so make sure the relevant websites (Booking, DuckDuckGo, and the hotel websites) are accessible at the time of running.
- Be cautious with the use of email credentials. Consider using environment variables or secret management tools to store sensitive information securely.
- If using ProtonMail ensure you have the correct WebDriver installed for your browser.
