import zipfile
import requests
import io
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from user_agent import generate_user_agent
from time import sleep


urlPortal = 'http://www.portaltransparencia.gov.br/download-de-dados/'
urls = ["ceis","cepim","cnep"]
dirExtract = 'PORTAL/'

userAgent = generate_user_agent(device_type="desktop")

options = Options()
options.add_argument('--headless')
options.add_argument(f'user-agent={userAgent}')
options.add_argument('--disable-gpu')
options.add_argument('--lang=pt_BR')
# prefs = {"download.default_directory":path}   #path is a string containing the directory you want the downloaded songs stored
# options.add_experimental_option("prefs",prefs)
options.add_argument('--no-sandbox')
options.add_argument("--disable-notifications")
options.add_argument('--disable-dev-shm-usage')


for url in urls:

	driver = webdriver.Chrome(options = options)
	driver.delete_all_cookies()
	driver.set_window_size(1061, 701)
	driver.get(urlPortal + url)
	sleep(4)
	link = driver.find_element(By.XPATH,'//*[@id="link-unico"]/li/a').get_attribute('href')
	print(link)
	driver.quit()
	
	fileZip = io.BytesIO(requests.get(link).content)

	with zipfile.ZipFile(fileZip) as zip_ref:
		zip_ref.extractall(dirExtract)
