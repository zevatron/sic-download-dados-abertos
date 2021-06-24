import datetime
import io
import os
import zipfile
import requests
from bs4 import BeautifulSoup

year = datetime.datetime.now().year
years = [year-1,year]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
url = "http://ftp.dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/"
dirExtract = 'FINANCEIRO/'
linksAnos = []
filesName = []

for y in years:
	urlAno = url + str(y) + '/'
	req = requests.get(urlAno, headers = headers)
	soup = BeautifulSoup(req.content,'html.parser')
	links = soup.find_all('a')
	linksAnos += [urlAno + l.get('href') for l in links if l.get('href').endswith('.zip')]

# urlAno = url + str(year) + '/'
# req = requests.get(urlAno, headers = headers)
# soup = BeautifulSoup(req.content,'html.parser')
# links = soup.find_all('a')
# linksAnos += [urlAno + l.get('href') for l in links if l.get('href').endswith('.zip')]



for link in linksAnos:
	fileZip = io.BytesIO(requests.get(link).content)
	with zipfile.ZipFile(fileZip) as zip_ref:
		members = zip_ref.namelist()
		filesName += members
		zip_ref.extractall(dirExtract)	


for file in filesName:
	os.replace(dirExtract + file, dirExtract + 'FINANCEIRO-' + file)