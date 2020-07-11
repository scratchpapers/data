#!/usr/bin/env python
# coding: utf-8

# In[457]:


from bs4 import BeautifulSoup as bs
from urllib.request import urlopen 
import pandas as pd
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt


# # Scrape Data from ESPN NBA Standings 2019-2020 using BeautifulSoup 
# 

# ### There are 2 URLs ( Both imported into Pandas and concatenated)
# #### 1. First is Regular Standings stats (url)
# #### 2. Second is the Expanded stats (url1)

# ### 1 - Regular Stats (Standings tab)

# In[458]:


url = 'http://www.espn.com/nba/standings/_/group/league'


# In[459]:


page = urlopen(url).read()
page_soup = bs(page,'html.parser')
table = page_soup.findAll('tbody',{'class':'Table__TBODY'})


# #### Getting Team Names 

# In[460]:


teamlink = table[0].find_all('div',{'class':'team-link'})
teaminfo = []

for team in teamlink:
    teamname = team.find('span',{'class':'hide-mobile'}).text
    teaminit = team.find('span',{'class':'show-mobile'}).text
    teaminfo.append([teamname, teaminit])


# #### Getting Stats for Each Team

# In[461]:


teamstat = []
statrows = table[1].findAll('tr',{'class':'Table__TR'}) #Stats Table with Individual Team stats
for statrow in statrows:
    row = statrow.findAll('td')
    won = row[0].text
    loss = row[1].text
    percent = row[2].text
    gamesbehind = row[3].text
    homerecord = row[4].text
    awayrecord = row[5].text
    divrecord = row[6].text
    confrecord = row[7].text
    ppg = row[8].text
    oppg = row[9].text
    diff = row[10].text
    winstreak = row[11].text
    last10 = row[12].text
    teamstat.append((won,loss,percent,gamesbehind,homerecord,awayrecord,
         divrecord,confrecord,ppg,oppg,diff,winstreak,last10))


# #### Combine Teaminfo and Teamstats to create single list for each team with Labels

# In[462]:


statlist =[]
for team,stats in zip(teaminfo,teamstat):
    statlist.append(team+list(stats))

labels = ['Team Name', 'Team Code', 'Win','Loss','% Win','Games Behind',
         'Home Record','Away Record','Division','Conference','PPG','Opp PPG',
         'PPG Difference','Win Streak','Last 10'] 


# ### Import data into Pandas DataFrame and clean

# In[463]:


df = pd.DataFrame(statlist,columns=labels)


# #### Changing 'Games Behind' value for Milwaukee Bucks from a String Value '-' into INT value '0'

# In[464]:


df.loc[0,('Games Behind')] = 0


# #### Turning String Values into INT, FLOAT and NUMERIC Values

# In[465]:


df[['Win','Loss']]=df[['Win','Loss']].astype(int)
df[['% Win','PPG','Opp PPG','Games Behind']] = df[['% Win','PPG','Opp PPG','Games Behind']].astype(float)
df['PPG Difference'] = pd.to_numeric(df['PPG Difference'])


# #### Turning decimals in % Win column into percentage out of 100

# In[466]:


df['% Win'] = df['% Win'] * 100


# In[495]:


df


# ### 2 - Expanded Stats. Scraping the data, importing into Pandas and cleaning data. 

# In[468]:


url1 = 'https://www.espn.com/nba/standings/_/group/league/view/expanded'


# In[469]:


page = urlopen(url1).read()
page_soup = bs(page,'html.parser')
table = page_soup.findAll('tbody',{'class':'Table__TBODY'})


# In[470]:


statrows = table[1].findAll('tr',{'class':'Table__TR'}) 


# In[471]:


teamlink = table[0].find_all('div',{'class':'team-link'})
teaminfo = []

for team in teamlink:
    teaminit = team.find('span',{'class':'show-mobile'}).text
    teaminfo.append([teaminit])


# In[472]:


teamstat1 = []
#Stats Table with Individual Team stats
statrows = table[1].findAll('tr',{'class':'Table__TR'}) 
for statrow in statrows:
    row = statrow.findAll('td')
    Game_3PT = row[4].text
    Game_10PT = row[5].text
    vs500above = row[6].text
    vs500below = row[7].text
    teamstat1.append((Game_3PT, Game_10PT, vs500above, vs500below))


# In[473]:


statlist1 =[]
for team,stats in zip(teaminfo,teamstat1):
    statlist1.append(team+list(stats))

labels1 = ['Team Code', '3 PT GAMES', '10 PT GAMES', 'VS. .500 And Above', 'VS. Below .500'] 


# #### Import data into Pandas dataframe and clean

# In[474]:


df1 = pd.DataFrame(statlist1,columns=labels1)


# ### Calculating and appending Win % for each column 
# #### * 3 PT GAMES = Record of games with final score difference of 3 points or less
# #### * 10 PT GAMES = Record of games with final score difference of 10 points or less
# #### * VS. .500 And Above = Record of games against teams with .500 average and above in season standing
# #### * VS. Below .500 = Record of games against teams with below .500 average in season standing

# In[475]:


games3 = df1['3 PT GAMES'].str.split('-', n=1, expand=True)
games10 = df1['10 PT GAMES'].str.split('-', n=1, expand=True)
vs500above = df1['VS. .500 And Above'].str.split('-', n=1, expand=True)
vs500below = df1['VS. Below .500'].str.split('-',n=1,expand=True)


# In[493]:


df1['3 PT GAMES % Won'] = round(games3[0].astype(int) *100 / (games3[0].astype(int)+games3[1].astype(int)),1)
df1['10 PT GAMES % Won'] = round(games10[0].astype(int) *100 / (games10[0].astype(int)+games10[1].astype(int)),1)
df1['VS .500 And Above % Won'] = round(vs500above[0].astype(int)*100 / (vs500above[0].astype(int)+vs500above[1].astype(int)),1)
df1['VS Below .500 % Won'] = round(vs500below[0].astype(int)*100 / (vs500below[0].astype(int)+vs500below[1].astype(int)),1)


# In[494]:


df1 = df1[['Team Code','3 PT GAMES','3 PT GAMES % Won','10 PT GAMES','10 PT GAMES % Won','VS. .500 And Above','VS .500 And Above % Won','VS. .500 And Above','VS Below .500 % Won']]


# In[478]:


df1.head()


# ### Combining both dataframe into one. Using Merge and Join to concatenate

# In[479]:


result = pd.merge(df, df1, on='Team Code', how='inner')


# In[492]:


result


# ### Checking some stats and getting the list of column names in dataframe to see what we can work with

# In[481]:


result.describe()


# ### Looks like we can work with these as they are numerical values

# In[482]:


finaldf = result[['Team Name', 'Team Code','Win', 'Loss','% Win','Games Behind','PPG','Opp PPG','PPG Difference','3 PT GAMES % Won','10 PT GAMES % Won','VS .500 And Above % Won','VS Below .500 % Won']].set_index('Team Code')


# In[483]:


finaldf


# ## Using Seaborn to Plot Relationship Between Stats
# ### Seaborn Bar Plot showing Team Code and Winning Percentage with Horizontal Line showing 50% winning threshold

# In[484]:


teams = [i.split(' ')[-1] for i in finaldf['Team Name']]


# In[485]:


finaldf.index.name


# In[486]:


fig = plt.figure(figsize=(20,10))
plt.xticks(rotation=75)
plt.rcParams['axes.labelsize'] = 40
plt.title("2019-20 NBA Standings with 50% Winning percentage line", size=24)
sns.set(style="whitegrid")
sns.barplot(data=finaldf, x=finaldf.index,y='% Win', palette='Paired').axhline(50)


# ### According to the current standings, there are 13 teams who has 50% and above winning percentage

# ## 1) What is the relationship between Team Win % and 3 PT Games % Win? 
# ### - How do teams with high % win do in very close games where game is decided by 3 points or less?
# ### - How important is the winning those very close games?

# In[487]:


fig = plt.figure(figsize=(9,10))
s = finaldf['Win']
plt.title("Team's season Win % vs 3 PT or less games Won %", size=24)
plt.rcParams['axes.labelsize'] = 40
ax = sns.scatterplot(x="% Win", y="3 PT GAMES % Won", data=finaldf, hue=finaldf.index, size=s, sizes=(40,300))
ax.legend(loc='center left', bbox_to_anchor=(1.25,0.5), ncol=1)
for line in range(0,len(finaldf['Team Name'])):
     ax.text(finaldf['% Win'][line]+0.01, finaldf['3 PT GAMES % Won'][line], 
     finaldf.index[line], horizontalalignment='left', 
     size='medium', color='black', weight='semibold')


# ### This scatterplot shows that the teams with higher season win % has overall higher close game winning percentage. Although there are cases of teams with high close game win percentage, the trend shows that better teams tend to win more close games. 
# 
# ### In addition, teams with around 70% or more win percentage wins 60% or more on all close games decided within 3 points. Since close games tend to have some luck involved, one can say that if the conditions were slightly changed, these winning teams could end up having a losing record very easily. 

# ## 2) How about games where the final score is within 10 points?

# In[488]:


fig = plt.figure(figsize=(9,10))
s=finaldf['Win']
plt.rcParams['axes.labelsize'] = 20
plt.title("Team's season Win % vs 10 PT or less games Won %", size=24)
ax = sns.scatterplot(x="% Win", y="10 PT GAMES % Won", data=finaldf, hue=finaldf.index, size=s, sizes=(40,300))
ax.legend(loc='center left', bbox_to_anchor=(1.25,0.5), ncol=1)
for line in range(0,len(finaldf['Team Name'])):
     ax.text(finaldf['% Win'][line]+0.01, finaldf['10 PT GAMES % Won'][line], 
     finaldf.index[line], horizontalalignment='left', 
     size='small', color='black', weight='semibold')


# ### This plot shows the relationship between Season Win % and Winning % of games where it was decided by 10 points or less. The size of the bubble is determined by the Win column, the more wins a team has the bigger the bubble.
# 
# #### It shows that teams with 50% or more season win percentage, win 55% or more of all the games where it's several possession

# ## 3) Is there a relationship between points per game scored vs Win %?
# 
# ### Some teams can play some games really well by scoring high but lose more games by scoring much less points. This would show the team has high points per game but its Win % would be low

# In[489]:


fig = plt.figure(figsize=(9,10))
plt.rcParams['axes.labelsize'] = 25
ax = sns.regplot(x="PPG Difference", y="% Win", marker='+', data=finaldf, scatter_kws={"color":'green'}, line_kws={'color':'blue'})
plt.title("Points Per Game Difference (PPG Difference) vs Season Win %", size=24)
for line in range(0,len(finaldf['Team Name'])):
     ax.text(finaldf['PPG Difference'][line]+0.01, finaldf['% Win'][line], 
     finaldf.index[line], horizontalalignment='left', 
     size='medium', color='black', weight='semibold')


# ### This Regression plot shows a Linear relationship between a team's season Win % vs season average Points Per Game differences (PPG Difference)
# #### * This shows that teams with higher % of season win on average win by a higher margin of score on each game
# #### * It also shows that teams that have around 50% season Win % lose only by a margin of 1.5 points or less. The teams in this part of the chart has a high chance of improving their season next year. 

# ### This project was done to show my abilities in using Python, BeautifulSoup, and Pandas. 

# ## 1) Data was scraped from ESPN using BeautifulSoup and Python
# ## 2) Data was imported into Pandas and cleaned
# ## 3) Using Seaborn, various data analysis was made in addition to creating plots such as Scatterplot and Regression plot
# 

# ## Further analysis can be done using this dataset but this project was just to show a sample of work that can be done. Interesting project would be to scrape all player data or gameplay data and doing further analysis. Machine Learning can be used to predict what kind of attributes will give an insight into how a player will play in the future
