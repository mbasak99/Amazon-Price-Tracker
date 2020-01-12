"""I wanted to create a price tracker to try to understand how some of the better applications available function
 and to get more accustomed with using libraries like BeautifulSoup and Requests"""

import requests
from bs4 import BeautifulSoup
import smtplib # Simple Mail Transfer Protocol Lib
import time

url = "https://www.amazon.ca/WH1000XM3-Wireless-Industry-Canceling-Headphones/dp/B07GP9D2Z7/ref=olp_product_details?_encoding=UTF8&me=&qid=1578807230&sr=8-3"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

# page = requests.Session()
def check_price():
    page = requests.get(url, headers=headers)

    """I needed to do the soupInit and soup because it would keep returning None without souping twice.
    Apparently this happens because of the way Amazon.ca uses JavaScript"""

    soupInit = BeautifulSoup(page.content, 'html.parser')

    soup = BeautifulSoup(soupInit.prettify(), 'html.parser')

    # Get price and title of product being tracked
    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    converted_price = float(price[5:]) # removes the 'CDN$ ' extracts only the dollar value and then converts to float

    if (converted_price < 300):
        send_email()

    # testing if application actually works
    # if (converted_price > 300):
    #     send_email()

    print(title.strip())
    print(converted_price)

def send_email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo() # Command sent by email server to id itself when connecting to another email
    server.starttls() # Encrypts connection
    server.ehlo()

    server.login('monarkb01@gmail.com', 'yrwpvnwafwqcmdfm') # Created a unique password for this app using Google App Passwords

    subject = "Product Price Lowered!"
    body = "Click the link to go to the Amazon page. Link: https://www.amazon.ca/WH1000XM3-Wireless-Industry-Canceling-Headphones/dp/B07GP9D2Z7/ref=olp_product_details?_encoding=UTF8&me=&qid=1578807230&sr=8-3"

    message = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        "monarkb01@gmail.com",
        "monarkb01@gmail.com",
        message
    )
    print("Email sent for:")

    server.quit()

while (True):
    check_price()
    time.sleep(60) # checks every minute

