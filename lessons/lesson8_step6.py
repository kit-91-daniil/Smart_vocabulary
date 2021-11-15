from selenium import webdriver
import math


def calc(number):
    return str(math.log(abs(12 * math.sin(number))))


browser = webdriver.Chrome()

link = "https://SunInJuly.github.io/execute_script.html"
browser.get(link)

x = int(browser.find_element_by_css_selector("#input_value").text)
result = calc(x)
print(x)
input_field = browser.find_element_by_css_selector("#answer")
input_field.send_keys(result)

button = browser.find_element_by_css_selector("button")
browser.execute_script("return arguments[0].scrollIntoView(true);", button)

input_checkbox = browser.find_element_by_css_selector("#robotCheckbox")
input_checkbox.click()

radio = browser.find_element_by_css_selector("#robotsRule")
radio.click()

button.click()

"""
Открыть страницу http://SunInJuly.github.io/execute_script.html.
Считать значение для переменной x.
Посчитать математическую функцию от x.
Проскроллить страницу вниз.
Ввести ответ в текстовое поле.
Выбрать checkbox "I'm the robot".
Переключить radiobutton "Robots rule!".
Нажать на кнопку "Submit".
"""
