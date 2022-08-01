# Final_Project
Flatiron Capstone Project


Beginning
Overview
Business Understanding

Project Overview
Discover insights into movie box office revenue from current industry data that will be used to make recomendations to Computing Vision in order to maximize the box office performance as well as popularity of their new movie production venture.


Middle
Data Understanding
The team created a singular data frame, using Pandas to join all the tables on the relevent data allowing us to efficiently explore, ask questions and form hypotheses.  The core data comes from the IMDB data base giving us movie titles, revenues, ratings, production budgets and allowed us to merge supplemental details from all other sources and prepare a clear overview of box office information and start to hypothesise about what helps movies perform well.

In order to narrow our recommendations we tested the correlation between foriegn and domestic gross revenue and found that they were highly correlated.  So all further data was filtered to domestic information since it can be reasonably assumed that performance will be similar.

![Correlation Scatter Plot](/Images/gross_scatter_plot.png)

The aggregated, domestic data was then transformed using Panda's functions to seperate the combined genre column that described each movie with multiple tags, eg(Action, Adventure, Comedy), now each movie entry could be grouped by genre.  Allowing us to test whether one genre tag or combination of genre tags could result in higher revenue, more popular movies.

Goals:
Discover the highest grossing movie genre from the data provided.
Discover the genre with the highest average net revenue fromt the data provided.
Discover the ost popular genre from the data provided.


1. Gross Box Office by genre
    Highest performing genre
    The team first decided to investigate which genre of movie has the highest average gross revenue from the data provided.
    Used Python string access function explode() to seperate the genre column where many movie entries had many genre tags seperated by commas.
    
    ![Gross Box Office Revenue](/Images/top_gross.png)
    
    Then ordered these categories by gross revenue and discovered the Animation genre had the highest box office revenue.
    t test compared to the next two highest average grossing genres, Adventure and Sci-Fi, showed a statistically significant difference in revenue and allows us to make recomendations that movies in the Animation, Adventure and Sci-Fi genre might make high revenues.
    

2.  Net revenue by genre
    Using the average gross revenue and the 'budget' column from the IMDB database, the team aggregated and calculated the average net revenue. gross - budget = net
    
    ![Net Profit](/Images/top_net.png)
    
    Animation, Musical, and Comedy genre tags are the top three average net revenue. Highest profit margins.  Recommend as movies to produce to make profit.


3. Popularity by genre
    Using the 'popularity' column from the "The Movies" database, the team investigated what genres were the most popular. The team also investigated and found Adventure is the most popular genre, while Documentaries received the highest vote score on average, but concluded the vote score caused by the outlier of having few votes all with high scores and skewing the average.  After a t test on the popularity metric we recommend that, for a goal of high popularity and engagement, a movie with the Adventure tag would perform well.
    
    ![Popularity](/Images/top_popularity.png)
    ![Top votes](/Images/top_votes.png)

End
Recommendations
Our recommendations to Computing Vision are:
Make movies that can be labled as Animation, Action, and/or Sci-fi to achieve the highest box office performance.
Make movies that can be labled as Animation and Musical to achieve the highest net revenue, ie profit.
Make movies that can be labled as Adventure to achieve maximum popularity and public appeal.

Next Steps
Preliminary data exploration has already begun to discover which writers, directors, and actors are associated with 
high performing movies, and who Computing Vision may seek to involve in the creative process in the future.
*See Trevor's Notebook Appendix* *See Adam's Notebook Appendix*

Thank You
This slide should include a prompt for questions as well as your contact information (name and LinkedIn profile)
