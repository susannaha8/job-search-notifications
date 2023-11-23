#given a dictionary of companies/ company job sites, 
#return new job posts

#eventually, send email for new job posts

#step 1: create this for a single site
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def linkedinAPI():
    ret = requests.get("https://api.linkedin.com/v2/job-search") 
    return ret.json()

def scrapeLinkedIn():
	r = requests.get('https://www.linkedin.com/jobs/search/?currentJobId=3739458491&f_E=2&f_TPR=r604800&f_WT=1%2C3&geoId=103644278&keywords=Software%20Engineer&location=United%20States&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=DD') 
  
	# Parsing the HTML 
	soup = BeautifulSoup(r.content, 'html.parser') 
	
	job_list = soup.find("div", {"class": "authentication-outlet"}) 
	print(job_list)
	#content = job_list.find_all('li') 
	

if __name__ == "__main__":
      scrapeLinkedIn()
	