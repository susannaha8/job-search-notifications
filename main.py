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
	#driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
	driver.get('https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Seattle%2C%20Washington%2C%20United%20States&locationId=&geoId=104116203&f_TPR=r86400&distance=25&position=1&pageNum=0')
	#driver.get("https://www.selenium.dev/selenium/web/web-form.html")
	driver.implicitly_wait(0.5)
	jobList = []
	print(driver.title)
	while (driver.title == "Sign Up | LinkedIn"):
		driver.get('https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Seattle%2C%20Washington%2C%20United%20States&locationId=&geoId=104116203&f_TPR=r86400&distance=25&position=1&pageNum=0')
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
		time.sleep(1)
		elements = driver.find_elements(by=By.XPATH, value="//div[@class='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card']")
		# show_more = driver.find_element(By.XPATH, "//button[@aria-label='Show more, visually expands previously read content above']")
		# show_more.click()
		# print(elements[0].text.split("\n"))
		#all_text = driver.page_source

		#content = driver.find_element(By.XPATH, "//div[@class='show-more-less-html__markup relative overflow-hidden']")
		#print(content.text)

		#for each job post, first check title and company, then check description for minimum experience
		i = 0
		for e in elements:
			print("ELEMENT:" + str(i))
			i = i + 1
			time.sleep(5)
			e.click()
			print(e.text)
			info = e.text.split("\n")
			if not checkInfo(excludedCompanies, excludedTitles, info):
				continue
			time.sleep(5)
			show_more = driver.find_element(By.XPATH, "//button[@aria-label='Show more, visually expands previously read content above']")
			show_more.click()
			description = (driver.find_element(By.XPATH, "//div[@class='show-more-less-html__markup relative overflow-hidden']")).text
			if (checkYears(excludedYears, description)):
				print("job checked")
				jobList.append({"title":info[1], "company":info[2], "location": info[3], "postDate":info[-1], "description":"", "applicationLink":""})
		
		print(jobList)

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
      excludedCompanies= ["Jobot","Dice"]
      excludedYears = ['4+','5+','6+','7+','8+','9+','10+'] #maybe change this to just find the years of exp
      excludedTitles = ["Senior","Lead","Principle","III","Sr"]
      scrapeLinkedIn(excludedYears, excludedCompanies, excludedTitles) #change to pass in all args
	