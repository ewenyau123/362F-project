from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

link = "http://127.0.0.1:2222/"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome(chrome_options=chrome_options) # to open the chromebrowser 
driver.get(link)

#login again
element = driver.find_element_by_name("client_id")
element.send_keys("10001")
time.sleep(1)
button = driver.find_element_by_id('submit')
button.click()
time.sleep(1)

#Add product into cart
element = driver.find_element_by_id("200001-no")
element.send_keys(Keys.DELETE)
element.send_keys("15")
button = driver.find_element_by_id('200001')
button.click()
time.sleep(1)

#Check the cart
button = driver.find_element_by_name('checkcart')
button.click()
time.sleep(1)

#enter the credit card detail
element = driver.find_element_by_id("credit")
element.send_keys("4111111111111111")
element = driver.find_element_by_id("cvv")
element.send_keys("123")
button = driver.find_element_by_id('checkout')
button.click()

#if the stock is not enough, it will redirect to Not enough stock message page.
time.sleep(2)
#Go To Login Page login again
button = driver.find_element_by_id("home")
button.click()
