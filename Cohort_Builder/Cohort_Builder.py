
import openpyxl
import psycopg2
import pandas as pd
import os
import os.path
from datetime import date, timedelta
import datetime
from twilio.rest import Client
import sys


id = 'id#'
token = 'token#'
twilio = 'twilio_number'
twilioClient = Client(id, token)
jy = 'my_number'


# sql connection
hostname = 'hostname_of_database'
username = 'username'
password = 'password'
database = 'database'
port = 1234


# open sql connection and create cursor
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
cur = myConnection.cursor()


today = date.today()
now = datetime.datetime.now()


# OneDrive Folder Location
loc = "folder_location"


# running 'cohort_builder' query and importing it into pandas, turning account_number into integer to join

query = "select * from tablename where condition"
# Importing the resulting SQL query into Pandas using read_sql
info = pd.read_sql(query, con=myConnection)
info['customer_id'] = info['customer_id'].astype(int)

# OneDrive Folder
# Getting the list of files in the folder that end with .csv and does not have '-info' in name since this means the file has been worked on already
filelist = [x.name for x in list(os.scandir(loc)) if x.is_file() and '.csv' in x.name and '-info' not in x.name]

global kerror
global kperror
global kverror
kerror = 0
kperror = 0
kverror = 0

# Using PANDAS to clean up and organize data
for file in filelist:
    try:
        name = file.split('.')[0]

        # reading the csv
        df = pd.read_csv(str(loc)+str(file))

        # drop all columns after first one and rename it 'accounts'
        df.drop(df.columns[1:], axis=1, inplace=True)
        df.columns = ['customer_id']

        # for each row in accounts, split the account_numbers by a comma, then strip the blank spaces and add it to a new list
        newlists = []

        df1 = df.iloc[:, :1]
        df1.drop_duplicates(subset='customer_id', inplace=True)
        df2 = df1['customer_id'].astype(str).tolist()

        for row in df2:
            if ',' in row:
                for each in row.split(','):
                    newlists.append(each.strip())
            else:
                newlists.append(row)

        # stack the list into a column, pick unique accounts_numbers, turn it into a dataframe, drop the newly created index
        new_df = pd.DataFrame(pd.DataFrame(newlists).stack().unique()).reset_index(drop=True)

        # rename the column as 'accounts' and turn the column account_numbers into integers to join to info
        # and creating a dataframe with unique accounts

        new_df.columns = ['customer_id']

        new_df['customer_id'] = new_df['customer_id'].astype(str)

        new_df.replace(r'nan', '0', regex=True, inplace=True)

        new_df['customer_id'] = new_df['customer_id'].apply(int)

        new_dfs = new_df[['customer_id']].copy()

        new_dfs.drop_duplicates(subset='customer_id', inplace=True)

        # merge (left-join) the unique account_number dataframe with the info dataframe from the cohort builder then sort
        df3 = pd.merge(new_dfs, info, left_on='customer_id', right_on='customer_id', how='left')
        df4 = df3[['customer_id', 'email', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zip', 'phone']]

        # getting dataframes with null and permissions (email permission & unsubscribe)
        dfnull = df4[df4['email'].isnull()]
        dfnoperm = df4[(df4['email'] == 'EMAIL - UNSUBSCRIBED') | (df4['email'] == 'EMAIL -  NO PERMISSION')]
        dfreg = df4[(df4['email'].notnull()) & (df4['email'] != 'EMAIL - UNSUBSCRIBED') & (df4['email'] != 'EMAIL -  NO PERMISSION')]

        # modifying regular email dataframe to rank it by having address_number then the accounts
        dfreg['addressnumber'] = dfreg['address1'].str.extract(r'(\d+)')
        dfreg['addressnumber'].fillna(99999, inplace=True)
        dfreg['addressnumber'] = dfreg['addressnumber'].astype(int)

        dfreg['rank'] = dfreg.groupby('email')['addressnumber'].rank(ascending=True, method='dense')
        dfreg['rank1'] = dfreg.groupby('email')['dp_customer_id'].rank(ascending=False, method='dense')

        dfregfiltered = dfreg[(dfreg['rank1'] == 1) & (dfreg['rank'] == 1)]
        dfregfiltered.drop(['rank', 'rank1', 'addressnumber'], axis=1, inplace=True)
        dfregfiltered = dfregfiltered.sort_values(by='email')

        # combining all the separate dataframes into one, replacing nulls and blank spaces with 'N/A'
        dfall = pd.concat([dfregfiltered, dfnoperm, dfnull])
        dfall.fillna('N / A', inplace=True)
        dfall.replace(r'^\s*$', 'N / A', regex=True, inplace=True)

        # sending it to excel and removing the old file
        dfall.to_excel(loc+name+'-info.xlsx', index=False)
        os.remove(loc+file)

    except PermissionError:
        # Alert when the file can't be removed because someone has the file opened
        kperror += 1

    except ValueError:
        # Alert when the file has non-numeric value for account_numbers
        kverror += 1

    except:
        # Alert when info append is not working and there are csv files in the folder by sending a text message
        kerror += 1


# ERROR TEXT MESSAGES
# Split up the errors into 2. First is when File is Opened and unable to be removed: Permission Error (permerror).
# Second is some other error in the system. Need to investigate further.

# Case 1: When Cohort Builder is working but unable to remove because the file is opened by someone or account number column has non-numeric entries
if kerror == 0 and (kverror > 0 or kperror > 0):
    contents = ("The Cohort is working: " + str(kperror) + " Opened / Unable to Remove csv file(s) and " +
                str(kverror) + " file(s) containing non-numeric account_id number. " + now.strftime("%Y-%m-%d %H:%M") + ".")

    message = twilioClient.messages.create(body=contents, from_=twilio, to=jy)

# Case 2 : When Cohort Builder is not working for some reason & not due to non-numeric account number or file being opened. Need to investigate
elif kerror > 0:
    contents = "The Cohort is not working right now. There are " + str(file) + " csv file(s) in the folder. Need to investigate. " + \
        now.strftime("%Y-%m-%d %H:%M") + "."
    message = twilioClient.messages.create(body=contents, from_=twilio, to=jy)

# commit sql changes and close cursor,connection
cur.close()
myConnection.commit()
myConnection.close()
