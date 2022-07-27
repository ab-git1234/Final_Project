#!/usr/bin/env python
# coding: utf-8

# ### Function to create total_movie_info df

# In[6]:


#imports
import sqlite3
import pandas as pd
import numpy as np
import regex as re
import matplotlib.pyplot as plt

def get_total_movie_info():
    # General Exploration of Data

    #Tables to explore info on the movies

    ## Load tables from data sources

    #Loading and looking at the tables and databases overall. Here we are trying to get a general idea of what we are working 
    #with


    movie_gross = pd.read_csv('../Data/bom.movie_gross.csv')
    movie_gross.head()

    #domestic gross hard to read due to large numbers
    #make domestic_gross abreviated as 'mil'

    #list of table names
    conn= sqlite3.connect("../Data/im.db")
    sql_query = """
    SELECT name FROM sqlite_master  
    WHERE type='table'
    ;"""

    pd.read_sql(sql_query,conn)

    #Person table
    q = """
    SELECT *
    FROM persons
    """
    persons_df = pd.read_sql(q, conn)

    persons_df.head()
    #missing data: birth and death year, primary professions
    #no missing person_id or primary_name

    #Writers table
    q = """
    SELECT *
    FROM writers
    """
    writers_df=pd.read_sql(q, conn)
    writers_df.head()
    writers_df.info()
    #many-to-many table(associative entity)

    #directors table
    q = """
    SELECT *
    FROM directors
    """
    directors_df=pd.read_sql(q, conn)
    directors_df.head()
    #many-to-many table(associative entity)

    #known_for table
    q = """
    SELECT *
    FROM known_for
    """
    known_for_df=pd.read_sql(q, conn)
    known_for_df.head()
    #many-to-many table(associative entity)
    #"this/these actor is known for many movies"

    #principals table
    q = """
    SELECT *
    FROM principals
    """
    principals_df=pd.read_sql(q, conn)
    principals_df.head()
    #missing many jobs and characters
    #some 'jobs' don't have character roles
    #none= no values 

    principals_df[principals_df['category']=='actor']
    #dataframe where the category is equal to actor
    #looking to see why the category is 'none'

    #movi_basics table
    q = """
    SELECT *
    FROM movie_basics
    """
    movie_basics_df=pd.read_sql(q, conn)
    movie_basics_df.head()

    #movie_ratings table
    q = """
    SELECT *
    FROM movie_ratings
    """
    movie_ratings_df=pd.read_sql(q, conn)
    movie_ratings_df.head()

    movie_ratings_df.info()
    #no null values

    #movie_akas table
    q = """
    SELECT *
    FROM movie_akas
    """
    movie_akas_df=pd.read_sql(q, conn)
    movie_akas_df.head()
    #multiple of the same movie ID, same movies but in different languages and regions
    #where certain movies do best

    reviews = pd.read_table('../Data/rt.reviews.tsv', encoding = 'latin-1')
    reviews.head()
    #need to use latin-1 in order to get it open
    #rating given out of 5(stored as string), might be best to only look at numerator 
    #use natural language processing to find missing ratings 

    tmdb_movies = pd.read_csv('../Data/tmdb.movies.csv')
    tmdb_movies.head()

    movie_budgets = pd.read_csv('../Data/tn.movie_budgets.csv')
    movie_budgets.head()
    #best table
    #can get gross amounts
    #forgeign gross = worldwide-domestic

    # Mapping Tables

    ### Combining tables without movie names 

    # Runtime to rating: movie_basics to movie_ratings

    # * only about half of ht movies have ratings. Brain storming ideas on how to solve potential missing ratings

    # Joinings movie basics and movie ratings tables on IDs
    df = movie_ratings_df.merge(movie_basics_df, how='inner', on='movie_id')
    df

    #Need to filter out foreign movies

    #### Looking at the movies_aka movies table to filter out regions

    # Joinings movie basics, movie ratings, and movie_akas tables on IDs
    df = movie_ratings_df.merge(movie_basics_df, how='inner', on='movie_id')
    df= df.merge(movie_akas_df, how='inner', on = "movie_id")
    df

    #### Keeping only the US movies

    #filtering out foerign movies, showing all regions(countries)
    df['region'].unique()

    #region we want to filter for is US

    us_movies = df[df['region']=='US']
    us_movies

    #Duplicate Movie IDs

    #dropping duplicate movie_id's
    us_movies= us_movies.drop_duplicates(subset=['movie_id'])
    us_movies


    #No duplicate movies, shows regions as well

    ### Adding in gross numbers to the table

    #### Clean title and year info to merge
    # -rules: 
    # 1. all lower
    # 2. only aplhanumeric
    # 3. remove spaces
    # 4. use primary title as title

    # merging on title AND year to show differnce in the movies with the same name (remakes?)

    # use RegEx to keep only alpha-numeric values, remove spaces and make all letters lowercase 
    #us_movies["title"] = us_movies["title"].map(lambda x: re.sub(r'[^A-Za-z0-9 ]+', '', x).lower())
    us_movies["title"] = us_movies["title"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    movie_budgets["movie"] = movie_budgets["movie"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    movie_gross["title"] = movie_gross["title"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())

    #splitting the release_date column into only a year

    # get a year column as int to match the other df types
    movie_budgets['year']= movie_budgets['release_date'].map(lambda x: int(x[-4:]))
    movie_budgets


    #### rename columns for merging
    ##### dataframes merged to get gros income across

    #movie_budgets.rename(columns={'movie': "title", 'domestic_gross':'domestic_gross_movie_budgets',
                         #'worldwide_gross': 'worldwide_gross_movie_budgets'}, inplace =True)
    #movie_gross.rename(columns={'domestic_gross': 'domestic_gross_movie_gross', 'foreign_gross': 'foreign_movie_gross'}, inplace =True)

    #us_movies.rename(columns ={'start_year': 'year'}, inplace=True)

    movie_budgets.rename(columns={"movie": "title", "domestic_gross": "domestic_gross_movie_budgets",
                          "worldwide_gross": "worldwide_gross_movie_budgets"}, inplace=True)

    movie_gross.rename(columns={"domestic_gross": "domestic_gross_movie_gross", 
                        "foreign_gross": "foreign_gross_movie_gross"}, inplace=True)

    #combine tables with 2 columns to distinguish different movies with same name
    final_gross_df1 = us_movies.merge(movie_budgets, on="title", how="inner")
    final_gross_df1

    final_gross_df2=us_movies.merge(movie_gross, on='title', how='inner').drop_duplicates(subset=['movie_id'])
    final_gross_df2

    #shows all gross tables merged
    final_gross_all = pd.concat([final_gross_df1, final_gross_df2]).drop_duplicates(subset=['movie_id'])
    final_gross_all

    #finding length of final_gross_df1
    len(final_gross_df1), final_gross_df1['movie_id'].nunique()

    final_gross_df1, final_gross_df1['movie_id'].nunique()

    ## Investigate Rotten Tomatoes Data

    #Joining director and movie 

    #Load tables
    conn = sqlite3.connect("../Data/im.db")
    sql_query = """
    SELECT name FROM sqlite_master  
    WHERE type='table';
    """
    pd.read_sql(sql_query,conn)

    #putting director's name and movie name in one table
    q = """
    SELECT movie_basics.movie_id, movie_basics.primary_title, persons.primary_name
    FROM directors
    JOIN movie_basics on directors.movie_id = movie_basics.movie_id
    JOIN persons ON directors.person_id = persons.person_id
    """
    director_to_movies = pd.read_sql(q, conn).drop_duplicates(subset=['primary_name','primary_title'])
    director_to_movies

    #rt_move_info and rt_movie_reviews

    #load rotten tomatoes
    rt_movie_info = pd.read_table('../Data/rt.movie_info.tsv')
    rt_movie_info.head()


    #Splitting the theatre_date column into just year. Done to be able to merge rt_movie_info with total_movie_info

    #drop missing values
    rt_movie_info.dropna(subset=['theater_date'],inplace=True)
    #split theatre_date column
    rt_movie_info['year']= rt_movie_info['theater_date'].map(lambda x: int(x[-4:]))
    rt_movie_info.head()

    #Plan: replace person ID with direct name and movie_id with the movie name. Then we will merge RT data with the gross table data. Merge on director and release date

    ## Merging the rotten tomatoes table with the director movie table

    ##### This will allow us to match the director with the release date


    #The goal in this is to match the director with the movie--- hopefully each director has only released one movie on one day

    #merging direct_to_movies with final_gross_all
    total_movie_info= final_gross_all.merge(director_to_movies[['movie_id','primary_name']], on="movie_id", how="left")
    total_movie_info[total_movie_info["movie_id"].duplicated(keep=False)]
    #checked to make sure duplicates all had different directors

    #Dropped duplicates but kept movies that appeared twice. Some movies will have 2 different directors.

    ### Final Merged Table

    #Gives us income, budget, genre, date, title, director, rating

    #Dropping NAN values
    total_movie_info.dropna(subset='primary_name', inplace= True)
    rt_movie_info.dropna(subset='director', inplace= True)

    #### Cleaning before the merge

    #making the primary_name uniform in im.db directors table
    total_movie_info["primary_name"] = total_movie_info["primary_name"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    #making the director names uniform in rt_movie_info table
    rt_movie_info["director"] = rt_movie_info["director"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())

    #merging total_movie_info to rt_movie_info
    total_movie_info_all= total_movie_info.merge(rt_movie_info, left_on=['primary_name','year'],right_on=['director','year'], how="left")
    total_movie_info

    #checking for dupicate movie_id's
    total_movie_info[total_movie_info["movie_id"].duplicated(keep=False)]

    return total_movie_info


# Function to turn str dollar values to float
def dollar_to_float(column):
    new_col = column.replace('[$,()]', '', regex=True).astype(float)
    
    return new_col


# Function to fill NaN values with corresponding column where available
# otherwise 0
def handle_NaN(col1, col2):
    new_col = col1.fillna(col2)
#     new_col = new_col.fillna(0)
    
    return new_col
    
def get_clean_df():
    df = get_total_movie_info()
    df["clean_domestic_gross"] = handle_NaN(df["domestic_gross_movie_budgets"], df["domestic_gross_movie_gross"])
    df["clean_worldwide_gross"] = handle_NaN(df["worldwide_gross_movie_budgets"], df["foreign_gross_movie_gross"])
    df["clean_domestic_gross"] = dollar_to_float(df["clean_domestic_gross"])
    df["clean_worldwide_gross"] = dollar_to_float(df["clean_worldwide_gross"])
    df["production_budget"] = dollar_to_float(df["production_budget"])
    
    return df



