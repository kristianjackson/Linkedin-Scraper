import csv
import re
import requests
from bs4 import BeautifulSoup
import time

filename = 'jobs.csv'
f = csv.writer(open(filename, 'w', newline=''))

f.writerow(['Job Name', 'Job Link'])

jobName = 'Technology' + '%20' + 'Consultant'
place = 'United' + '%20' + 'States'
amountOfJobs = 100
joblist = []

print("# Collecting first n job links")

for page in range(25, amountOfJobs, 25):
    print('Page: ' + str(page))
    print('https://www.linkedin.com/jobs/search?keywords=' + jobName +
          '&location=' + place + '&start=' + str(page))
    html = requests.get('https://www.linkedin.com/jobs/search?keywords=' +
                        jobName + '&location=' + place + '&start=' + str(page))
    soup = BeautifulSoup(html.text, 'html.parser')
    joblist = joblist + soup.find(class_='jobs-search__results-list').findAll(
        'a', {'class': 'result-card__full-card-link'})

print("# Filtering jobs")

filteredJobs = []

for job in joblist:
    link = job.get('href', '#')
    name = job.find('span').text

    jobHtml = requests.get(str(link))
    jobSoup = BeautifulSoup(jobHtml.text, 'html.parser')

    description = jobSoup.find(class_='show-more-less-html__markup')
    found = description.findAll(string=re.compile(r"\bWashington\b", re.I))
    if found:
        print('Found: ', name)
        f.writerow([name, link])
