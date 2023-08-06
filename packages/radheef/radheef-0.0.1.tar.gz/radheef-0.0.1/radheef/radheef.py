# Author : Moots (github.com/mootss)

# import dependencies
from requests import get
from bs4 import BeautifulSoup

# main func
def radheef(word):
	query = ("http://radheef.mv/result/?query={}").format(word)
	page = get(query)
	soup = BeautifulSoup(page.content, "html.parser")
	ss = soup.find(id="myTabContent")
	res = ss.find(class_="description")

	return res.text

	

# last updated: 22/01/2021