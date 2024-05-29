from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

chrome_profile_path = '/home/wonyoung/.config/google-chrome/Default'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

url = 'https://10ff.net/'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

for i in range(4):
    input()

    input_text = driver.find_elements(By.CLASS_NAME, 'place')
    text = []
    if input_text:
        html = input_text[0].get_attribute("innerHTML")
        soup = BeautifulSoup(html, "html.parser")
        span_elements = soup.find_all("span")

        for span in span_elements:
            text.append(span.get_text()) # get text in span

    box = driver.find_element(By.XPATH, "//input")

    for t in text:
        box.send_keys(t + ' ')

driver.close()