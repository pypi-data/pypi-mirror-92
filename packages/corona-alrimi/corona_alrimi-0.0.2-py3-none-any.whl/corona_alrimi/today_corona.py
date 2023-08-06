from selenium import webdriver

from bs4 import BeautifulSoup


def today_confirm_total():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    confirm_num = soup.select_one('p.inner_value')
    print("오늘 확진 환자 수는 총 전일 대비 ", confirm_num.text, "만큼의 변화가 있었습니다.")


def today_confirm_national():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    confirm_num = soup.select('p[class*="_"]')[2]
    res = ''
    for i in confirm_num :
        res += i
    print("오늘 국내 발생 확진자 수는 ", res, "명 입니다.")


def today_confirm_oversea():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    confirm_num = soup.select('p[class*="_"]')[3]
    res = ''
    for i in confirm_num :
        res += i
    print("오늘 해외 유입 확진자 수는 ", res, "명 입니다.")


def today_release():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    checkup_num = soup.select('span[class*="_"]')[1]
    res = ''
    for i in checkup_num:
        res += i
    print("오늘 격리 해제 수는 전일 대비 ", res, "만큼의 변화가 있었습니다.")


def today_quarantine():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    quarantine = soup.select('span[class*="_"]')[2]
    res = ''
    for i in quarantine :
        res += i
    print("오늘 격리중인 사람 수는 전일 대비 ", res, "만큼의 변화가 있었습니다.")


def today_dead():
    driver = webdriver.Chrome(executable_path=r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    src = driver.page_source
    soup = BeautifulSoup(src, "html.parser")
    driver.close()

    dead = soup.select('span[class*="_"]')[3]
    res = ''
    for i in dead :
        res += i
    print("오늘 사망자 수는 전일 대비 ", res, "만큼의 변화가 있었습니다.")
