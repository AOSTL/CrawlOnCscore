import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from bs4 import BeautifulSoup

url = 'http://cscore.buaa.edu.cn/#/problem?ProblemId=%s&PieId=1123'
options = Options()
options.add_argument('--disable-gpu')
options.add_argument("--headless")
option = selenium.webdriver.ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(options=options)
id = "YourID"
cookie = {"name": "vuex", "value": id, "domain": "cscore.buaa.edu.cn"}
driver.get(url)
driver.add_cookie(cookie)
driver.refresh()
ST = 1
ED = 2001
LEN = ED - ST
cntFound = 0
print("Start Processing")
startTime = time.time()
with open("cscore.txt", "w", encoding="utf-8") as f:
    for i in range (ST, ED):
        driver.get(url % i)
        sleep(1)
        html=driver.page_source
        if "题目编号" in html:
            cntFound = cntFound + 1
            html.encode("utf-8")
            soup = BeautifulSoup(html, 'html.parser')
            pid = soup.find('h2', style = "display: inline-block;")
            pid = pid.text.strip()
            pType = soup.find('span', class_ = "v-chip__content")
            pType = pType.text.strip()
            pTitle = soup.find('div', class_ = "markdown-body")
            if (pTitle.find('h1') is not None) | (pTitle.find('h2') is not None):
                pTitle = "-" + pTitle.get_text().split("\n")[0]
                if len(pTitle) > 15:
                    pTitle = ""
            else:
                pTitle = ""
            title = str(i) + ": " + pid + pTitle + "(" + pType + ")"
            print(title, file=f)

        print('\r', end='')
        process = int((i - ST + 1) * 100 / LEN)
        print('[', end='');
        for j in range(1, int(process / 2)):
            print("=", end='')
        print(str(process) + "%", end='')
        for j in range(int(process / 2) + 1, 54 - len(str(process))):
            print('', end=' ')
        print('] ', end='')
        usedTime = time.time() - startTime
        etaTime = usedTime * (ED - i) / (i - ST + 1)
        print(" %*d/%d | Found %4d | ETA: %d min %02d s" % (len(str(ED - ST + 1)), i - ST + 1, ED - ST, cntFound, etaTime / 60, etaTime % 60), end='')

deltaTime = time.time() - startTime
print()
print("Process Finished, Total time: %d min %02d s" % (deltaTime / 60, deltaTime % 60))
driver.quit()
