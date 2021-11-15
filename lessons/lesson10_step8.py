import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def calc(number):
    return str(math.log(abs(12 * math.sin(number))))


browser = webdriver.Chrome()

browser.get("http://suninjuly.github.io/explicit_wait2.html")

WebDriverWait(browser, 10).until(EC.text_to_be_present_in_element((By.ID, "price"), "$100"))

book_button = browser.find_element_by_id("book")
book_button.click()

x = int(browser.find_element_by_css_selector("#input_value").text)
calc_result = calc(x)

input_field = browser.find_element_by_css_selector("#answer")
input_field.send_keys(calc_result)

button = browser.find_element_by_css_selector("#solve")
button.click()



