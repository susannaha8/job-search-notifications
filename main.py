#given a dictionary of companies/ company job sites, 
#return new job posts

#eventually, send email for new job posts

#step 1: create this for a single site
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager


def linkedinAPI():
    ret = requests.get("https://api.linkedin.com/v2/job-search") 
    return ret.json()

def scrapeLinkedIn():
      
	driver = webdriver.Chrome()
	#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
	driver.get('https://www.linkedin.com/jobs/search?keywords=%22junior%22%20%22software%22&location=Seattle%2C%20Washington%2C%20United%20States&locationId=&geoId=104116203&f_TPR=r86400&distance=25&position=1&pageNum=0')
	#driver.get("https://www.selenium.dev/selenium/web/web-form.html")
	driver.implicitly_wait(0.5)
	
	print(driver.title)
	try:
		#items = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list') #only for under 1000 jobs
		no_of_jobs = int(driver.find_element(By.CLASS_NAME, 'results-context-header__job-count').text.split(' ')[0])
		print(no_of_jobs)

		# #scroll to the bottom of the page
		# scrolls = no_of_jobs/25 + 1
		# while True:
		# 	scrolls -= 1
		# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		# 	time.sleep(1)
		# 	if scrolls < 0:
		# 		break
		
		#get all the job posts
		elements = driver.find_elements(by=By.XPATH, value="//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card']")
		show_more = driver.find_element(By.XPATH, "//button[@aria-label='Show more, visually expands previously read content above']")
		print(show_more.text)
		show_more.click()
		content = driver.find_element(By.XPATH, "//div[@class='show-more-less-html__markup relative overflow-hidden']")
		print(content)
		# i = 0
		# for e in elements:
		# 	print("ELEMENT:" + str(i))
		# 	i = i + 1
		# 	e.click()
		# 	time.sleep(3)
		# 	show_more = driver.find_element(By.XPATH, "//button[@aria-label='Show more, visually expands previously read content above']")
		# 	show_more.click()
		# 	print(e.text)
	except Exception as e:
        	print(e)
	# Parsing the HTML
	#soup = BeautifulSoup(r.content, 'html.parser')
	#print (soup)

       

       #res = soup.select('#global-nav')
       #res = soup.find_all("div", class_="job-search-results-list")
       

	#job_list = soup.find("div", {"class": "authentication-outlet"}) 
	#print(job_list) 
	#content = job_list.find_all('li') 
	

if __name__ == "__main__":
      scrapeLinkedIn()
	