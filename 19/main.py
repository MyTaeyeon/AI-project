from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import subprocess
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

chrome_profile_path = '/home/wonyoung/.config/google-chrome/Default'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

url = 'https://killersudoku.com/'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

time.sleep(6)
print("Start!")

td_elements = None  
key_pad_pointer = [0]
matrix = ""

def getInput():
    global td_elements, matrix, sum, color

    for i in range(1, 10):
        key_pad_pointer.append(driver.find_element(By.ID, f'digit-{i}'))

    td_elements = driver.find_elements(By.CLASS_NAME, 'gridCell')

    if td_elements:
        for idx, td in enumerate(td_elements):
            html = td.get_attribute("innerHTML")
            soup = BeautifulSoup(html, "html.parser")
            input_e = soup.find("input")
            if input_e:
                matrix += input_e.get("value", "") + " "
            else:
                matrix += "0 "

            span = soup.find("span")
            if span:
                matrix += span.text + " "
            else:
                matrix += "0 "

            matrix += td.get_attribute("style")[37] + " "

def click(answer):
    global td_elements, key_pad_pointer, matrix
    for td, val in zip(td_elements, answer):
        if td.get_attribute("clickable") == "1":
            td.click()
            key_pad_pointer[int(val)].click()

def solve():
    result = subprocess.run(["./19/engineer"], input=matrix, text=True, capture_output=True)

    if result.returncode == 0:
        click(result.stdout)
    else:
        print("Failed to solve the puzzle. Error:", result.stderr)

getInput()
solve()

time.sleep(10)

driver.close()