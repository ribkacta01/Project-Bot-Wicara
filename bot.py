import time
from xml.dom.minidom import Element
import numpy as np
import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def youtube_login(email,password):

	op = webdriver.ChromeOptions()
	op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	op.add_argument('--headless')
	op.add_argument('--disable-dev-shm-usage')
	op.add_argument('--no-sandbox')
	
	driver = webdriver.Chrome(executable_path= r'C:\Program Files (x86)\chromedriver.exe')
	driver.maximize_window()
	driver.get('https://accounts.google.com/ServiceLogin?hl=en&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fhl%3Den%26feature%3Dsign_in_button%26app%3Ddesktop%26action_handle_signin%3Dtrue%26next%3D%252F&uilel=3&passive=true&service=youtube#identifier')

	driver.find_element(By.ID, "identifierId").send_keys("00011sunn@gmail.com")
	time.sleep(3)
	driver.find_element(By.ID, "identifierNext").click()
	time.sleep(2)
	
	
	driver.find_element(By.CLASS_NAME, "whsOnd").send_keys("fullsun2901")
	time.sleep(2)
	driver.find_element(By.ID, "passwordNext").click()
	

	return driver

def comment_page(driver,urls,comment):

	if len( urls ) == 0:
		print ('Youtube Comment Bot: Finished!')
		return []
	
	url = urls.pop()
	
	driver.get(url)
	print(url)
	driver.implicitly_wait(1)

	if not check_exists_by_xpath(driver,'//*[@id="movie_player"]'):
		return comment_page(driver, urls, random_comment())
	time.sleep(4)
	driver.execute_script("window.scrollTo(0, 600);")
	
	if not check_exists_by_xpath(driver,'//*[@id="simple-box"]/ytd-comment-simplebox-renderer'):
		return comment_page(driver, urls, random_comment())

	if check_exists_by_xpath(driver,'//*[@id="contents"]/ytd-message-renderer'):
		return comment_page(driver, urls, random_comment())

	WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")))

	driver.find_element_by_css_selector("ytd-comments ytd-comment-simplebox-renderer div#placeholder-area").click()
	driver.implicitly_wait(5)
	driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(comment)
	driver.find_element_by_xpath('//*[@id="contenteditable-root"]').send_keys(Keys.CONTROL, Keys.ENTER)

	post = WebDriverWait(driver, 15).until(
	    EC.element_to_be_clickable((By.CSS_SELECTOR,'ytd-comments ytd-comment-simplebox-renderer'))
	)
	post.click()

	r = np.random.randint(2,5)
	time.sleep(r)

	return comment_page(driver, urls, random_comment())


def random_comment():
# You can edit these lines=======
	messages = [
		'The Best!',
		'Nice video!',
		'Loved it',
		'Best video ever',
		'Great video'
	]
# ===============================
	r = np.random.randint(0, len(messages))

	return messages[r]
 
def check_exists_by_xpath(driver,xpath):
	
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False

    return True

if __name__ == '__main__':
# You should edit these lines=======
	email = '00011sunn@gmail.com'
	password = 'fullsun2901'
# ==================================

	urls = [
	  'https://www.youtube.com/watch?v=qORaYudQ7Zc',
	]
	
	inp = open("url.txt","r")
	for line in inp.readlines():
			urls.append(line)
  	

	driver = youtube_login(email, password)

	comment_page(driver,urls,random_comment())