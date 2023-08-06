from bs4 import BeautifulSoup
from selenium import webdriver


def corona_by_gender():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    confirm = soup.select("td span")

    confirm_man = soup.select("td span")[0]
    print('남성 확진자:', confirm_man.text)
    print('남성 사망자:', confirm[2].text)

    confirm_woman = soup.select("td span")[5]
    print('여성 확진자:', confirm_woman.text)
    print('여성 사망자:', confirm[7].text)


def corona_by_age(age):
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()
    confirm = soup.select("td span")

    if age >= 80:
        confirm_age = confirm[10]
        dead_age = confirm[12]
        print('80세 이상 확진자:', confirm_age.text)
        print('80세 이상 사망자:', dead_age.text)
    elif age >= 70:
        confirm_age = confirm[15]
        dead_age = confirm[17]
        print('70 ~ 79 확진자:', confirm_age.text)
        print('70 ~ 79 사망자:', dead_age.text)
    elif age >= 60:
        confirm_age = confirm[20]
        dead_age = confirm[22]
        print('60 ~ 69 확진자:', confirm_age.text)
        print('60 ~ 69 사망자:', dead_age.text)
    elif age >= 50:
        confirm_age = confirm[25]
        dead_age = confirm[27]
        print('50 ~ 59 확진자:', confirm_age.text)
        print('50 ~ 59 사망자:', dead_age.text)
    elif age >= 40:
        confirm_age = confirm[30]
        dead_age = confirm[32]
        print('40 ~ 49 확진자:', confirm_age.text)
        print('40 ~ 49 사망자:', dead_age.text)
    elif age >= 30:
        confirm_age = confirm[35]
        dead_age = confirm[37]
        print('30 ~ 39 확진자:', confirm_age.text)
        print('30 ~ 39 사망자:', dead_age.text)
    elif age >= 20:
        confirm_age = confirm[40]
        dead_age = confirm[42]
        print('20 ~ 29 확진자:', confirm_age.text)
        print('20 ~ 29 사망자:', dead_age.text)
    elif age >= 10:
        confirm_age = confirm[45]
        dead_age = confirm[47]
        print('10 ~ 19 확진자:', confirm_age.text)
        print('10 ~ 19 사망자:', dead_age.text)
    elif age >= 0:
        confirm_age = confirm[50]
        dead_age = confirm[52]
        print('0 ~ 9 확진자:', confirm_age.text)
        print('0 ~ 9 사망자:', dead_age.text)
