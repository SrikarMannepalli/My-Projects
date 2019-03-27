import requests
import bs4
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import flask
import pymysql.cursors
from flask import Flask
from flask_mysqldb import *

page=requests.get('http://indianexpress.com/section/sports/')
soup=BeautifulSoup(page.content,'html.parser')
temp=soup.find('div',{'class':'nation'})
title=[]
title=temp.findAll('div',{'class':'title'})
total_num=0
for i in title:
	total_num+=1
headings=[]
img=[]
links=[]
imagelinks=[]
imagewidths=[]
imageheights=[]
con=pymysql.connect(host='localhost',
                    user='root',
                    password='Albus Dumbledore',
                    db='myFlaskApp',
                    charset='utf8',
                    cursorclass=pymysql.cursors.DictCursor)
cur=con.cursor()
cur.execute('DROP TABLE IF EXISTS datatables')
cur.execute('CREATE TABLE datatables(id INT(11) AUTO_INCREMENT PRIMARY KEY,heading VARCHAR(1000),link VARCHAR(1000),imagelink VARCHAR(1000),imagewidth INT(11),imageheight INT(11),article VARCHAR(13000))')
for i in range(0,total_num):
	dammit=UnicodeDammit(title[i].get_text())
	headings.append(dammit.unicode_markup)
	links.append(title[i].find('a')['href'])
	img=temp.find_all('div',{'class':'snaps'})
	imagelinks.append(img[i].find('img')['data-lazy-src'])
	imageheights.append(img[i].find('img')['height'])
	imagewidths.append(img[i].find('img')['width'])
	reqpage=requests.get(links[i])
	reqsoup=BeautifulSoup(reqpage.content,'html.parser')
	yo=reqsoup.find('div',{'class':'articles'}).findAll('p')
	length=len(yo)
	mypara=''
	for j in range(0,length-1):
		dammit=UnicodeDammit(yo[j].get_text().encode('utf8'))
		pp=dammit.unicode_markup
		pp=str(pp)
		mypara=mypara+"\n"+pp
		mypara=str(mypara)
	cur.execute('INSERT INTO datatables(heading,link,imagelink,imagewidth,imageheight,article) VALUES(%s,%s,%s,%s,%s,%s)',(str(headings[i]),str(links[i]),str(imagelinks[i]),str(imagewidths[i]),str(imageheights[i]),mypara))
	con.commit()
