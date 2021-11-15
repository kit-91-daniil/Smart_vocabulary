from selenium import webdriver
import time 

link = "http://suninjuly.github.io/registration2.html"

try:
    browser = webdriver.Chrome()
    browser.get(link)

    input1 = browser.find_element_by_css_selector(".first_block>.first_class>.first")
    input1.send_keys("Ivan")
    input2 = browser.find_element_by_css_selector(".first_block>.second_class>.second")
    input2.send_keys("Petrov")
    input3 = browser.find_element_by_css_selector(".first_block>.third_class>.third")
    input3.send_keys("qwerqwer@mail.ru")
    
    button = browser.find_element_by_class_name("btn.btn-default")
    button.click()
    time.sleep(1)
    welcome_text_elt = browser.find_element_by_tag_name("h1")
    # записываем в переменную welcome_text текст из элемента welcome_text_elt
    welcome_text = welcome_text_elt.text
    assert "Congratulations! You have successfully registered!" == welcome_text

finally:
    # ожидание чтобы визуально оценить результаты прохождения скрипта
    time.sleep(3)
    # закрываем браузер после всех манипуляций
    browser.quit()

# не забываем оставить пустую строку в конце файла