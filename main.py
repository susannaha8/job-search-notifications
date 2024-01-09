#given a dictionary of companies/ company job sites, 
#return new job posts

#eventually, send email for new job posts

#step 1: create this for a single site
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import secrets

# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

def linkedinAPI():
    ret = requests.get("https://api.linkedin.com/v2/job-search") 
    return ret.json()

def add_entry_to_notion(data = None): #assume db already exists
	headers = {
		"Authorization": "Bearer " + secrets.NOTION_TOKEN,
		"Content-Type": "application/json",
		"Notion-Version": "2022-06-28",
	}

	#create_url = "https://api.notion.com/v1/pages"
	url = f"https://api.notion.com/v1/databases/{secrets.DATABASE_ID}/query"

	#payload = {"parent": {"database_id": secrets.DATABASE_ID}, "properties": data}
	payload = {"page_size": 1}
	res = requests.get(url, headers=headers, json=payload)
	print(res.status_code)
	print(res)
	#res = requests.post(create_url, headers=headers, json=payload)

	return res

#get any element: timeout after 15 seconds
def wait(driver,value):
	try:
		print("WAITING " + value)
		element = WebDriverWait(driver, 15).until(
			EC.element_to_be_clickable((By.XPATH, value)))
		return element
	except Exception as e:
		print(e)
		return None
	

def checkInfo(excludedCompanies=[], excludedTitles=[], info=[]):
	if (info[2] in excludedCompanies):
		return False
	for word in excludedTitles:
		if word in info[1]:
			return False
	return True

def checkYears(excludedYears=[], all_text=""):
	for y in excludedYears:
		if (y in all_text):
			print("found excluded year: " + str(y))
			return False
	return True


def scrapeLinkedIn(excludedYears=[], excludedCompanies=[], excludedTitles=[]):
      
	driver = webdriver.Chrome()
	driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3792269702&distance=25&f_TPR=r86400&geoId=104116203&keywords=Software%20Engineer&location=Seattle%2C%20Washington%2C%20United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&sortBy=DD')
	driver.implicitly_wait(0.5)
	jobList = []
	print(driver.title)
	while (driver.title == "Sign Up | LinkedIn"):
		driver.get('https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Seattle%2C%20Washington%2C%20United%20States&locationId=&geoId=104116203&f_TPR=r86400&distance=25&position=1&pageNum=0')
	try:
		#items = driver.find_element(By.CLASS_NAME, 'jobs-search__results-list') #only for under 1000 jobs
		no_of_jobs = int(driver.find_element(By.CLASS_NAME, 'results-context-header__job-count').text.split(' ')[0])
		print(no_of_jobs)

		#get all the job posts
		elements = driver.find_elements(by=By.XPATH, value="//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card']")
	
		# #scroll to the bottom of the page
		# scrolls = no_of_jobs/25 + 1
		# while True:
		# 	scrolls -= 1
		# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		# 	time.sleep(1)
		# 	if scrolls < 0:
		# 		break

	except Exception as e: #could not get results page
		print(e)
		return 


	#for each job post
	i = 0
	for e in elements:
		
		try:
			#print the element, check title and company
			print("ELEMENT:" + str(i))
			print(e.text)
			i = i + 1
			info = e.text.split("\n")
			if not checkInfo(excludedCompanies, excludedTitles, info):
				continue

			#click on the element
			e.click()
			
			#show more, check description
			show_more = wait(driver, "//button[@aria-label='Show more, visually expands previously read content above']")
			#show_more = driver.find_element(By.XPATH, "//button[@aria-label='Show more, visually expands previously read content above']")
			show_more.click()
			
			#description = (driver.find_element(By.XPATH, "//div[@class='show-more-less-html__markup relative overflow-hidden']")).text
			description = wait(driver, "//div[@class='show-more-less-html__markup relative overflow-hidden']").text
			if not checkYears(excludedYears, description):
				continue

			print("job checked")

			#get application link, add job to list
			#apply = driver.find_element(By.XPATH, "//button[@class='sign-up-modal__outlet top-card-layout__cta mt-2 ml-1.5 h-auto babybear:flex-auto top-card-layout__cta--primary btn-md btn-primary']")
			apply = wait(driver, "//button[@class='sign-up-modal__outlet top-card-layout__cta mt-2 ml-1.5 h-auto babybear:flex-auto top-card-layout__cta--primary btn-md btn-primary']")
			apply.click()

			#external_site = driver.find_element(By.XPATH, "//a[@class='sign-up-modal__sign-up-later']")	
			external_site = wait(driver, "//a[@class='sign-up-modal__sign-up-later']")
			external_site.click()

			time.sleep(5)
			driver.switch_to.window(driver.window_handles[1])
			url = driver.current_url
			driver.close()
			driver.switch_to.window(driver.window_handles[0])
			new_job = {"title":info[1], "company":info[2], "location": info[3], "postDate":info[-1], "description":"", "applicationLink":url}
			jobList.append(new_job)
			print(new_job)
		
		except Exception as e:
			print(e) #this current job had issues
			continue

	print(jobList)


	

if __name__ == "__main__":
      excludedCompanies= ["Jobot","Dice"]
      excludedYears = ['4+','5+','6+','7+','8+','9+','10+'] #maybe change this to just find the years of exp
      excludedTitles = ["Senior","Lead","Principle","III","Sr"]
      #scrapeLinkedIn(excludedYears, excludedCompanies, excludedTitles) #change to pass in all args
      add_entry_to_notion()
	

