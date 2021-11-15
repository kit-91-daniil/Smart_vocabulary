import os
from selenium import webdriver

browser = webdriver.Chrome()

link = "http://suninjuly.github.io/file_input.html"
browser.get(link)

first = browser.find_element_by_css_selector("input[name='firstname']")
last = browser.find_element_by_css_selector("input[name='lastname']")
email = browser.find_element_by_css_selector("input[name='email']")

first.send_keys("first")
last.send_keys("last")
email.send_keys("mail")

current_dir = os.path.abspath(os.path.dirname(__file__))  # получаем путь к директории текущего исполняемого файла
file_path = os.path.join(current_dir, 'test.txt')  # добавляем к этому пути имя файла

file_input = browser.find_element_by_css_selector("#file")
file_input.send_keys(file_path)

button = browser.find_element_by_css_selector("button")
button.click()

# element.send_keys(file_path)
