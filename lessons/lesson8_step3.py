from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select

link = "http://suninjuly.github.io/selects1.html"

browser = webdriver.Chrome()
browser.get(link)

try:
    num1 = int(browser.find_element_by_css_selector("#num1").text)
    num2 = int(browser.find_element_by_css_selector("#num2").text)
    result = num1 + num2

    select = Select(browser.find_element_by_tag_name("select"))
    select.select_by_value(str(result))
    submit_button = browser.find_element_by_css_selector("[type='submit']")
    submit_button.click()

finally:
    time.sleep(5)
    browser.quit()
