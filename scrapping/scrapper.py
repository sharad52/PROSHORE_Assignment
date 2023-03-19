import requests
from bs4 import BeautifulSoup

import dbc


def extractData(tableName):
    dbc.truncateTable(tableName)

    baseUrl = "https://proshore.eu/resources/"
    response = requests.get(baseUrl)
    soup = BeautifulSoup(response.text, 'html.parser')
    for div in soup.find_all("div", class_="playground-item-col"):
        print('***************************************************')
        job = []  
        title = (div.find('div', class_='playground-body white').h4.string)
        description = (div.find('div', class_='playground-body white').div.string)
        blog_image_url = (div.find('div', class_='playground-image').img['data-src']) 
        author_name = (div.find('div', class_='playground-author-body').find('div', class_='playground-author-name').string) 
        author_image_url = (div.find('div', class_='playground-author-image').img['data-src']) 
        author_designation = (div.find('div', class_='playground-author-body').find('div', class_='playground-author-description').string)
        flag = div.find('div', class_='playground-read-time').span
        if flag:
            reading_time = (div.find('div', class_='playground-read-time').span.string)
        else:
            reading_time = (div.find('div', class_='playground-read-time').span)

        job.append(title)
        job.append(description)
        job.append(blog_image_url)
        job.append(author_name)
        job.append(author_image_url)
        job.append(author_designation)
        job.append(reading_time)

        dbc.insertData(job, tableName)
        
for i in range(0, 5000):
    print('success')
    extractData('public.content')