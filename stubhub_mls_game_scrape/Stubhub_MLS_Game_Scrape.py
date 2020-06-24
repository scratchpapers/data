#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
import pandas as pd
import datetime
from datetime import datetime as dt
import itertools
import pdfkit


# In[2]:


"""Setting up Chrome webdriver"""
driver = webdriver.Chrome()


# In[3]:


"""LA Galaxy, LAFC, DC, and San Jose urls"""
domain = 'https://www.stubhub.com/'
urls = ['la-galaxy-tickets/performer/12587/',
        'lafc-tickets/performer/100275569/',
        'dc-united-tickets/performer/23188/',
        'san-jose-earthquakes-tickets/performer/143/']
data = []


# In[4]:


"""Going through each url and scraping data"""
for url in urls:
    driver.get(domain+url)
    
    """If there is 'See More Events tab on bottom to show more games, click. Otherwise, continue"""
    try:
        more = driver.find_element_by_class_name('EventListPanel__Footer')
        if more:
            more.click()
    except:
        pass
    
    """Creating content variable to store the information into"""
    content = driver.find_elements_by_class_name('EventItem__Body')
    
    """Collecting all the info for listed games"""


    for info in content:

        details = info.find_element_by_class_name('EventItem__Details')
        day = info.find_element_by_class_name('DateStamp__Day').text
        date = info.find_element_by_class_name('DateStamp__MonthDate').text
        gameinfo = details.find_element_by_tag_name('a')
        state = details.find_element_by_class_name('EventItem__MixInfo').text.split()
        
#         Turning Date into DateTime
        gamedatetime = datetime.datetime.strptime(date,'%b %d')
        gamedate = gamedatetime.strftime('%m-%d-'+str(dt.today().year))
        

        """If time is TBD (To be determined), which is basically all the Parking Pass tabs"""
        if state[0] == 'TBD':
            time = ' '.join(state[0:1])
            city = ' '.join(state[6:])
            venue = details.find_element_by_class_name('EventItem__VenueInfo').text

        else:
            time = ' '.join(state[0:2])
            venue = details.find_element_by_class_name('EventItem__VenueInfo').text
            
        """Getting the Home Team"""
        away = gameinfo.text.split(' at')[0]

        """Getting the Away Team"""
        home = gameinfo.text.split('at ')[1]

        """Show how much the ticket prices start from, and how many tickets are left if available"""
    #     Lowest Price tickets start from
        try:
            tickets = details.find_element_by_class_name("EventItem__Price").text
        except:
            pass

    #     If available, how many tickets are left at the listed price
        try:
            ticksleft = info.find_element_by_class_name("EventItem__Urgency").text
        except:
            pass

        """Grab the links for each games that will take you to ticket purchase for each game. **Optional**"""
        link = details.find_element_by_class_name('EventItem__TitleLink')
        link_url = link.get_attribute('href')

        data.append([day, home, away, gamedate, gameinfo.text, time, venue, tickets, link_url])
        
        


# In[5]:


data.sort()


# In[6]:


# There are duplicates since one team shows a game with another team and vice versa. Removing Duplicates


# In[7]:


data_dedupe = list(k for k, _ in itertools.groupby(data))


# In[8]:


columns = ['Day', 'Home','Away', 'GameDate','GameName', 'GameTime','Venue','LowestTicket','TicketLink']


# In[9]:


# Creating a DataFrame


# In[10]:


dataframe = pd.DataFrame(data_dedupe, columns=columns).sort_values(by=['GameDate'], ascending=True)


# In[11]:


df = dataframe.reset_index(drop=True)


# In[12]:


# Sorted table by Game Date (descending) and reset the index so it can be exported to Excel / CSV / PDF


# In[13]:


# Export to Excel
df.to_excel("MLS_Games_Excel.xlsx")


# In[14]:


# Export to CSV
df.to_csv("MLS_Games_CSV.csv")


# In[ ]:




