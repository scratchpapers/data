#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


file = '2020MayHousingSales.xlsx'
df = pd.read_excel(file)


# ## Data Visualizations - Existing Single-Family Home
# 
# ### 1 - SF BAY AREA : Year to Year Median Sold Price (May-2019 / May-2020)
# ### 2 - SF BAY AREA : Year to Year Median Sold Price Change % (May-2019 / May-2020)
# ### 3 - SF BAY AREA : Year to Year % Change in Sales (May-2019 / May-2020)
# ### 4 - SF BAY AREA : Month to Month Median Sold Price (Apr-2020 / May-2020)
# ### 5 - SF BAY AREA : Month to Month Median Sold Price Change % (Apr-2020 / May-2020)
# ### 6 - SF BAY AREA : Month to Month Sales Change %  (Apr-2020 / May-2020)
# 
# ### 7 - SO CAL AREA : Year to Year Median Sold Price (May-2019 / May-2020)
# ### 8 - SO CAL AREA : Year to Year Median Sold Price Change % (May-2019 / May-2020)
# ### 9 - SO CAL AREA : Year to Year % Change in Sales (May-2019 / May-2020)
# ### 10 - SO CAL AREA : Month to Month Median Sold Price (Apr-2020 / May-2020)
# ### 11 - SO CAL AREA : Month to Month Median Sold Price Change % (Apr-2020 / May-2020)
# ### 12 - SO CAL AREA : Month to Month Sales Change %  (Apr-2020 / May-2020)

# ## SF BAY AREA DATA

# ### Setting up Pandas DataFrame

# In[4]:


dfSF = df.iloc[13:23]
dfSF = dfSF.dropna(axis=1)
dfSF.columns = dfSF.iloc[0]
dfSF = dfSF.drop(dfSF.index[0])


# In[5]:


dfSF


# In[6]:


dfSF.columns = 'SF Bay Area','2020-05-01','2020-04-03','2019-05-02','Price MTM % Chg','Price YTY % Chg','Sales MTM % Chg','Sales YTY % Chg'


# In[7]:


dfSF[['Price MTM % Chg', 'Price YTY % Chg','Sales MTM % Chg', 'Sales YTY % Chg']] = dfSF[['Price MTM % Chg', 'Price YTY % Chg','Sales MTM % Chg', 'Sales YTY % Chg']].applymap("{0:.2f}".format)


# In[8]:


dfSF.index = np.arange(1, len(dfSF)+1)


# In[9]:


dfSF['Price MTM % Chg'] = pd.to_numeric(dfSF['Price MTM % Chg'])
dfSF['Price YTY % Chg'] = pd.to_numeric(dfSF['Price YTY % Chg'])
dfSF['Sales MTM % Chg'] = pd.to_numeric(dfSF['Sales MTM % Chg'])
dfSF['Sales YTY % Chg'] = pd.to_numeric(dfSF['Sales YTY % Chg'])

dfSF.loc[:,'Price MTM % Chg'] = dfSF['Price MTM % Chg'] * 100
dfSF.loc[:,'Price YTY % Chg'] = dfSF['Price YTY % Chg'] * 100
dfSF.loc[:,'Sales MTM % Chg'] = dfSF['Sales MTM % Chg'] * 100
dfSF.loc[:,'Sales YTY % Chg'] = dfSF['Sales YTY % Chg'] * 100


# In[10]:


sfmediansoldprice = dfSF.loc[:,:'Price YTY % Chg']
sfmediansoldsales = dfSF.loc[:, 'Sales MTM % Chg':'Sales YTY % Chg']
sfheader = {'Median Sold Price $ of Existing Single-Family Homes':sfmediansoldprice, 'Number of Existing Single-Family Home Sales': sfmediansoldsales}


# In[11]:


dfSFcategory = pd.concat(sfheader.values(), axis=1, keys=sfheader.keys())


# In[34]:


dfSFcategorygory


# ### 1 - SF BAY AREA : Year to Year Median Sold Price (May-2019 / May-2020)

# In[13]:


May19Price = dfSF.loc[:,['SF Bay Area','2019-05-02']]
May20Price = dfSF.loc[:,['SF Bay Area','2020-05-01']]
YTYPriceDiff = pd.merge(May19Price,May20Price, how='inner',on=['SF Bay Area']).set_index('SF Bay Area').plot.bar(figsize=(13,6),cmap='Paired')
plt.title('Year to Year Median Sold Price of Existing Single Family Homes (May-2019 / May-2020)')
plt.ylabel('Median Sold Price ($)')
plt.xlabel('SF Bay Area')
plt.xticks(rotation='horizontal')


# ### 2 - SF BAY AREA : Year to Year Median Sold Price Change % (May-2019 / May-2020)

# In[14]:


dfSF[['Price YTY % Chg']] = dfSF[['Price YTY % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
sns.barplot(x='SF Bay Area',y='Price YTY % Chg', data=dfSF, palette="RdBu_r")
plt.title('Year to Year Price Change Percentage (%) in Existing Single-Family Homes (May-2019 / May-2020)')
plt.ylabel('YTY Price Change Percentage (%)')
plt.xlabel('SF Bay Area')


# ### 3 - SF BAY AREA : Year to Year % Change in Sales (May-2019 / May-2020)

# In[15]:


dfSF[['Sales YTY % Chg']] = dfSF[['Sales YTY % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
sns.barplot(x='SF Bay Area',y='Sales YTY % Chg', data=dfSF,palette="RdBu_r")
plt.title('Year to Year Percentage (%) Change in Number of Existing Single-Family Home Sales (May-2019 / May-2020)')
plt.ylabel('YTY Number of Sales % Change')
plt.xlabel('SF Bay Area')


# ### 4 - SF BAY AREA : Month to Month Median Sold Price (Apr-2020 / May-2020)

# In[16]:


Apr20Price = dfSF.loc[:,['SF Bay Area','2020-04-03']]
May20Price = dfSF.loc[:,['SF Bay Area','2020-05-01']]
MTMPriceDiff = pd.merge(Apr20Price,May20Price, how='inner',on=['SF Bay Area']).set_index('SF Bay Area').plot.bar(figsize=(13,6),cmap='Paired')
plt.ylabel('Median Sold Price ($)')
plt.title('Month to Month Median Sold Price of Existing Single-Family Homes (Apr-2020 / May-2020)')
plt.xlabel('SF Bay Area')
plt.xticks(rotation='horizontal')


# ### 5 - SF BAY AREA : Month to Month Median Sold Price Change % (Apr-2020 / May-2020)

# In[17]:


dfSF[['Price MTM % Chg']] = dfSF[['Price MTM % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
sns.barplot(x='SF Bay Area',y='Price MTM % Chg', data=dfSF,palette="RdBu_r")
plt.ylabel('MTM Price % Change')
plt.title('Month to Month Median Sold Price Change Percentage (%) of Existing Single Family Homes (Apr-2020 / May-2020)')
plt.xlabel('SF Bay Area')


# ### 6 - SF BAY AREA : Month to Month % Change Sales (Apr-2020 / May-2020)

# In[18]:


dfSF[['Sales MTM % Chg']] = dfSF[['Sales MTM % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
MTMperc = sns.barplot(x='SF Bay Area',y='Sales MTM % Chg', data=dfSF, palette="RdBu_r")
plt.title('Month to Month Percentage (%) Change in Number of Existing Single Family Homes Sales (Apr-2020 / May-2020)')
plt.ylabel('MTM Number of Sales % Change')
plt.xlabel('SF Bay Area')


# ## SOUTHERN CALIFORNIA DATA

# ### Setting up Pandas DataFrame

# In[19]:


dfSC = df[23:30]
dfSC = dfSC.dropna(axis=1)
dfSC.columns = dfSC.iloc[0]
dfSC = dfSC.drop(dfSC.index[0])


# In[20]:


dfSC


# In[21]:


dfSC.columns = 'So Cal Area','2020-05-01','2020-04-03','2019-05-02','Price MTM % Chg','Price YTY % Chg','Sales MTM % Chg','Sales YTY % Chg'


# In[22]:


dfSC[['Price MTM % Chg', 'Price YTY % Chg','Sales MTM % Chg', 'Sales YTY % Chg']] = dfSC[['Price MTM % Chg', 'Price YTY % Chg','Sales MTM % Chg', 'Sales YTY % Chg']].applymap("{0:.2f}".format)


# In[23]:


dfSC.index = np.arange(1, len(dfSC)+1)


# In[24]:


dfSC['Price MTM % Chg'] = pd.to_numeric(dfSC['Price MTM % Chg'])
dfSC['Price YTY % Chg'] = pd.to_numeric(dfSC['Price YTY % Chg'])
dfSC['Sales MTM % Chg'] = pd.to_numeric(dfSC['Sales MTM % Chg'])
dfSC['Sales YTY % Chg'] = pd.to_numeric(dfSC['Sales YTY % Chg'])

dfSC.loc[:,'Price MTM % Chg'] = dfSC['Price MTM % Chg'] * 100
dfSC.loc[:,'Price YTY % Chg'] = dfSC['Price YTY % Chg'] * 100
dfSC.loc[:,'Sales MTM % Chg'] = dfSC['Sales MTM % Chg'] * 100
dfSC.loc[:,'Sales YTY % Chg'] = dfSC['Sales YTY % Chg'] * 100


# In[25]:


scmediansoldprice = dfSC.loc[:,:'Price YTY % Chg']
scmediansoldsales = dfSC.loc[:, 'Sales MTM % Chg':'Sales YTY % Chg']
scheader = {'Median Sold Price $ of Existing Single-Family Homes':scmediansoldprice, 'Number of Existing Single-Family Home Sales': scmediansoldsales}


# In[26]:


dfSCcategory = pd.concat(scheader.values(), axis=1, keys=scheader.keys())


# In[27]:


dfSCcategory


# ### 7 - SO CAL AREA : Year to Year Median Sold Price (May-2019 / May-2020)

# In[28]:


May19Price = dfSC.loc[:,['So Cal Area','2019-05-02']]
May20Price = dfSC.loc[:,['So Cal Area','2020-05-01']]
YTYPriceDiff = pd.merge(May19Price,May20Price, how='inner',on=['So Cal Area']).set_index('So Cal Area').plot.bar(figsize=(13,6),cmap='Paired')
plt.title('Year to Year Median Sold Price of Existing Single Family Homes (May-2019 / May-2020)')
plt.ylabel('Median Sold Price ($)')
plt.xlabel('So Cal Area')
plt.xticks(rotation='horizontal')


# ### 8 - SO CAL AREA : Year to Year Median Sold Price Change % (May-2019 / May-2020)

# In[29]:


dfSC[['Price YTY % Chg']] = dfSC[['Price YTY % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
sns.barplot(x='So Cal Area',y='Price YTY % Chg', data=dfSC, palette="RdBu_r")
plt.title('Year to Year Price Change Percentage (%) in Existing Single-Family Homes (May-2019 / May-2020)')
plt.ylabel('YTY Price Change Percentage (%)')
plt.xlabel('So Cal Area')


# ### 9 - SO CAL AREA : Year to Year % Change in Sales (May-2019 / May-2020)

# In[30]:


dfSC[['Sales YTY % Chg']] = dfSC[['Sales YTY % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
sns.barplot(x='So Cal Area',y='Sales YTY % Chg', data=dfSC,palette="RdBu_r")
plt.title('Year to Year Percentage (%) Change in Number of Existing Single-Family Home Sales (May-2019 / May-2020)')
plt.ylabel('YTY Number of Sales % Change')
plt.xlabel('So Cal Area')


# ### 10 - SO CAL AREA : Month to Month Median Sold Price (Apr-2020 / May-2020)

# In[31]:


Apr20Price = dfSC.loc[:,['So Cal Area','2020-04-03']]
May20Price = dfSC.loc[:,['So Cal Area','2020-05-01']]
MTMPriceDiff = pd.merge(Apr20Price,May20Price, how='inner',on=['So Cal Area']).set_index('So Cal Area').plot.bar(figsize=(13,6),cmap='Paired')
plt.ylabel('Median Sold Price ($)')
plt.title('Month to Month Median Sold Price of Existing Single-Family Homes (Apr-2020 / May-2020)')
plt.xlabel('So Cal Area')
plt.xticks(rotation='horizontal')


# ### 11 - SO CAL AREA : Month to Month Median Sold Price Change % (Apr-2020 / May-2020)

# In[32]:


dfSC[['Price MTM % Chg']] = dfSC[['Price MTM % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
sns.barplot(x='So Cal Area',y='Price MTM % Chg', data=dfSC,palette="RdBu_r")
plt.ylabel('MTM Price % Change')
plt.title('Month to Month Median Sold Price Change Percentage (%) of Existing Single-Family Homes (Apr-2020 / May-2020)')
plt.xlabel('So Cal Area')


# ### 12 - SO CAL AREA : Month to Month Sales Change %  (Apr-2020 / May-2020)

# In[33]:


dfSC[['Sales MTM % Chg']] = dfSC[['Sales MTM % Chg']].astype(float)
fig = plt.figure(figsize=(13,6))
MTMperc = sns.barplot(x='So Cal Area',y='Sales MTM % Chg', data=dfSC, palette="RdBu_r")
plt.title('Month to Month Percentage (%) Change in Number of Existing Single-Family Homes Sales (Apr-2020 / May-2020)')
plt.ylabel('MTM Number of Sales % Change')
plt.xlabel('So Cal Area')

