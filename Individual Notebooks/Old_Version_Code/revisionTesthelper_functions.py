#imports
import sqlite3
import pandas as pd
import numpy as np
import regex as re
import matplotlib.pyplot as plt
from get_total_movie_info import *

def get_clean_df():
    # # General Exploration of Data

    # Tables to explore info on the movies

    # ## Load tables from data sources

    # Loading and looking at the tables and databases overall. Here we are trying to get a general idea of what we are working 
    # with
    # 

    # In[2]:


    movie_gross = pd.read_csv('../Data/bom.movie_gross.csv')
    movie_gross.head()

    #domestic gross hard to read due to large numbers
    #make domestic_gross abreviated as 'mil'


    # In[3]:


    # connect to sql db
    conn= sqlite3.connect("../Data/im.db")


    # In[4]:


    #movi_basics table
    q = """
    SELECT *
    FROM movie_basics
    """
    movie_basics_df=pd.read_sql(q, conn)
    movie_basics_df.head()


    # In[5]:


    #movie_ratings table
    q = """
    SELECT *
    FROM movie_ratings
    """
    movie_ratings_df=pd.read_sql(q, conn)
    movie_ratings_df.head()


    # In[6]:


    #movie_akas table
    q = """
    SELECT * FROM movie_akas
    """
    movie_akas_df = pd.read_sql(q, conn)
    movie_akas_df.head()


    # In[7]:


    movie_budgets = pd.read_csv('../Data/tn.movie_budgets.csv')
    movie_budgets.head()
    #best table
    #can get gross amounts
    #forgeign gross = worldwide-domestic


    # # Mapping Tables

    # ### Combining tables without movie names 

    # Runtime to rating: movie_basics to movie_ratings

    # * only about half of ht movies have ratings. Brain storming ideas on how to solve potential missing ratings

    # In[8]:


    # Joinings movie basics and movie ratings tables on IDs
    df = movie_ratings_df.merge(movie_basics_df, how='inner', on='movie_id')
    df


    # Need to filter out foreign movies

    # #### Looking at the movies_aka movies table to filter out regions

    # In[9]:


    # Joinings movie basics, movie ratings, and movie_akas tables on IDs
    df = movie_ratings_df.merge(movie_basics_df, how='inner', on='movie_id')
    df= df.merge(movie_akas_df, how='inner', on = "movie_id")
    df


    # #### Keeping only the US movies

    # In[10]:


    #filtering out foerign movies, showing all regions(countries)
    df['region'].unique()


    # region we want to filter for is US

    # In[11]:


    us_movies = df[df['region']=='US']
    us_movies


    # Duplicate Movie IDs

    # In[12]:


    #dropping duplicate movie_id's
    us_movies= us_movies.drop_duplicates(subset=['movie_id'])
    us_movies


    # No duplicate movies, shows regions as well

    # ### Adding in gross numbers to the table

    # #### Clean title and year info to merge
    # -rules: 
    # 1. all lower
    # 2. only alphanumeric
    # 3. remove spaces
    # 4. use primary title as title
    # 
    # merging on title AND year to show differnce in the movies with the same name (remakes?)

    # In[13]:


    # use RegEx to keep only alpha-numeric values, remove spaces and make all letters lowercase 
    #us_movies["title"] = us_movies["title"].map(lambda x: re.sub(r'[^A-Za-z0-9 ]+', '', x).lower())
    us_movies["title"] = us_movies["title"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    movie_budgets["movie"] = movie_budgets["movie"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    movie_gross["title"] = movie_gross["title"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())


    # In[14]:


    #splitting the release_date column into only a year


    # In[15]:


    # get a year column as int to match the other df types
    # movie_budgets['year']= movie_budgets['release_date'].map(lambda x: int(x[-4:]))
    # movie_budgets


    # #### rename columns for merging
    # ##### dataframes merged to get gros income across

    # In[16]:


    #movie_budgets.rename(columns={'movie': "title", 'domestic_gross':'domestic_gross_movie_budgets',
                                #'worldwide_gross': 'worldwide_gross_movie_budgets'}, inplace =True)
    #movie_gross.rename(columns={'domestic_gross': 'domestic_gross_movie_gross', 'foreign_gross': 'foreign_movie_gross'}, inplace =True)

    #us_movies.rename(columns ={'start_year': 'year'}, inplace=True)

    movie_budgets.rename(columns={"movie": "title", "domestic_gross": "domestic_gross_movie_budgets",
                                "worldwide_gross": "worldwide_gross_movie_budgets"}, inplace=True)

    movie_gross.rename(columns={"domestic_gross": "domestic_gross_movie_gross", 
                                "foreign_gross": "foreign_gross_movie_gross"}, inplace=True)


    # In[17]:


    #combine tables with 2 columns to distinguish different movies with same name
    final_gross_df1 = us_movies.merge(movie_budgets, on="title", how="inner")
    final_gross_df1


    # In[18]:


    final_gross_df2=us_movies.merge(movie_gross, on='title', how='inner').drop_duplicates(subset=['movie_id'])
    final_gross_df2


    # In[19]:


    #shows all gross tables merged
    final_gross_all = pd.concat([final_gross_df1, final_gross_df2]).drop_duplicates(subset=['movie_id'])
    final_gross_all


    # ## Investigate Rotten Tomatoes Data

    # Joining director and release date

    # In[20]:


    #putting director's name and movie name in one table
    q = """
    SELECT movie_basics.movie_id, movie_basics.primary_title, persons.primary_name
    FROM directors
    JOIN movie_basics on directors.movie_id = movie_basics.movie_id
    JOIN persons ON directors.person_id = persons.person_id
    """
    director_to_movies = pd.read_sql(q, conn).drop_duplicates(subset=['primary_name','primary_title'])
    director_to_movies


    # rt_move_info and rt_movie_reviews

    # In[21]:


    #load rotten tomatoes
    rt_movie_info = pd.read_table('../Data/rt.movie_info.tsv')
    rt_movie_info.head()


    # # *****need to unpack rows with multiple directors

    # In[22]:


    for index, row in rt_movie_info.iterrows():
        print(row["director"])


    # In[23]:


    x = rt_movie_info.dropna(subset=["director"])
    x[x["director"].str.contains("\|")]


    # In[24]:


    # directors = rt_movie_info['director']
    # rt_movie_info['director'] = directors.str.split(pat="|")


    # In[25]:


    # testing unpacking the directors
    direcs = []
    ids = []

    for index, row in rt_movie_info.iterrows():
        try:
            for person in row["director"]:
                direcs.append(person)
                ids.append(row["id"])
        except:
            direcs.append("-")
            ids.append(row["id"])
            
    y = pd.DataFrame({"rt_id": ids, "director": direcs})
    y[y["rt_id"].duplicated(keep=False)]


    # Splitting the theatre_date column into just year. Done to be able to merge rt_movie_info with total_movie_info

    # In[26]:


    #drop missing values
    rt_movie_info.dropna(subset=['theater_date'],inplace=True)
    #split theatre_date column
    rt_movie_info['year']= rt_movie_info['theater_date'].map(lambda x: int(x[-4:]))
    rt_movie_info.head()


    # Plan: replace person ID with direct name and movie_id with the movie name. Then we will merge RT data with the gross table data. Merge on director and release date

    # ## Merging the rotten tomatoes table with the director movie table

    # ##### This will allow us to match the director with the release date
    # 

    # The goal in this is to match the director with the movie--- hopefully each director has only released one movie on one day

    # In[27]:


    #merging direct_to_movies with final_gross_all
    total_movie_info= final_gross_all.merge(director_to_movies[['movie_id','primary_name']], on="movie_id", how="left")
    total_movie_info[total_movie_info["movie_id"].duplicated(keep=False)]
    #checked to make sure duplicates all had different directors


    # In[28]:


    total_movie_info.head()


    # In[29]:


    total_movie_info[["release_date"]]


    # Dropped duplicates but kept movies that appeared twice. Some movies will have 2 different directors.

    # We are going to merge based the assumption that no director/directors released more than 1 movie on the exact same day

    # ### Final Merged Table

    # Gives us income, budget, genre, date, title, director, rating

    # In[30]:


    #Dropping NAN values
    total_movie_info.dropna(subset=['primary_name', 'release_date'], inplace= True)
    rt_movie_info.dropna(subset=['director', 'theater_date'], inplace= True)


    # #### Cleaning before the merge

    # In[32]:


    #making the primary_name uniform in im.db directors table
    total_movie_info["primary_name"] = total_movie_info["primary_name"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    #making the director names uniform in rt_movie_info table
    rt_movie_info["director"] = rt_movie_info["director"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())


    # In[46]:


    #merging total_movie_info to rt_movie_info
    total_movie_info_all= total_movie_info.merge(rt_movie_info, left_on=['primary_name','release_date'],right_on=['director','theater_date'], how="left")
    total_movie_info_all


    # In[47]:


    total_movie_info_all[["theater_date", "release_date", "director", "primary_name"]].head()
           
    
    
    total_movie_info_all["clean_domestic_gross"] = handle_NaN(total_movie_info_all["domestic_gross_movie_budgets"], total_movie_info_all["domestic_gross_movie_gross"])
    total_movie_info_all["clean_worldwide_gross"] = handle_NaN(total_movie_info_all["worldwide_gross_movie_budgets"], total_movie_info_all["foreign_gross_movie_gross"])
    total_movie_info_all["clean_domestic_gross"] = dollar_to_float(total_movie_info_all["clean_domestic_gross"])
    total_movie_info_all["clean_worldwide_gross"] = dollar_to_float(total_movie_info_all["clean_worldwide_gross"])
    total_movie_info_all["production_budget"] = dollar_to_float(total_movie_info_all["production_budget"])

    return total_movie_info_all

def dollar_to_float(column):
        new_col = column.replace('[$,()]', '', regex=True).astype(float)
        
        return new_col

def handle_NaN(col1, col2):
    new_col = col1.fillna(col2)
#     new_col = new_col.fillna(0)

    return new_col


