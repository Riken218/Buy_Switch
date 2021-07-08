from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import smtplib
import datetime
import time
# Run following line in command line. "-u" is to unbuffer outputs to update
# txt file in real time.
# python3.7 -u /home/richarjr/programs/add_switch_to_cart.py > /home/richarjr/switch_running_time.txt &

# Find & Replace "your.email@outlook.com" and "Password" 
# with your Outlook email address and Amazon password respectively.

def try_buy_and_email():
  try:
    driver.find_elements_by_class_name('hlb-checkout-button')[0].click()
    try:
      driver.find_element_by_id('ap_password').send_keys('Password')
      driver.find_element_by_id('auth-signin-button').click()
    except:
      None      
    driver.find_elements_by_class_name('place-order-button-text')[0].click()
    bought = True
  except:
    body = 'Subject: Switch from Amazon\n\n\n' + 'Switch Sold Out Before Puchase was Complete.'
    bought = False
    try: 
        smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587) 
    except Exception as e: 
        print(e) 
        smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465) 
    smtpObj.ehlo() 
    smtpObj.starttls() 
    smtpObj.login('your.email@mail.com', "Password")  
    smtpObj.sendmail('your.email@mail.com', 'your.email@mail.com', body) 
    smtpObj.quit()
    return bought
  # Email Me When Added to Cart
  body = 'Subject: Switch from Amazon\n\n\n' + 'Switch has been Purchased.' 
  try: 
      smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587) 
  except Exception as e: 
      print(e) 
      smtpObj = smtplib.SMTP_SSL('smtp-mail.outlook.com', 465) 
  smtpObj.ehlo() 
  smtpObj.starttls() 
  smtpObj.login('your.email@mail.com', "Password")  
  smtpObj.sendmail('your.email@mail.com', 'your.email@mail.com', body) 
  smtpObj.quit()
  return bought


def find_switch_amazon():
  driver = webdriver.Chrome() 
  driver.get('https://www.amazon.com/gp/offer-listing/B07VGRJDFY/ref=olp_f_new?ie=UTF8&f_new=true')
  # Sign into Amazon
  driver.find_elements_by_class_name('nav-action-button')[1].click()
  driver.find_element_by_id('ap_email').send_keys('your.email@mail.com')
  driver.find_element_by_id('continue').click()
  driver.find_element_by_id('ap_password').send_keys('Password')
  driver.find_element_by_id('auth-signin-button').click()
  # Find and Compare Prices and Seller Ratings
  price_init = float(driver.find_element_by_class_name('a-color-price').text[1:])
  print(str(datetime.datetime.today()))
  #print(price_init,type(price_init)) 
  added_to_cart=False 
  start_time=time.time()
  price_init=1500.0
  earliest_in_list = 0
  switch_on_page = -1
  # Repeat Until Requirements met
  while not added_to_cart:
    for i in range(10):
      try:
        price = float(driver.find_elements_by_class_name('a-color-price')[i].text[1:])
      except:
        continue
      if price < 300.0:
        button = driver.find_elements_by_class_name('a-button-input')[i]
        button.click()
        print('MSRP Switch Added to Cart')
        added_to_cart=True
        break
      try:
        rating_str = driver.find_elements_by_tag_name('p')[4*i+3].get_attribute('textContent').replace(' ','').replace('\n','')
        rating = float(rating_str[:rating_str.find('outof5stars')])
        total_ratings_str = driver.find_elements_by_tag_name('p')[4*i+3].get_attribute('textContent').replace(' total ratings)','').replace(' ','').replace(',','')
        total_ratings = float(total_ratings_str[total_ratings_str.find('(')+1:])
      except:
        #print('rating get not working')
        continue
      if rating < 4.5 or total_ratings < 20:
        continue
      #if (price < 340.0 and rating >= 4.0):
      elif price < 340.0:
        button = driver.find_elements_by_class_name('a-button-input')[i]
        button.click() 
        print('Price Gauged Switch Added to Cart')
        added_to_cart=True 
        break
      else:
        lowest_price = price
        switch_on_page
        if lowest_price != price_init or switch_on_page != i:
          price_init = lowest_price
          switch_on_page = i
          print('Looking at the {} down on the page'.format(i+1))
          print('Lowest price on page with decent rating: {:.2f}'.format(price))
        if (time.time()-start_time)%(60*10) <= 15 and time.time()-start_time > 15:
          print('It\'s been {:.2f} hours\nTime: {}'.format((time.time()-start_time)/3600,str(datetime.datetime.today())))
        time.sleep(10) 
        driver.refresh()
        break
  # Purchasing now
  return try_buy_and_email()

errors = False
timeouts = 0
#find_switch_amazon()
#print('Out of while loop')
while not errors:
#  print('In while loop')
  try:
    print('Timeouts so far: {}'.format(timeouts))
    bought = find_switch_amazon()
    if not bought:
      errors = False
      time.sleep(60*5)
    else:
      errors = True
  except:
    timeouts += 1
    print('Error occurred')

