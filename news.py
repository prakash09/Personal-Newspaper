import urllib2
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import random
import re
import smtplib
import json

def google_news():
	query='Delhi'
	final_url = ('https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q='+query+'&userip=INSERT-USER-IP')
	json_obj=urllib2.urlopen(final_url)
	data=json.load(json_obj)

        data_file=open("letter.html",'a')
        data_file.write("<div style=\"background-color:mistyrose\">")

        for news3 in data['responseData']['results']:
		atitle="<h3>"+"Headline:"+str(news3['titleNoFormatting'])+"</h3><br>"
                data_file.write(atitle)
		alink=str(news3['unescapedUrl'])
                apublisher="<a href="+alink+">"+"Site:"+str(news3['publisher'])+" Full story...</a>"
         	data_file.write(apublisher)
        data_file.write("</div>")
        data_file.write("</body></html>")
        data_file.close()
        return None

def bigriddles():
    puzzles_list=[]
    paragraph=""
    links=["http://www.bigriddles.com/medium-riddles",
            "http://www.bigriddles.com/easy-riddles",
            "http://www.bigriddles.com/famous-riddles"
            "http://www.bigriddles.com/logic-riddles",
            "http://www.bigriddles.com/good-riddles",
            "http://www.bigriddles.com/microsoft-interview-riddles",
            "http://www.bigriddles.com/hard-riddles"]
    htmltext=urllib2.urlopen(random.choice(links))
    soup=BeautifulSoup(htmltext.read())
    for puzzles in soup.findAll('a',href=True):
        if re.search("/riddle/",str(puzzles),flags=0):
            puzzles_list.append(puzzles['href'])
    htmltext=urllib2.urlopen("http://www.bigriddles.com"+random.choice(puzzles_list))
    soup=BeautifulSoup(htmltext.read())
    heading=soup.h2.string
    for para in soup.findAll('p'):
        paragraph+=para.string+"\n"
    data_file=open("letter.html",'a')
    data_file.write("<div style=\"background-color:orange\">")
    data_file.write("<h1>"+heading+"</h1>")
    data_file.write("<p>"+paragraph+"</p>")
    data_file.write("</div>")
    data_file.close()
    return None


def vocabulary():
    synonyms=""
    dailyvocab=urllib2.urlopen("http://dailyvocab.com")
    soup=BeautifulSoup(dailyvocab)
    word_url=soup.find('h1',class_='entry-title').a['href']
    todays_word_url=urllib2.urlopen(word_url)
    todays_word=word_url.split('/')[-2]
    data_file=open('letter.html','a')
    data_file.write("<div style=\"background-color:tan\">")
    data_file.write("<h2>"+todays_word+"</h2></br>")
    soup=BeautifulSoup(todays_word_url)
    for i in soup.findAll(['strong','a'],text=True): #finding synonyms
        if re.search("Synonym",str(i),flags=0):
            if re.search("rel",str(i),flags=0):
                synonyms=synonyms+i.string+","
    data_file.write("<p><b>Synonyms:<b>"+synonyms+"</p><br>")

    hindi_meaning=soup.findAll('strong')[5]
    data_file.write("<p>"+str(hindi_meaning)+"</p>")
    data_file.write("</div>")
    data_file.close()
    return None


def send_email():
	FROM = "prakash.gbpec@gmail.com"
	TO = "prakash.kumar94@live.com"
	SUBJECT = "Delhi Headlines"
        msgRoot=MIMEMultipart('related')
        msgRoot['Subject']=SUBJECT
        msgRoot['From']=FROM
        msgRoot['To']=TO
        msgAlternative=MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)

        with open("letter.html","r") as myfile:
            data=myfile.read().replace('\n','')

        msgHtml=MIMEText(data,'html')
        msgAlternative.attach(msgHtml)
        part1=MIMEText("this is plane text",'plain')
        msgRoot.attach(part1)
	# Send the mail
        server = smtplib.SMTP(host ='smtp.gmail.com', port=587)
        server.starttls()
        server.login('email-id', 'password') #email id and password from which email will be sent
        server.sendmail(FROM,TO,msgRoot.as_string())
        server.quit()
        #server.close()

if __name__=="__main__":
    #data_file=open("letter.html",'w')
    #data_file.write("<html><body>")
    #data_file.close()
    #vocabulary()
    #bigriddles()
    #google_news()
    send_email()


