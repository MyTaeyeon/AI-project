from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import subprocess

# path to Chrome profile in Linux
# in Window: C:\Users\YourUsername\AppData\Local\Google\Chrome\User Data\ProfileName
# in MacOS, its maybe located at: ~/Library/Application Support/Google/Chrome/ProfileName
chrome_profile_path = '/home/nguyen/.config/google-chrome/Default'

# create Chrome profile's option 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

# activate your chrome
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://papergames.io/en/gomoku") 

while True:
    cpp_program = "./main"

    # open bash to run C++ program
    process = subprocess.Popen(cpp_program, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    game_over = False
    lastMove = -1

    def getInput():
        # find all the cell
        table = driver.find_elements(By.CLASS_NAME, 'table-board')

        if table:
            for tb in table:
                html = tb.get_attribute("outerHTML")

                soup = BeautifulSoup(html, "html.parser")
                td_elements = soup.find_all("td")

                for idx, td in enumerate(td_elements):
                    if idx == lastMove: continue
                    if len(td['class']) == 2:    
                        svg_tags = td.find_all('svg') 
                        if len(svg_tags) == 1:
                            
                            circle_tags = svg_tags[0].find_all('circle') 
                            
                            if len(circle_tags) == 2:
                                return idx
        else:
            print("Không tìm thấy bảng.")
            return -2
        return -1

    n = input('com play first?[y/n]').strip()
    if n == 'y':
        process.stdin.write("2\n")
        process.stdin.flush()
        output = list(map(int, process.stdout.readline().strip().split()))

        class_att = f'cell-{output[0]-1}-{output[1]-1}'
        td_element = driver.find_element(By.CLASS_NAME, class_att)
        td_element.click()
        lastMove = (output[0]-1)*15+output[1]-1
        print('clicked!')
    else:
        process.stdin.write("1\n")

    # sent input for cpp program
    while game_over == False:
        inp = -1
        while inp == -1:
            time.sleep(3)
            inp = getInput()

        if inp == -2:
            break

        inp = str(inp // 15 + 1) + " " + str(inp % 15 + 1)
        print('Input:', inp)

        process.stdin.write(inp + "\n")
        process.stdin.flush()
        output = list(map(int, process.stdout.readline().strip().split()))

        print('Output: ', output)

        # AI turn
        class_att = f'cell-{output[0]-1}-{output[1]-1}'
        td_element = driver.find_element(By.CLASS_NAME, class_att)
        td_element.click()
        lastMove = (output[0]-1)*15+output[1]-1
        print('clicked!')

    # close the stream and wait the process close
    process.stdin.close()
    process.stdout.close()
    process.stderr.close()
    process.wait()

    g = input('press q to exit.').strip()
    if g == 'q': break

# close the driver
driver.close()
