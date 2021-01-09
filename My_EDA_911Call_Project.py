#!/usr/bin/env python
# coding: utf-8

# # 911 Calls Capstone Project
# 
# 

# For this capstone project we will be analyzing some 911 call data from Kaggle. The data contains the following fields:

# - lat : String variable, Latitude
# - lng: String variable, Longitude
# - desc: String variable, Description of the Emergency Call
# - zip: String variable, Zipcode
# - title: String variable, Title
# - timeStamp: String variable, YYYY-MM-DD HH:MM:SS
# - twp: String variable, Township
# - addr: String variable, Address
# - e: String variable, Dummy variable (always 1)

# # Data and Setup

# 1)Import numpy and pandas

# In[7]:


#By using import we import the libraries of numpy and pandas and creating alias with standard alias name np and pd 
import numpy as np
import pandas as pd


# 2)Import visualization libraries and set %matplotlib inline.

# In[8]:


#There are two visualization libraries matplotlib and seaborn in python these we have imported here
#using %matplotlib inline is used to set the o/p of backend matplotlib of plotting commands to display inline within frontends

import matplotlib.pyplot as plt
import seaborn as sns

get_ipython().run_line_magic('matplotlib', 'inline')


# 3)Read in the csv file as a dataframe called df

# In[9]:


#using pandas lib we have read the csv file as a called dataframe df.

# As,e: String variable, Dummy variable we don't need it here we drop the column
#drop command in df is used to drop the unecessary column where 'e' is column name.
#axis=1 is used to specify we are dropping the column and not the row.
#inplace=True specifies the operation would work on the original object. 

#df.head(5) is used to display data of first five rows.

df=pd.read_csv("C:\\Users\\AMAN BIRADAR\\Downloads\\Python\\Call Dataset.csv")
df.drop('e',axis=1,inplace=True)
df.head(5)


# 4)Check the info() of the df

# In[10]:


# It is observe that zip,twp,addr have some missing values.
#df.info() displays the data,column name,count of values in the columnn and datatype
df.info()


# 5)Check the head of df

# In[11]:


#df.head(5) is used to display data of first five rows of the dataset.
df.head(5)


# # #Basic Questions

# 6)What are the top 5 zipcodes for 911 calls?

# In[12]:


# To find top 5 zip code from where calls are usually done
df['zip'].value_counts().head(5)


# 7)What are the top 5 townships (twp) for 911 calls?

# In[13]:


#count the datset for every class in the column twp for the datset
df['twp'].value_counts().head(5)


# 8)Take a look at the 'title' column, how many unique title codes are there?

# In[14]:


#gives no of unique count for the column mention for the dataset
df['title'].nunique()


# ## Creating new features

# 9)In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.
# For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS. *

# In[15]:


# Adding column Reason using split we split the value from column title and display only intial value
df['Reason']=df['title'].apply(lambda x:x.split(':')[0])
df.head(5)


# 10)What is the most common Reason for a 911 call based off of this new column?

# In[16]:


#count the datset for every class in the column Reason for the datset
#we have see the countof calls are higher for EMS and less for Fire 
df['Reason'].value_counts()


# 11)Now use seaborn to create a countplot of 911 calls by Reason

# In[17]:


sns.countplot(x='Reason',data= df)
#EMS calls are more as compair to other services.
#Traffic
#Fire


# 12)Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column? 

# In[18]:


#prints the type and time value for timeStamp column
print(type(df['timeStamp'][0]))
print(df['timeStamp'][0])


# 13)You should have seen that these timestamps are still strings. Use pd.to_datetime to convert the column from strings to DateTime objects. **

# In[19]:


#pd.to_datetime we can convert the time value in standard time format
df['timeStamp']=pd.to_datetime(df['timeStamp'])
print(type(df['timeStamp'][0]))
print(df['timeStamp'][0])


# 14)You can now grab specific attributes from a Datetime object by calling them. For example:*
#    
#    time = df['timeStamp'].iloc[0]
#    
#    time.hour
#    
#    You can use Jupyter's tab method to explore the various attributes you can call. Now that the timestamp column are actually DateTime objects, use .apply() to create 3 new columns called Hour, Month, and Day of Week. You will create these columns based off of the timeStamp column

# In[20]:


#iloc is used to locate the value
time=df['timeStamp'].iloc[0]
time.hour


# In[21]:


#Hour,Month,Day of Week are new columns we have created by extracting value from timeStamp column
df['Hour']=df['timeStamp'].apply(lambda x:x.hour)
df['Month']=df['timeStamp'].apply(lambda x:x.month)
df['Day of Week']=df['timeStamp'].apply(lambda x:x.dayofweek)
df.head(5)


# 15)Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week: **
# dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

# In[22]:


#.map is used to map the values from the mentioned dictionary
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day of Week']=df['Day of Week'].map(dmap)
df.head(5)


# 16)Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column. **

# In[23]:


#Using Seaborn the plot is plotted 
#day of week on x-axis and count of call on for Reasond on y-axis
#Observed that For Fire Service calls are moderate for all days but there changes in EMS and Traffic call

sns.countplot(x='Day of Week',hue='Reason',data=df)
plt.legend(bbox_to_anchor=(1,1))


# 17)Now do the same for Month:

# In[24]:


#Using Seaborn the plot is plotted 
#month on x-axis and count of call on for Reasond on y-axis
#Observed that For All Services the calls are almost less from 7th month to end of month than other month
sns.countplot(x='Month',hue='Reason',data=df)
plt.legend(bbox_to_anchor=(1.3,1))


# Did you notice something strange about the Plot?

# You should have noticed it was missing some Months, let's see if we can maybe fill in this information by plotting the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, we'll need to do some work with pandas... 

# 18)Now create a gropuby object called byMonth, where you group the DataFrame by the month column and use the count() method for aggregation. Use the head() method on this returned DataFrame. **

# In[25]:


#all he values are grouped by month
byMonth=df.groupby('Month').count()
byMonth


# 19)Now create a simple plot off of the dataframe indicating the count of calls per month.

# In[26]:


#Using matplotlib we have plotted below plot where we have month on x-axis and count on y-axis
#count for 8 to 12 months are low and for 1st month is highest 
byMonth['lat'].plot()


# 20)Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. Keep in mind you may need to reset the index to a column.

# In[27]:


#Using seaborn below plot is plotted
#month on x-axis and twp is on y-axis


sns.lmplot(x='Month',y='twp',data=byMonth.reset_index())


# 21)Create a new column called 'Date' that contains the date from the timeStamp column. You'll need to use apply along with the .date() method. 

# In[28]:


#date new column is added ectratcing value of date from timeStamp column
df['Date']=df.timeStamp.apply(lambda x:x.date())
df.head(5)


# 22)Now let's move on to creating heatmaps with seaborn and our data. We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week. There are lots of ways to do this, but I would recommend trying to combine groupby with an unstack method. Reference the solutions if you get stuck on this!*

# In[29]:


#Day of Week is index for datset and Hours are column
#So,with we can observe the count of call on daily basis and hour basis
dayHour = df.groupby(['Day of Week','Hour']).count()['lat'].unstack()
dayHour


# 23)Now create a HeatMap using this new DataFrame

# In[30]:


#Using seborn heatmap is plotted
#Hours on x-axis and Day of Week on y-axis
#observed from below heatmap that count for 0 to 6 hours are too less than further hours
#Week wise Sat,Sun we have count less 
plt.figure(figsize=(10,8))
sns.heatmap(dayHour)


# 24)Now create a clustermap using this DataFrame.

# In[31]:


#Using seborn clustermap is plotted
#Hours on x-axis and Day of Week on y-axis
#observed from below clustermap gives more laborated plot
#0,5,1,4,2,3,6,23 these are sequenced according to the lowest to low call count for hours
plt.figure(figsize=(10,8))
sns.clustermap(dayHour)


# 25)Now repeat these same plots and operations, for a DataFrame that shows the Month as the column.

# In[32]:


#displayed column by month count for dataset 
Month=df.groupby(['Day of Week','Month']).count()['lat'].unstack()
Month


# In[33]:


#Using seborn heatmap is plotted
#Month on x-axis and Day of Week on y-axis
#8 to 12 month we see call count is too less than other months and Sat,Sun call are count is less than other days
plt.figure(figsize=(10,8))
sns.heatmap(Month)


# In[34]:


#Using seborn clustermap is plotted
#Month on x-axis and Day of Week on y-axis
#using clustermap we observe that calls for 8,12 -month is less than other months 
#Sat,Sun is less in Day of Week otherthan 1,4,7 months
plt.figure(figsize=(8,8))
sns.clustermap(Month)

