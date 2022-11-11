import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from urllib import request
import json
import time
from datetime import date
from datetime import datetime
from bs4 import BeautifulSoup

racingno=6
firsttime = True
sleeptime = 3

winplaurl='https://bet.hkjc.com/racing/getJSON.aspx?type=winplaodds&date=2020-05-06&venue=HV'
qinurl='https://bet.hkjc.com/racing/pages/odds_wpq.aspx?lang=ch&date=2020-05-06&venue=HV&raceno='
qplurl='https://bet.hkjc.com/racing/getJSON.aspx?type=qpl&date=2020-05-06&venue=HV&raceno='
dblurl='https://bet.hkjc.com/racing/getJSON.aspx?type=dbl&date=2020-05-06&venue=HV&raceno='
pooltoturl='https://bet.hkjc.com/racing/getJSON.aspx?type=pooltot&date=2020-05-06&venue=HV&raceno='

winpla = winplaurl + '&start=' + str(racingno) + '&end=' + str(racingno)
qin = qinurl + str(racingno)
qpl = qplurl + str(racingno)
dbl = dblurl + str(racingno)
pooltot = pooltoturl + str(racingno)


scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json",scope)
client = gspread.authorize(creds)

ss=[]
for m in range(11):
    ss.append((racingno-1)*4+m)
    
if (firsttime):
    winpageurl='https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=ch&date=2020-05-06&venue=HV&raceno=' + str(racingno)
    driver = webdriver.Chrome()
    driver.get(winpageurl)
    tables = driver.find_element_by_id("detailWPTable")
    horseno=[] #1
    horsename=[] #3
    draw=[] #4
    weight=[] #5
    jocky=[] #6
    trainer=[] #7
    for i in range(1,16):
        temp='//*[@id="detailWPTable"]/table/tbody/tr['+str(i)
        horseno.append(driver.find_element_by_xpath(temp+']/td[1]').text)
        horsename.append(driver.find_element_by_xpath(temp+']/td[3]').text)
        draw.append(driver.find_element_by_xpath(temp+']/td[4]').text)
        weight.append(driver.find_element_by_xpath(temp+']/td[5]').text)
        jocky.append(driver.find_element_by_xpath(temp+']/td[6]').text)
        trainer.append(driver.find_element_by_xpath(temp+']/td[7]').text)
    detailWPTablesheet = client.open("storage").get_worksheet(ss[10])
    detailWPTableinsert=[]
    for i in range(len(horseno)-1,-1,-1):
        temp=[]
        temp.append(horseno[i])
        temp.append(horsename[i])
        temp.append(draw[i])
        temp.append(weight[i])
        temp.append(jocky[i])
        temp.append(trainer[i])
        detailWPTablesheet.insert_row(temp,1)
    
winbetsheet = client.open("storage").get_worksheet(ss[0])
plabetsheet = client.open("storage").get_worksheet(ss[1])
qinbetsheet = client.open("storage").get_worksheet(ss[2])
qplbetsheet = client.open("storage").get_worksheet(ss[3])
dblbetsheet = client.open("storage").get_worksheet(ss[4])
winoddsheet = client.open("storage").get_worksheet(ss[5])
plaoddsheet = client.open("storage").get_worksheet(ss[6])
qinoddsheet = client.open("storage").get_worksheet(ss[7])
qploddsheet = client.open("storage").get_worksheet(ss[8])
dbloddsheet = client.open("storage").get_worksheet(ss[9])

done = 0
error = 1
while (error < 40 and done<1):
    try:
        now1 = datetime.now()
        now = now1.strftime("%H:%M:%S.%f")[:-2]

        winplaData1 = request.urlopen(winpla).read()
        qinData1 = request.urlopen(qin).read()
        qplData1 = request.urlopen(qpl).read()
        dblData1 = request.urlopen(dbl).read()
        pooltotData1 = request.urlopen(pooltot).read()

        winplaData = json.loads(winplaData1)
        qinData = json.loads(qinData1)
        qplData = json.loads(qplData1)
        dblData = json.loads(dblData1)
        pooltotData = json.loads(pooltotData1)

        winbet1 = winplaData['OUT'].split("#")
        winbet2 = winbet1[0].split(";") #win odd
        winbet3 = winbet1[1].split(";") #place odd
        wincomb = []
        winbet = []
        plabet = []
        for i in range(len(winbet2)):
            temp=winbet2[i].split("=")
            if (i==0):
                continue
            if (temp[1]=="SCR"):
                wincomb.append(temp[0])
                winbet.append(999)
                continue
            wincomb.append(temp[0])
            winbet.append(temp[1])
        for i in range(len(winbet3)):
            temp=winbet2[i].split("=")
            if (i==0):
                continue
            if (temp[1]=="SCR"):
                plabet.append(999)
                continue
            plabet.append(temp[1])



        qinbet1 = qinData['OUT'].split(";")
        qincomb = []
        qinbet = []



        for i in range(len(qinbet1)):
            temp=qinbet1[i].split("=")
            if (i==0):
                continue
            if (temp[1]=="SCR"):
                qincomb.append(temp[0])
                qinbet.append(999)
                continue
            qincomb.append(temp[0])
            qinbet.append(temp[1])


        qplbet1 = qplData['OUT'].split(";")
        qplcomb = []
        qplbet = []

        for i in range(len(qplbet1)):
            temp=qplbet1[i].split("=")
            if (i==0):
                continue
            if (temp[1]=="SCR"):
                qplcomb.append(temp[0])
                qplbet.append(999)
                continue
            qplcomb.append(temp[0])
            qplbet.append(temp[1])

        wintot = float(pooltotData["inv"][0]["value"])
        platot = float(pooltotData["inv"][1]["value"])
        qintot = float(pooltotData["inv"][2]["value"])
        qpltot = float(pooltotData["inv"][3]["value"])

        winfirstrow = ["time"]
        for i in wincomb:
            winfirstrow.append(i)

        qinfirstrow = ["time"]
        for i in qincomb:
            qinfirstrow.append(i)
            
        qplfirstrow = ["time"]
        for i in qplcomb:
            qplfirstrow.append(i)
            
        winmoney = []
        plamoney = []
        qinmoney = []
        qplmoney = []
        for i in winbet:
            winmoney.append(int(wintot*0.825/float(i)))
            plamoney.append(int(platot*0.825/float(i)))
        for i in qinbet:
            qinmoney.append(int(qintot*0.825/float(i)))
            qplmoney.append(int(platot*0.825/float(i)))
            
        wininsert = [now]
        for i in winmoney:
            wininsert.append(i)
            
        plainsert = [now]
        for i in plamoney:
            plainsert.append(i)

        qininsert = [now]
        for i in qinmoney:
            qininsert.append(i)
            
        qplinsert = [now]
        for i in qplmoney:
            qplinsert.append(i)

        if (firsttime):
            winbetsheet.insert_row(winfirstrow, 1)
            plabetsheet.insert_row(winfirstrow, 1)
            qinbetsheet.insert_row(qinfirstrow, 1)
            qplbetsheet.insert_row(qplfirstrow, 1)

        winbetsheet.insert_row(wininsert, 2)
        plabetsheet.insert_row(plainsert, 2)
        qinbetsheet.insert_row(qininsert, 2)
        qplbetsheet.insert_row(qplinsert, 2)

        winbetsheet.update_acell('a1', wintot)
        plabetsheet.update_acell('a1', platot)
        qinbetsheet.update_acell('a1', qintot)
        qplbetsheet.update_acell('a1', qpltot)
        done+=1
        print ("done")
        time.sleep(sleeptime)
        
        
    except:
        error+=1
        print ("error")