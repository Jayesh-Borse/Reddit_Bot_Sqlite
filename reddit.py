from bs4 import BeautifulSoup
import urllib.request,urllib.parse,urllib.error
from selenium import webdriver
import sqlite3
from time import sleep

PATH = "D:\PythonC\my_stuff\webdrivers\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get('https://www.reddit.com/r/india/')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(15)
html=driver.execute_script("return document.documentElement.outerHTML")
soup=BeautifulSoup(html,'html.parser')

tag=soup.find_all('div',{'class':'lrzZ8b0L6AzLkQj5Ww7H1'})
news=soup.find_all('h3')
posted_by=soup.find_all('a',{'class':'_2tbHP6ZydRpjI44J3syuqC _23wugcdiaj44hdfugIAlnX oQctV4n0yUb0uiHDdGnmE'})

comment=soup.find_all('span',{'class':'FHCV02u6Cp2zYL0fhQPsO'})

conn=sqlite3.connect("reddit_db.sqlite")
cur = conn.cursor()

tag_list = list()
for x in tag:
	tg = x.find('span')
	if tg is None:
		continue
	else :
		tag_list.append(tg.contents[0])

new_list = list()
for y in news:
	new_list.append(y.contents[0])

posted_list=list()
for z in posted_by:
	posted_list.append(z.contents[0])

comment_list=list()
for w in comment:
	comment_list.append(w.contents[0])

cur.executescript('''
DROP TABLE IF EXISTS Main;
DROP TABLE IF EXISTS Tags;

CREATE TABLE Main(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	tag_id INTEGER,
	heading TEXT,
	comment INTEGER,
	posted_by TEXT

);
CREATE TABLE Tags(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	tag TEXT UNIQUE
)
''')

for item in tag_list:
	cur.execute(''' INSERT OR IGNORE INTO Tags (tag) VALUES(?)
	''',(item,))
conn.commit()
for i in range(len(tag_list)):
	tags=tag_list[i]
	head=new_list[i]
	comments=comment_list[i]
	post=posted_list[i]

	cur.execute('''SELECT id FROM Tags WHERE tag = ?''',(tags,))
	t_id=cur.fetchone()[0]

	cur.execute('''INSERT OR IGNORE INTO Main (tag_id,heading,comment,posted_by) VALUES(?,?,?,?)''',(t_id,head,comments,post))
conn.commit()
