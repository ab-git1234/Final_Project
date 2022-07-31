# Final_Project
Flatiron Capstone Project


Beginning
Overview
Business Understanding

Project Overview
For this project, you will use exploratory data analysis and statistical methods to generate insights for a business stakeholder.

Business Problem
Computing Vision (a made-up company for the purposes of this project) sees all the big companies creating original video content and they want to get in on the fun. They have decided to create a new movie studio, but they don’t have much background in creating movies. You are charged with exploring what types of films are currently doing the best at the box office using different samples of available data. You then will translate those findings into actionable insights that the head of Computing Vision's new movie studio can use to help decide what type of films to create.

Middle
Data Understanding
The team created a singular data frame, using Pandas to join all the tables on the relevent data allowing us to efficiently explore and ask questions and form hypotheses.  The core data comes from the IMDB data base giving us movie titles, revenues, ratings, production budgets and allowed us to merge supplemental details from all other sources and prepare a clear overview of box office information and start to hypothesise about what helps movies perform well.


Goal:
Highest gross
Highest net
Most popular through engagement.


1. Gross Box Office by genre
    Highest performing genre
    The team first decided to investigate which genre of movie has the highest average gross revenue from the data provided.
    Used Python string access function explode() to seperate the genre column where many movie entries had many genre tags seperated by commas.
    Then ordered these categories by gross revenue and discovered the Animation genre had the highest box office revenue.
    t test compared to the next two highest average grossing genres, Adventure and Sci-Fi, showed a statistically significant difference in revenue and allows us to make recomendations that movies in the Animation, Adventure and Sci-Fi genre might make high revenues.
    

2.  Net revenue by genre
    Using the average gross revenue and the 'budget' column from the IMDB database, the team aggregated and calculated the average net revenue. gross - budget = net
    Animation, Musical, and Comedy genre tags are the top three average net revenue. Highest profit margins.  Recommend as movies to produce to make profit.


3. Popularity by genre
    Using the 'popularity' column from the "The Movies" database, the team investigated what genres were the most popular. The team also investigated and found Adventure is the most popular genre, while Documentaries received the highest vote score on average, but concluded the vote score caused by the outlier of having few votes all with high scores and skewing the average.  After a t test on the popularity metric we recommend that, for a goal of high popularity and engagement, a movie with the Adventure tag would perform well.
    
    
    
    
    
    
    
Data Analysis
Statistical Inference
End
Recommendations
Next Steps
Thank You
This slide should include a prompt for questions as well as your contact information (name and LinkedIn profile)
