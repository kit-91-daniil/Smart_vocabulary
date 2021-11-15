import math
import time
from selenium import webdriver

target_link = str(math.ceil(math.pow(math.pi, math.e)*10000))

browser = webdriver.Chrome()
initial_page_link = "http://suninjuly.github.io/find_link_text"
browser.get(initial_page_link)

try:
    correct_link = browser.find_element_by_link_text(target_link)
    correct_link.click()
    input1 = browser.find_element_by_name("first_name")
    input1.send_keys("Ivan")
    input2 = browser.find_element_by_name("last_name")
    input2.send_keys("Petrov")
    input3 = browser.find_element_by_class_name("city")
    input3.send_keys("Smolensk")
    input4 = browser.find_element_by_id("country")
    input4.send_keys("Russia")
    button = browser.find_element_by_css_selector("button.btn")
    button.click()

finally:
    time.sleep(10)
    browser.quit()
