# Helper Functions
# This notebook contains the code to build and test the helper functions used to clean the data.
# The functions are built so they can be used by any team member in any notebook.

# import libraries
import sqlite3
import pandas as pd
import regex as re

def get_clean_df():
    """
    This function will return clean gross financial and budget figures for the movie data.
    """
    # movie gross data
    movie_gross = pd.read_csv('./Data/bom.movie_gross.csv')

    # connect to sql db
    conn= sqlite3.connect("./Data/im.db")

    #movie_basics table
    q = """
    SELECT *
    FROM movie_basics
    """
    movie_basics_df=pd.read_sql(q, conn)

    #movie_ratings table
    q = """
    SELECT *
    FROM movie_ratings
    """
    movie_ratings_df=pd.read_sql(q, conn)

    #movie_akas table
    q = """
    SELECT * FROM movie_akas
    """
    movie_akas_df = pd.read_sql(q, conn)

    #close the connection to the sql db
    conn.close()

    # movie budget data
    movie_budgets = pd.read_csv('./Data/tn.movie_budgets.csv')

    # ## Combine tables from sql db

    # Joinings movie basics, movie ratings, and movie_akas tables on IDs
    df = movie_ratings_df.merge(movie_basics_df, how='inner', on='movie_id')
    df= df.merge(movie_akas_df, how='inner', on = "movie_id")

    # keep only US
    us_movies = df[df['region']=='US']

    #dropping duplicate movie_id's
    us_movies= us_movies.drop_duplicates(subset=['movie_id'])

    # ## Adding in gross numbers to the table

    # #### Clean title and year info to merge
    # -rules: 
    # 1. all lower
    # 2. only alphanumeric
    # 3. remove spaces
    #     *to eliminate issues with titles contaning "Star Wars:Episode 3" vs "Star Wars: Episode 3" and "Mc'Donald" vs "mc donald"
    # 4. use primary title as title
    # 
    # *merging on title AND year to show difference in the movies with the same name (remakes)

    # use RegEx to keep only alpha-numeric values, remove spaces and make all letters lowercase
    us_movies["title"] = us_movies["title"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    movie_budgets["movie"] = movie_budgets["movie"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())
    movie_gross["title"] = movie_gross["title"].map(lambda x: re.sub(r'[^A-Za-z0-9]+', '', x).lower())

    # rename columns for clean merging
    movie_budgets.rename(columns={"movie": "title", "domestic_gross": "domestic_gross_movie_budgets",
                                "worldwide_gross": "worldwide_gross_movie_budgets"}, inplace=True)

    movie_gross.rename(columns={"domestic_gross": "domestic_gross_movie_gross", 
                                "foreign_gross": "foreign_gross_movie_gross"}, inplace=True)

    us_movies.rename(columns={"start_year": "year"}, inplace=True)


    # add a year column for merging on year
    movie_budgets["year"] = movie_budgets["release_date"].map(lambda x: int(x[-4:]))

    #combine tables on title and year columns to distinguish different movies with same name and different release dates
    final_gross_df1 = us_movies.merge(movie_budgets, on=["title", "year"], how="inner")
    final_gross_df2=us_movies.merge(movie_gross, on=['title', 'year'], how='inner').drop_duplicates(subset=['movie_id'])

    #concatenate all gross tables
    final_gross_all = pd.concat([final_gross_df1, final_gross_df2]).drop_duplicates(subset=['movie_id'])

    # ## Clean financial values

    # convert strings to floats
    final_gross_all["domestic_gross_movie_budgets"] = final_gross_all["domestic_gross_movie_budgets"].replace('[$,()]', '', regex=True).astype(float)
    final_gross_all["worldwide_gross_movie_budgets"] = final_gross_all["worldwide_gross_movie_budgets"].replace('[$,()]', '', regex=True).astype(float)
    final_gross_all["foreign_gross_movie_gross"] = final_gross_all["foreign_gross_movie_gross"].replace('[$,()]', '', regex=True).astype(float)
    final_gross_all["production_budget"] = final_gross_all["production_budget"].replace('[$,()]', '', regex=True).astype(float)

    # replace missing gross values from bugets data with gross data from gross table
    final_gross_all["clean_domestic_gross"] = final_gross_all["domestic_gross_movie_budgets"].fillna(final_gross_all["domestic_gross_movie_gross"])
    final_gross_all["clean_worldwide_gross"] = final_gross_all["worldwide_gross_movie_budgets"].fillna(final_gross_all["domestic_gross_movie_gross"])

    # drop the remaining null values
    final_gross_all.dropna(subset=["clean_domestic_gross", "clean_worldwide_gross"], inplace=True)

    return final_gross_all

def median_days_in_theater(genre):
    rt_movie_info = pd.read_table("./Data/rt.movie_info.tsv", thousands=',')
    rt_movie_info3 = rt_movie_info
    
    rt_movie_info3['theater_date'] = pd.to_datetime(rt_movie_info3['theater_date'])
    rt_movie_info3['dvd_date'] = pd.to_datetime(rt_movie_info3['dvd_date'])
    rt_movie_info3['days_in_theater'] = rt_movie_info3['dvd_date'] - rt_movie_info3['theater_date']
    rt_movie_info3['days_in_theater'] = rt_movie_info3['days_in_theater'].dt.days #dt.dats converts timedelta to float
    rt_movie_info3['release_year'] = rt_movie_info3['theater_date'].dt.year
    today = pd.to_datetime('today').normalize()
    rt_movie_info3 = rt_movie_info3[(today.year - rt_movie_info3['release_year'] <= 10)]
    
    genres = rt_movie_info3['genre']
    rt_movie_info3['genre'] = genres.str.split(pat="|")
    rt_movie_info3 = rt_movie_info3.explode("genre").reset_index(drop=True)
    
    genre_in_theatre = rt_movie_info4.groupby("genre").median()[["days_in_theater"]].sort_values("days_in_theater", ascending=False)
    
    median_days = genre_in_theater.loc[[genre]]['days_in_theater']
    median_days = median_days[0]
    
    return median_days

def genre_list():
    rt_movie_info = pd.read_table("./Data/rt.movie_info.tsv", thousands=',')
    rt_movie_info3 = rt_movie_info

    genres = rt_movie_info3['genre']
    rt_movie_info3['genre'] = genres.str.split(pat="|")
    rt_movie_info3 = rt_movie_info3.explode("genre").reset_index(drop=True)
    genres = rt_movie_info3['genre']
    
    return genres.unique()