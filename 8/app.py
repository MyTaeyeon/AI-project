from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import subprocess

cpp_program = "./main"

# open bash to run C++ program
process = subprocess.Popen(cpp_program, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# path to Chrome profile in Linux
# in Window: C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data\ProfileName
# in MacOS, its maybe located at: ~/Library/Application Support/Google/Chrome/ProfileName
chrome_profile_path = '/home/nguyen/.config/google-chrome/Default'

# create Chrome profile's option 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

# activate your chrome
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://papergames.io/vi/c%E1%BB%9D-caro")

# wait for the web loaded completely
time.sleep(3)

# click the play button
button_play_online = driver.find_element(By.XPATH, "//button[contains(text(),' Chơi với robot ')]")
button_play_online.click()

# time for you type username and click continue
time.sleep(5)

# find and click on button 'contimue'
button_continue = driver.find_element(By.XPATH, "//button[contains(text(),'Tiếp tục')]")
button_continue.click()

time.sleep(5)

game_over = False
nMask = [[0]*15 for _ in range(15)]

def getInput():
    # find all the cell
    table = driver.find_elements(By.CLASS_NAME, 'table-board')

    if table:
        for tb in table:
            html = tb.get_attribute("outerHTML")

            soup = BeautifulSoup(html, "html.parser")
            td_elements = soup.find_all("td")

            for idx, td in enumerate(td_elements):
                if len(td['class']) == 2:
                    if nMask[idx//15][idx%15] == 0:
                        return idx
    else:
        print("Không tìm thấy bảng.")
        return -2
    return -1

# sent input for cpp program
while game_over == False:
    inp = -1
    while inp == -1:
        time.sleep(2)
        inp = getInput()

    if inp == -2:
        break

    nMask[inp//15][inp%15] = 1
    inp = str(inp // 15 + 1) + " " + str(inp % 15 + 1)
    print('Input:', inp)

    process.stdin.write(inp + "\n")
    process.stdin.flush()
    output = list(map(int, process.stdout.readline().strip().split()))
    nMask[output[0]-1][output[1]-1] = 2

    print('Output: ', output)

    # AI turn
    class_att = f'cell-{output[0]-1}-{output[1]-1}'
    td_element = driver.find_element(By.CLASS_NAME, class_att)
    td_element.click()
    print('clicked!')
    time.sleep(3)

# close the stream and wait the process close
process.stdin.close()
process.stdout.close()
process.stderr.close()
process.wait()

# close the driver
driver.close()
