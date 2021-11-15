from selenium import webdriver
import time
import math


def calc(number):
    return str(math.log(abs(12 * math.sin(int(number)))))


link = "http://suninjuly.github.io/math.html"

browser = webdriver.Chrome()
browser.get(link)

try:
    x = browser.find_element_by_css_selector("#input_value")
    calc_result = calc(x.text)
    text_field = browser.find_element_by_css_selector("#answer")
    text_field.send_keys(calc_result)
    the_robot_ack = browser.find_element_by_css_selector("#robotCheckbox")
    the_robot_ack.click()
    robots_rule_radio = browser.find_element_by_css_selector("#robotsRule")
    robots_rule_radio.click()
    submit_button = browser.find_element_by_css_selector("[type='submit']")
    submit_button.click()

finally:
    time.sleep(10)
    browser.quit()
