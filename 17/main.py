from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
from strategy import strategies

chrome_profile_path = '/home/wonyoung/.config/google-chrome/Default'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")

url = 'https://gamevui.vn/pikachu/game'
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)

frame = driver.find_element(By.XPATH, '//iframe[@id="giframe"]')
driver.switch_to.frame(frame)

def click(element):
    action = ActionChains(driver)
    action.move_to_element(element).click().perform()

size = (width, height) = (16, 9)
directions = (up, right, down, left) = ((-1, 0), (0, 1), (1, 0), (0, -1))
key = -1
maxdepth = 3
matrix = None
cards = None

print('Start?[y/n]')
n = input().strip()

def init():
    global matrix
    matrix = [[-1]*(width+4)] \
            + [[-1]+ [0]*(width+2) + [-1]] \
            + [[-1, 0] + [1] * width + [0, -1] for _ in range(height)] \
            + [[-1] + [0]*(width+2) + [-1]] \
            + [[-1]*(width+4)]

def getInput():
    global matrix, driver, cards

    cards = driver.find_elements(By.XPATH, '//td[@id="board"]/div//div')
    cards = cards[3:]

    for idx, card in enumerate(cards):
        if matrix[idx%height+2][idx//height+2] > 0:
            html_content = card.get_attribute('innerHTML')
            end = html_content.index('.png')
            matrix[idx%height+2][idx//height+2] = int(html_content[34:end])

def dfs(target, i, j, curr_dir, depth):
    global key
    if depth > maxdepth:
        return 0
    else:
        if matrix[i][j] == -1:
            return 0
        elif matrix[i][j] == 0:
            pass
        elif matrix[i][j] != target:
            return 0
        else:
            key = [i, j]
            return 1
        
        res = dfs(target, i+directions[curr_dir][0], j+directions[curr_dir][1], curr_dir, depth)
        if res: return res
        res = res | dfs(target, i+directions[curr_dir-1][0], j+directions[curr_dir-1][1], directions.index(directions[curr_dir-1]), depth+1)
        if res: return res
        res = res | dfs(target, i+directions[curr_dir-3][0], j+directions[curr_dir-3][1], directions.index(directions[curr_dir-3]), depth+1)
        return res
    
def falling(pos, level):
    if level == 0:
        return None
    elif level == 1:
        l = []
        for i in range(pos[0], 1, -1):
            if matrix[i][pos[1]] > 0:
                l.append(matrix[i][pos[1]])
            matrix[i][pos[1]] = 0
        for i in range(len(l)):
            matrix[pos[0]-i][pos[1]] = l[i]
        return None
    elif level == 2:
        l = []
        for i in range(2, height+2):
            if matrix[i][pos[1]] > 0:
                l.append(matrix[i][pos[1]])
            matrix[i][pos[1]] = 0
        for i in range(len(l)):
            matrix[i+2][pos[1]] = l[i]
        return None
    elif level == 3:
        l = []
        for i in range(2, width+2):
            if matrix[pos[0]][i] > 0:
                l.append(matrix[pos[0]][i])        
            matrix[pos[0]][i] = 0  
        for i in range(len(l)):
            matrix[pos[0]][i+2] = l[i]
        return None
    elif level == 4:
        l = []
        for i in range(width+1, 1, -1):
            if matrix[pos[0]][i] > 0:
                l.append(matrix[pos[0]][i])
            matrix[pos[0]][i] = 0
        for i in range(len(l)):
            matrix[pos[0]][width+1-i] = l[i]
        return None
    elif level == 5:
        if pos[0] > 5:
            l = []
            for i in range(height+1, 5, -1):
                if matrix[i][pos[1]] > 0:
                    l.append(matrix[i][pos[1]])
                matrix[i][pos[1]] = 0
            for i in range(len(l)):
                matrix[height+1-i][pos[1]] = l[i]
        else:
            l = []
            for i in range(2, 6):
                if matrix[i][pos[1]] > 0:
                    l.append(matrix[i][pos[1]])
                matrix[i][pos[1]] = 0
            for i in range(len(l)):
                matrix[2+i][pos[1]] = l[i]
    elif level == 6:
        a = []
        for i in range(4, 1, -1):
            if matrix[i][pos[1]] > 0:
                a.append(matrix[i][pos[1]])
            matrix[i][pos[1]] = 0

        b = []
        for i in range(5, height+2):
            if matrix[i][pos[1]] > 0:
                b.append(matrix[i][pos[1]])
            matrix[i][pos[1]] = 0
        
        if len(a) == 0:
            if len(b) == 0:
                pass
            elif len(b) == 1:
                matrix[6][pos[1]] = b[0]
                return None

        for i in range(len(a)):
            matrix[4-i][pos[1]] = a[i]
        for i in range(len(b)):
            matrix[5+i][pos[1]] = b[i]  

    else:
        return None
    
def solve(level):
    global matrix, directions, cards
    remain = width * height
    getInput()
    while remain > 0:
        l = remain
        restart = False
        for row, column in strategies[level%5]: 
            if restart == True: break
            if matrix[row][column] > 0:
                for dir in range(4):
                    res = dfs(matrix[row][column], row+directions[dir][0], column+directions[dir][1], dir, 1)
                    if res:
                        remain -= 2
                        click(cards[(column-2)*height+row-2])
                        click(cards[(key[1]-2)*height+key[0]-2])
                        matrix[row][column] = 0
                        matrix[key[0]][key[1]] = 0
                        
                        falling(key, level)
                        falling([row, column], level)

                        if abs(key[0]-row) + abs(key[1]-column) == 1: restart = True
                        break
        
        if l == remain: 
            print("there's no pair!!!")
            time.sleep(3)

            alert = driver.switch_to.alert
            alert.accept()

            getInput()

for i in range(7):
    init()
    solve(i)
    print(f"Level {i+1} is completed!")
    time.sleep(3)

input('>>> ')

driver.quit()
