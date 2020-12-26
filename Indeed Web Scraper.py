#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install requests


# In[2]:


import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# In[ ]:





# In[3]:


def get_url(position, location):
    """Generate a url from position and location"""
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url


# In[4]:


url = get_url('backend developer', 'mumbai')


# In[5]:


url


# In[6]:


response = requests.get(url)


# In[7]:


response


# In[8]:


response.reason


# In[9]:


soup = BeautifulSoup(response.text, 'html.parser')


# In[10]:


cards = soup.find_all('div', 'jobsearch-SerpJobCard')


# In[11]:


len(cards)


# In[12]:


## Prototype the model with a single record


# In[13]:


card = cards[0]


# In[14]:


card


# In[15]:


atag = card.h2.a


# In[16]:


atag['title']


# In[17]:


# get method is prefered because if the data doesn't exist then the above
# code will give an attribute error whereas get method will return none
job_title = atag.get('title')


# In[18]:


job_url = 'https://www.indeed.com' + atag.get('href')


# In[19]:


card.find('span','company').text.strip()


# In[20]:


card.find('div', 'recJobLoc').get('data-rc-loc')


# In[21]:


job_summary = card.find('div','summary').text.strip()


# In[22]:


post_date = card.find('span','date').text


# In[23]:


today = datetime.today().strftime('%Y-%m-%d')


# In[24]:


try:
    job_salary = card.find('span','salaryText').text.strip()
except AttributeError:
    job_salary = ''


# In[25]:


## Generalize the model with a function


# In[26]:


def get_record(card):
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://www.indeed.com' + atag.get('href')
    company = card.find('span','company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div','summary').text.strip()
    post_date = card.find('span','date').text
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        job_salary = card.find('span','salaryText').text.strip()
    except AttributeError:
        job_salary = ''
    
    record = (job_title, company, job_location, post_date, today, job_summary, job_salary )
    
    return record


# In[27]:


records = []

for card in cards:
    record = get_record(card)
    
    records.append(record)


# In[28]:


records[0]


# In[29]:


url = 'https://in.indeed.com' + soup.find('a',{'aria-label':'Next'}).get('href')


# In[30]:


url


# In[31]:


while True:
    try:
        url = 'https://in.indeed.com' + soup.find('a',{'aria-label':'Next'}).get('href')
    except AttributeError:
        break
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    cards = soup.find_all('div','jobsearch-SerpJobCard')
    
    for card in cards:
        record = get_record(card)
        records.append(record)


# In[32]:


len(records)


# In[33]:


## Putting it all together


# In[38]:


import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def get_url(position, location):
    """Generate a url from position and location"""
    template = 'https://in.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def get_record(card):
    """Extract Job Record from a single record"""
    atag = card.h2.a
    job_title = atag.get('title')
    job_url = 'https://www.indeed.com' + atag.get('href')
    company = card.find('span','company').text.strip()
    job_location = card.find('div', 'recJobLoc').get('data-rc-loc')
    job_summary = card.find('div','summary').text.strip()
    post_date = card.find('span','date').text
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        job_salary = card.find('span','salaryText').text.strip()
    except AttributeError:
        job_salary = ''
    
    record = (job_title, company, job_location, post_date, today, job_summary, job_salary )
    
    return record

def main(position, location):
    """Run the main program routine"""
    records = []
    url = get_url(position,location)
    print(url)
    
    # Extract the Job Data
    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text,'html.parser')
        cards = soup.find_all('div','jobsearch-SerpJobCard')
        
        for card in cards:
            record = get_record(card)
            records.append(record)

        try:
            url = 'https://in.indeed.com' + soup.find('a',{'aria-label':'Next'}).get('href')
        except AttributeError:
            break
      
    print(len(records))
    # Save the job data
    with open('results2.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['JobTitle','Company','Location','PostDate','ExtractDate','Summary', 'Salary', 'JobUrl'])
        writer.writerows(records)


# In[39]:


# run the main function


# In[41]:


main('developer', 'mumbai')

