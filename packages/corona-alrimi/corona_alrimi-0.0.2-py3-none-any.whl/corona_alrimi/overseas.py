from selenium import webdriver
from bs4 import BeautifulSoup
import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

def overseas_total():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    inflow = soup.find("td", colspan="2").text
    return inflow

def overseas_total_new():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    new = soup.find("td").text
    return new

def overseas_china():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    china = soup.select("tr td")
    print("중국 유입 신규 확진자:", china[2].text)
    print("중국 유입 누적 확진자:", china[3].text)

def overseas_asia():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    asia = soup.select("tr td")
    print("중국외아시아 유입 신규 확진자:", asia[5].text)
    print("중국외아시아 유입 누적 확진자:", asia[6].text)

def overseas_europe():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    europe = soup.select("tr td")
    print("유럽 유입 신규 확진자:", europe[8].text)
    print("유럽 유입 누적 확진자:", europe[9].text)

def overseas_america():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    america = soup.select("tr td")
    print("미주 유입 신규 확진자:", america[11].text)
    print("미주 유입 누적 확진자:", america[12].text)

def overseas_africa():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    africa = soup.select("tr td")
    print("미주 유입 신규 확진자:", africa[14].text)
    print("미주 유입 누적 확진자:", africa[15].text)

def overseas_australia():
    driver = webdriver.Chrome(r'.\chromedriver.exe')
    url = 'http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun='
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    australia = soup.select("tr td")
    print("미주 유입 신규 확진자:", australia[17].text)
    print("미주 유입 누적 확진자:", australia[18].text)