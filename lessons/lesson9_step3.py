from selenium import webdriver
import math


def calc(number):
    return str(math.log(abs(12 * math.sin(number))))


browser = webdriver.Chrome()
link = "http://suninjuly.github.io/alert_accept.html"
browser.get(link)

first_link_button = browser.find_element_by_css_selector("[type='submit']")
first_link_button.click()

alert = browser.switch_to.alert
alert.accept()

x = int(browser.find_element_by_css_selector("#input_value").text)
result = calc(x)

input_field = browser.find_element_by_css_selector("#answer")
input_field.send_keys(result)

button = browser.find_element_by_css_selector("button")

button.click()

