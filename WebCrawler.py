#-*- coding = utf-8 -*-

from bs4 import BeautifulSoup  # analist website
import re                      # match the charater roles
import urllib.request            # find URL
import urllib.error
import xlwt                          # use excel
import sqlite3                      # use SQLite


def main():
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getData(baseurl)
    savepath = ".\\RankingdoubanMovie.xls"
    dbpath = ".\\movie.db"
    saveData(datalist,savepath)
    saveDatatoDB =(datalist,dbpath)
    #askURL("https://www.wyav.tv/list?keyword=&star=&page=")



findLink = re.compile(r'<a href="(.*?)>')
findImgSrc = re.compile(r'<img.*src="(.*?)"',re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*)</span>')
findDB = re.compile(r'<p class="">(.*?)</p>',re.S)

def getData(baseurl):
    datalist = []
    for i in range(0,10):    #for loop to run all websites
        url = baseurl + str(i*25)
        html = askURL(url)

        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div', class_="item"):  #find the match item
            # print(item) # test
            data = []
            item = str(item)

            Link = re.findall(findLink,item)[0]
            data.append(Link)

            imgSrc = re.findall(findImgSrc,item)[0]
            data.append(imgSrc)

            titles = re.findall(findTitle, item)
            if(len(titles) == 2):
                ctitle = titles[0] #first name
                data.append(ctitle)
                otitle = titles[1].replace("/","") #second name
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')

            rating = re.findall(findRating,item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq,item)
            if len(inq) !=0:
                inq =inq[0].replace("。","")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findDB,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)
            bd = re.sub('/'," ",bd)
            data.append(bd.strip())  #delete space

            datalist.append(data) #data input to datalist





    return datalist
    



#specified website
def askURL(url):
    head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
    } #tell service that is a true user ask request

    request = urllib.request.Request(url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
            
    return html
    
def saveData(datalist,savepath):
    print("test")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('douban movie', cell_overwrite_ok=True)
    col = ("link","picture","name","other name","rank","comment","summary","other information")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("The %d movie"%i)
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])


    book.save(savepath)



def saveDatatoDB(datalist,dbpath):
    print("database test")



def init_db():
    sql = ""
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor = execute(sql)
    conn.commit()
    conn.close()



if __name__ == "__main__":
    main()