from bs4 import BeautifulSoup
import requests
import pandas as pd
import threading
import time

start_time = time.time()

joblist = []


def do_the_thing(page_index):
    soup = BeautifulSoup(requests.get(f'https://www.freelancer.com/jobs/{page_index}/?keyword=web%20scraping').text, 'lxml')
    all_jobs = soup.find_all('div', class_='JobSearchCard-primary')

    print(f'scraping page {page_index}')

    for m in all_jobs:
        data = {
            'title' : m.find('a', class_='JobSearchCard-primary-heading-link').text.strip() if m.find('a', class_='JobSearchCard-primary-heading-link') != None else '',
            'bid-amount' : m.find('div', class_='JobSearchCard-primary-price').text.strip() if m.find('div', class_='JobSearchCard-primary-price') != None else '',
            'short-description' : m.find('p', class_='JobSearchCard-primary-description').text.strip() if m.find('p', class_='JobSearchCard-primary-description') != None else ''
        }

        joblist.append(data)

thrds = [threading.Thread(target=do_the_thing, args=(i,)) for i in range(60)]
[x.start() for x in thrds]
[x.join() for x in thrds]


df = pd.DataFrame(joblist)
df.to_csv('jobs.csv')
print(df.head())

print(f'this program took {time.time() - start_time}s to run ')

# do_the_thing(10)

