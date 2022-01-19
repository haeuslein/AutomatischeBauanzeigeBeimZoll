from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, From, To, Bcc, HtmlContent, SendGridException
from datetime import date
import os
import logging

filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cron.log')
logging.basicConfig(filename=filename, format='%(asctime)s %(message)s', level=logging.DEBUG)
current_year = date.today().strftime("%Y")
today = date.today().strftime("%d.%m.%Y")

#######################################################################################
#variables in between these double comment blocks need to be peronalized by each user!#
#######################################################################################

#defining necessary variables for the email itself
sender = "sedgrid.authenticated.email@some-domain.com"     #this has to be the address you authenticated in SendGrid
recipient = "some.city@zollamt.de"                         #the address of the customs office/branch
bcc_address = "guy.incognito@some-domain.com"              #have the script send a blind copy to yourself
subject = "Brauanzeige"                                    #the subject line of the email, i. e. "Brauanzeige"

#personal info
name = "Guy Incognito"                     #your name. This will also be shown to the recipient instead of the sender email address
brewer_number = "0815"                     #Hobbybrauer-Nummer, the ID given to you by customs after you first registered with them
street = "123 Fake Street"
plz = "0815"
city = "Fake City"

#path to the SendGrid API key
api_key_path = "/home/pi/SendGrid/API-Key.txt"

#######################################################################################
#                         end of personalized variables block                         #
#######################################################################################

#defining the content of the email
content = f"""
    Darmstadt, den {today} <br><br><br>
    Sehr geehrte Damen und Herren, <br><br>
    Ich beabsichtige im Kalenderjahr {current_year}  für den Eigenbedarf an meinem Wohnsitz Bier zu brauen. Die Gesamtmenge an Vollbier wird 200 Liter nicht überschreiten. <br><br>
    Mit freundlichen Grüßen, <br>
    {name} <br><br> <br>
    Hobbybrauer-Nr. {brewer_number} <br>
    {street} <br>
    {plz} {city} <br>
"""

#importing and assigning the API key
with open(api_key_path, "r") as f:
    api_key = f.read()
    
#using the API key with the SendGrid client
sendgrid_client = SendGridAPIClient(api_key)

def sendMyEmail(sender, recipient, bcc_address, subject, content, name):
    """
    Function that calls the SendGrid API to send an email. Returns the response status code, response headers, and response body.
    str --> str
    """
    # Sendgrid client
    message = Mail(
        from_email=(sender, name),
        to_emails=recipient,
        subject=subject,
        html_content=content
    )
    #adding personalization
    message.reply_to=bcc_address
    personalization1 = Personalization()
    personalization1.add_email(To(recipient))
    personalization1.add_email(Bcc(bcc_address))
    message.add_personalization(personalization1)
     
    # Sending the email
    try:
        response = sendgrid_client.send(message)
        return response.status_code
        
    except Exception as e:
       return e        
    
# Sending the email and writing the response to the log file
re = sendMyEmail(sender, recipient, bcc_address, subject, content, name)
logging.info('Name: ' + name + ' - Recipient: ' + recipient + ' - Response: ' + str(re))
