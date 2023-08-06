import requests
from bs4 import BeautifulSoup

def total_checkup_result():
    req = requests.get("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun=")
    soup = BeautifulSoup(req.text, "html.parser")

    #cis == Cumulative Inspection Status 누적 검사 현황
    cis = soup.find("div", class_="data_table mgt16 mini").find_all("td")
    
    total = "합계: " + str(cis[7].text)
    checkup_ing = "아직 검사중인 인원: " + str(cis[6].text)
    checkup_fin = "검사 완료 인원: " + str(cis[5].text)
    negative = "결과 음성: " + str(cis[4].text)
    confirm_total = "확진 환자 수: " + str(cis[3].text)
    quarantine = "격리중: " + str(cis[0].text)
    release = " 격리 해제: " + str(cis[1].text)
    dead = "사망: " + str(cis[2].text)
    
    result = ["누적 검사 현황", total,
              checkup_ing, checkup_fin,
              negative, confirm_total,
              quarantine, release,
              dead
            ]
    
    return result