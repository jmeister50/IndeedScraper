import pandas as pd
import requests
from bs4 import BeautifulSoup
import config as cfg

def SearchIndeed(keyword, salary, city, experience_level=None,distance=None):

	page = 0
	base_url = f"https://www.indeed.com/jobs?q={keyword},{salary}&l={city}&start={page}"

	if experience_level != None:
		url =  base_url + f"&explvl={experience_level}"
		print(url)
	else:
		url = base_url
		print(url)

	if distance != None:
		url =  base_url + f"&radius={distance}"
		print(url)
	else:
		url = base_url
		print(url)


	# Request page raw html and open with bs4
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')

	# Get all divs with class title
	jobs = soup.findAll("div", {"class": "row"})

	positions, companies, locations , links = [],[],[],[]

	# Print each job title in list
	for job in jobs:
		job_titles = job.findAll("a", {"data-tn-element": "jobTitle"})
		for job_title in job_titles:
			if len(job_title["title"]) > 0:
				positions.append(job_title["title"])
			else:
				continue
		
		company_names = job.findAll("span", {"class": "company"})
		for company_name in company_names:
			if len(company_name.text.replace("\n","")) > 0:
				companies.append(company_name.text.replace("\n",""))
			else:
				continue

		company_locations = job.findAll("div", {"class": "recJobLoc"})
		for company_location in company_locations:
			if len(company_location["data-rc-loc"]) > 0:
				locations.append(company_location["data-rc-loc"])
			else:
				continue
		job_links = job.findAll("a", {"data-tn-element": "jobTitle"})
		for job_link in job_links:
			if len(job_link["href"]) > 0:
				links.append(job_link["href"])
			else:
				continue

	#print(companies)
	print(len(positions),len(locations),len(companies),len(links))
	career_info = pd.DataFrame(
		{
		"JobTitle": positions,
		"CompanyName": companies,
		"JobLocation": locations,
		"JobLink": links,
		}
	)
	career_info.fillna("Missing")
	career_info.to_csv("JobListings.csv")

if __name__ == '__main__':

	# Search by keyword, salary, location, experience level, distance from desired location.

	SearchIndeed("Manager","60000", "Chicago","entry_level","25")