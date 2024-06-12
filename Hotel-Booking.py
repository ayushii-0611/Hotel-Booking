#!/usr/bin/env python
# coding: utf-8

# #Buisness Problem:
# In recent years,City Hotel and Resort Hotel have seen high cancellation rates.Each hotel is now dealing with a number of issues as a result,including fewer revenues and less tahn ideal room use.Consequently ,lowering cancellations rates is both hotels primary goal in oredr to incraese their efficiency in generating revenue.

# In[43]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# In[2]:


df=pd.read_csv("hotel_bookings 2.csv ")
df.head()


# In[3]:


df.tail()


# In[5]:


df.shape


# In[6]:


df.info()


# In[12]:


df['reservation_status_date'] = pd.to_datetime(df[ 'reservation_status_date'])


# In[13]:


df.describe(include='object')


# In[15]:


for col in df.describe(include='object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[16]:


df.isnull().sum()


# In[17]:


df.drop(['company','agent'],axis=1,inplace=True)
df.dropna(inplace=True)


# In[18]:


df.isnull().sum()


# In[19]:


df.describe()


# In[20]:


df['adr'].plot(kind='box')


# In[21]:


df=df[df['adr']<5000]


# # Data Analysis and Visualization

# In[26]:


cancelled_perc=df['is_canceled'].value_counts(normalize=True)
print(cancelled_perc)

plt.figure(figsize=(5,4))
plt.title('Reservation Status Count')
plt.bar(['Not cancelled','cancelled'],df['is_canceled'].value_counts(),edgecolor='k',width=0.7)
plt.show()


# The accompanying bar graph shows the percentage of reservations that are cancelled and those that are not.It is obvious that there are still a significant number of reservations that have not been canceled.There are still 37% of clients who cancelled their reservation,ehich has a significant impact on the hotels earnings.

# In[30]:


plt.figure(figsize=(8,4))
ax1=sns.countplot(x='hotel',hue='is_canceled',data=df,palette='Blues')
legend_labels,_=ax1. get_legend_handles_labels()
plt.title('Reservation Status in Different Hotels',size=20)
plt.xlabel('hotel')
plt.ylabel(['not canceled','canceled'])
plt.show()


# #The line graph above shows that,on certain days,the average daily rate for a city hotel is less than that of a resort hotel,and on other days it is even less.It goes without saying that weekends and holidays may see a rise in resort hotel rates.

# In[31]:


resort_hotel=df[df['hotel']=='Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize=True)


# In[34]:


city_hotel=df[df['hotel']=='City Hotel']
city_hotel['is_canceled'].value_counts(normalize=True)


# In[35]:


resort_hotel=resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel=city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[38]:


plt.figure(figsize=(20,8))
plt.title("Average Daily Rate in City and Resort Hotel",fontsize=30)
plt.plot(resort_hotel.index,resort_hotel['adr'],label='Resort Hotel')
plt.plot(city_hotel.index,city_hotel['adr'],label='City Hotel')
plt.legend(fontsize=20)
plt.show()


# In[44]:


df['month']=df['reservation_status_date'].dt.month
plt.figure(figsize=(16,8))
ax1=sns.countplot(x='month',hue='is_canceled',data=df,palette='bright')
legend_labels,_=ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation Status Month',size=20)
plt.xlabel('month')
plt.ylabel(['number of reservations'])
plt.legend(['not canceled','canceled'])
plt.show()


# #We have developed the grouped bar graph to analyze the months with the highest and lowest reservation levels according to reservation status.As can be seen,both the number of confirmed reservations and the number of cancelled reservation are largest in the month of August,whereas January is the month with the most canceled reservations.

# In[46]:


plt.figure(figsize=(16,8))
plt.title('ADR per Month',size=30)
sns.barplot('month','adr',data=df[df['is_canceled']==1].groupby('month')[['adr']].sum().reset_index())
plt.show()


# #This bar graph demonstrates that cancellations are most common when prices are greatest and are least common when they are lowest.Therefore,the cost of the accomodation is solely responsible for the cancellation.

# In[47]:


cancelled_data=df[df['is_canceled']==1]
top_10_country=cancelled_data['country'].value_counts()[:10]
plt.figure(figsize=(8,8))
plt.title('Top 10 Countries with Reservation Canceled')
plt.pie(top_10_country,autopct='%.2f',labels=top_10_country.index)
plt.show()


# #Pie chart shows the highest number of cancellations,Portugal has the highest number of cancellations

# In[48]:


df['market_segment'].value_counts()


# In[49]:


df['market_segment'].value_counts(normalize=True)


# In[50]:


cancelled_data['market_segment'].value_counts(normalize=True)


# #Around 46% of the clients come from online travel agencies,whereas 27% come from groups.Only 4% of clients book hotels directly by visiting them and making reservations.

# In[53]:


cancelled_df_adr=cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace=True)
cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

not_cancelled_data=df[df['is_canceled']==0]
not_cancelled_df_adr=not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace=True)
not_cancelled_df_adr.sort_values('reservation_status_date',inplace=True)

plt.figure(figsize=(20,6))
plt.title("Average Daily Rate")
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label='not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label='cancelled')
plt.legend()


# In[54]:


cancelled_df_adr=cancelled_df_adr[(cancelled_df_adr['not_cancelled_df_adr']>'2016')&(cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr=not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016')&(not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[55]:


plt.figure(figsize=(20,8))
plt.title("Average Daily Rate",fontsize=30)

plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label='not_cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'],label='cancelled')

plt.legend(fontsize=20)
plt.show()


# #As seen in the above graph,reservations are cancelled when the average daily rate is higher than when it is not canceled.It is clearly proves all the above analysis,that the higher price leads to higher cancelation.

# # Suggestions

# #1. Cancellation rates rise as the price does.In order to prevent cancellations of reservations,hotel could work on their pricing strategies and try to lower the rates for specific locations,can also provide discounts to customers
# 
# #2. As the ratio of the cancellation and not cancellation of the resort hotel is higher in the resort hotel than the city hotels,so the hotels should provide a reasonable discount on the room prices on weekends or on holidays.
# 
# #3.In the month jan ,hotels can start campaigns or marketing with a reasonable amount to incraese thier revenue as cancellation rate is higher in this month.
# 
# #4.They can also increase the quality of their hotel and services maily in Portugal to reduce the cancellation rate
