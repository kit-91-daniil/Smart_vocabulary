from selenium import webdriver
import time

browser = webdriver.Chrome()

try:
    link = "http://suninjuly.github.io/registration1.html"
    new_link = "http://suninjuly.github.io/registration2.html"
    # browser.get(link)
    browser.get(new_link)

    input1 = browser.find_element_by_css_selector(".first_block input.first")
    input1.send_keys("Ivan")
    input2 = browser.find_element_by_css_selector(".first_block input.second")
    input2.send_keys("Petrov")
    input3 = browser.find_element_by_css_selector(".first_block input.third")
    input3.send_keys("my_mail@mail.ru")
    input4 = browser.find_element_by_css_selector(".second_block input.first")
    input4.send_keys("my_number")
    input5 = browser.find_element_by_css_selector(".second_block input.second")
    input5.send_keys("my_address")
    button = browser.find_element_by_css_selector("button.btn")
    button.click()

    time.sleep(1)

    welcome_text_elt = browser.find_element_by_tag_name("h1")
    welcome_text = welcome_text_elt.text

    assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    time.sleep(10)
    browser.quit()
