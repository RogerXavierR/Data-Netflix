#!/usr/bin/env python
# coding: utf-8

# # Data Cleaning in Pandas | Python

# In[9]:


import pandas as pd


# In[84]:


# Replace the URL with the raw file URL on GitHub
url = 'https://raw.githubusercontent.com/RogerXavierR/Data-Netflix/main/netflix_titles.csv'
# Load data into a pandas DataFrame
df = pd.read_csv(url)

# Display the first few rows of the DataFrame to verify
df.head()


# ## Duplicates

# In[85]:


df = df.drop_duplicates()
df


# ## Unneded columns

# In[86]:


df =df.drop(columns= "description")
df


# ### Look into your data

# In[87]:


# Descriptive statistics
summary_stats = df.describe(include='all')

# Information about missing data
missing_info = df.info()

# Display the summary statistics and missing data information
print(summary_stats)
print(missing_info)


# ## Missing values

# In[88]:


# Count missing values in each column
missing_count = df.isnull().sum()

# Display the total number of missing values per column
print("Missing values count per column:")
print(missing_count)


# In[89]:


# examining missing values

print("Missing values distribution: ")

print(df.isnull().mean())
print("")


# ### Missing values : "director, cast, country, rating"

# In[90]:


# names of the columns
columns = ['director', 'cast', 'country', 'rating']

# looping through the columns to fill the entries with NaN values with ""
for column in columns:
    df[column] = df[column].fillna("Not Given")


# In[48]:


# Count missing values in each column
missing_count = df.isnull().sum()

# Display the total number of missing values per column
print("Missing values count per column:")
print(missing_count)


# ### Missing values : "date_added, duration"

# In[91]:


df = df.dropna()


# In[92]:


df


# ## Columns of strings, check for trailing whitespaces

# In[93]:


# Apply strip to all string columns
df = df.apply(lambda x: x.str.strip() if x.dtype == 'O' else x)


# ## Splitting clumns: extracting more information

# ### date_added

# In[94]:


# Convert the 'date_added' column to datetime format with errors='coerce'
df['date_added'] = pd.to_datetime(df['date_added'], format='%d-%b-%y', errors='coerce')

# Create new columns 'month_added', 'day_added', and 'year_added'
df['month_added'] = df['date_added'].dt.strftime('%B')
df['day_added'] = df['date_added'].dt.day
df['year_added'] = df['date_added'].dt.year

df


# In[95]:


# Create a cross-tabulation matrix
cross_tab = pd.crosstab(df['type'], df['duration'])

# Display the matrix
print("Cross-tabulation Matrix:")
print(cross_tab)


# ### duration

# In[96]:


# Create separate DataFrames for 'Movie' and 'TV Show'
df_movie = df[df['type'] == 'Movie'].copy()
df_tv_show = df[df['type'] == 'TV Show'].copy()



# In[97]:


df_tv_show


# In[98]:


df_movie


# ## Unique values

# In[99]:


# Concatenate the Movie and TV Show DataFrames
df_combined = pd.concat([df_movie, df_tv_show])

# Count unique values for each variable in the combined DataFrame
unique_values_combined = df_combined.nunique()

# Display the table with unique values
print("Unique Values for Movie and TV Show Combined:")
print(unique_values_combined)


# ## Standarizing columns values
# ###  Country

# In[100]:


# Display unique values and their counts for the "country" column
country_counts = df_combined['country'].value_counts()

# Display the first few unique values and their counts
print("Unique Values and Counts for 'country' column:")
print(country_counts.head())

# Display total unique values and counts
print("\nTotal Unique Values:", len(country_counts))
print("Total Counts:", country_counts.sum())


# In[101]:


# Split values in the 'country' column based on commas
split_countries = df['country'].str.split(',')

# Create a new column 'country1' with the first country
df_combined['country1'] = split_countries.str[0].str.strip()

# Drop the original 'country' column
df_combined.drop('country', axis=1, inplace=True)

df_combined


# In[103]:


# Display unique values and their counts for the "country" column
country_counts = df_combined['country1'].value_counts()

# Display the first few unique values and their counts
print("Unique Values and Counts for 'country' column:")
print(country_counts.head())

# Display total unique values and counts
print("\nTotal Unique Values:", len(country_counts))
print("Total Counts:", country_counts.sum())


# In[104]:


df_combined.head()


# # Exploratory Data Analysis

# In[106]:


import matplotlib.pyplot as plt
import seaborn as sns

# Display summary statistics
print("Summary Statistics:")
print(df_combined.describe())


# In[107]:


# Visualize the distribution of 'release_year'
plt.figure(figsize=(10, 6))
sns.histplot(df_combined['release_year'], bins=30, kde=True)
plt.title('Distribution of Release Year')
plt.xlabel('Release Year')
plt.ylabel('Frequency')
plt.show()


# In[108]:


# Visualize the count of different 'type' values
plt.figure(figsize=(8, 6))
sns.countplot(x='type', data=df_combined)
plt.title('Count of Different Types')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()


# In[109]:


# Visualize the distribution of 'rating'
plt.figure(figsize=(10, 6))
sns.countplot(x='rating', data=df_combined, order=df_combined['rating'].value_counts().index)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()


# In[110]:


# Visualize the count of shows added each month
plt.figure(figsize=(10, 6))
sns.countplot(x='month_added', data=df_combined, order=df_combined['month_added'].value_counts().index)
plt.title('Count of Shows Added Each Month')
plt.xlabel('Month Added')
plt.ylabel('Count')
plt.show()


# In[113]:


# Visualize a heatmap of correlations
plt.figure(figsize=(12, 8))
sns.heatmap(df_combined.corr(numeric_only=True), annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Heatmap of Correlations')
plt.show()


# In[115]:


# Save df_combined to CSV
df_combined.to_csv('df_combined.csv', index=False)

# Save df_movie to CSV
df_movie.to_csv('df_movie.csv', index=False)

# Save df_tv_show to CSV
df_tv_show.to_csv('df_tv_show.csv', index=False)

