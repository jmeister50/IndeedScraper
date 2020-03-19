import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import config as cfg

url = cfg.url
browser = webdriver.Chrome(cfg.driver)

def wait_until_clickable_xpath(xpath):

	element = WebDriverWait(browser, 20).until(
		EC.element_to_be_clickable((By.XPATH, str(xpath)))
		)
	element.click()
	return element

def search_jobs(keyword,salary,city):
	
	# Go to starting url
	browser.get(url)

	# Clicking the keyword in the 'keyword' box. 
	element = wait_until_clickable_xpath('//*[@id="text-input-what"]')
	element.send_keys(keyword+ ", " + salary)



	# Clicking the city in the 'location' box.
	element = wait_until_clickable_xpath('//*[@id="text-input-where"]')
	element.send_keys(Keys.CONTROL + "a" + Keys.DELETE)
	element.send_keys(city)

	
	# Clicking the 'Find Jobs' Button.
	wait_until_clickable_xpath('//*[@id="whatWhereFormId"]/div[3]/button')

	# Create list of jobs, comapny names, locations and wages. 
	job_titles = browser.find_elements_by_class_name('title')
	company_names = browser.find_elements_by_class_name('company')
	company_locations = browser.find_elements_by_class_name('location')

	jobs, companies, locations, links = [],[],[],[]
	
	# Append job title to list.

	for job in job_titles:
		jobs.append(job.text)
		href = str(job.find_element_by_css_selector('a').get_attribute('href'))
		links.append(href)
		
	for company in company_names:
		companies.append(company.text)
		
	for location in company_locations:
		locations.append(location.text)
			

	# Pairs names and rates in a Dictionary.//*[@id="sja0"]
	career_info = pd.DataFrame(
		{
		"JobTitle": jobs,
		"CompanyName": companies,
		"JobLocation": locations,
		"JobLink": links
		}
	)
	career_info.fillna("Missing")
	career_info.to_csv("JobListings.csv")


if __name__ == '__main__':
	
	search_jobs("Manager", "$60,000", "Chicago")