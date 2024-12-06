import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_email_smtp(sender_email, 
                    app_password, 
                    recipient_email, 
                    subject, 
                    html_body, 
                    attachment_paths):
    # Google SMTP server settings
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Create a multipart message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    # Attach the email body
    # msg.attach(MIMEText(body, "plain"))
    # Attach the HTML email body
    msg.attach(MIMEText(html_body, "html"))

    # Add the attachments
    for attachment_path in attachment_paths:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={os.path.split(attachment_path)[-1]}"
            )
            msg.attach(part)
        except Exception as e:
            print(f"Failed to attach file {attachment_path}: {e}")
            return False

    try:
        # Connect to the SMTP server and log in
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Secure the connection
        server.login(sender_email, app_password)

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        # print("Email sent successfully with attachments!")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
    finally:
        server.quit()

def send_email(hotel_emails):
    ### 0. GET THE BASIC DATA ###
    # 0.1. Important paths
    documents_path = './Data/Documents/'
    config_path = "./Data/Config/"
    already_sent_path = "./Data/Config/emails_sent.txt"
    
    # 0.2. Login Credentials and e-mail subject
    file_path = config_path + "config.json"
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        gmail_username = data['gmail_username']
        app_password = data['gmail_app_password']
        email_subject = data['email_subject']# -*- coding: utf-8 -*-
    
    # 0.3. Cover Letter
    # Open and read the file to get the email body
    cover_letter_path = config_path + 'CoverLetterHtml.txt'
    # Read the content of the file
    with open(cover_letter_path, 'r', encoding='utf-8') as f:
        email_body = f.read()
        
    # 0.4. Already sent emails
    with open(already_sent_path, 'r') as f:
        already_sent = [line.strip() for line in f]
        
    # 0.5. Check which emails to sent
    hotel_emails = [e for e in hotel_emails if e not in already_sent]
    
    if not hotel_emails:
        return True
    
    # Get a list of all files in the document directory
    documents = os.listdir(documents_path)
    # Get the absolute path of each document
    attachment_paths = [os.path.abspath(os.path.join(documents_path, file)) for file in documents]
    
    for email_to in hotel_emails:
        
        # Send the email
        is_email_sent = send_email_smtp(gmail_username, 
                                        app_password, 
                                        email_to, 
                                        email_subject, 
                                        email_body, 
                                        attachment_paths)
        
        if is_email_sent:
            # Write this email to the file
            with open(already_sent_path, 'a') as f:
                f.write(email_to + '\n')
        else:
            print('Try again tomorrow')
            return