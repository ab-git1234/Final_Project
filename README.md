# Box Office Analysis
### Flatiron Capstone Project
#### Python Fever - Danish Ali, Adam Burstyn, Trevor Flanagan, Ian Haas, Hope Miller

### Project Overview
To discover insights into movie box office revenue from current industry data that will be used to make recomendations to Computing Vision in order to maximize the box office performance as well as popularity of their new movie production venture.



### Data Understanding
The team created a singular data frame, using Pandas to join all the tables on the relevent data allowing us to efficiently explore, ask questions and form hypotheses.  The core data comes from the IMDB data base giving us movie titles, revenues, ratings, production budgets and allowed us to merge supplemental details from all other sources and prepare a clear overview of box office information and start to hypothesise about what helps movies perform well.

In order to narrow our recommendations we tested the correlation between foriegn and domestic gross revenue and found that they were highly correlated.  So all further data was filtered to domestic information since it can be reasonably assumed that performance will be similar.

![Correlation Scatter Plot](/Images/gross_scatter_plot.png)

The aggregated, domestic data was then transformed using Panda's functions to seperate the combined genre column that described each movie with multiple tags, e.g. Action, Adventure, Comedy. Now each movie entry could be grouped by genre.  Allowing us to test whether one genre tag or combination of genre tags could result in higher grossing, more popular movies.

### Goals:
#### Discover the highest grossing movie genre from the data provided.
#### Discover the genre with the highest average net revenue from the data provided.
#### Discover the most popular genre from the data provided.


### Gross Box Office by genre
The team first decided to investigate which genre of movie has the highest average gross revenue from the data provided.
Used Python string access function explode() to seperate the genre column where many movie entries had many genre tags seperated by commas.
    
![Gross Box Office Revenue](/Images/top_gross.png)

Then we ordered these categories by gross revenue and discovered the Animation genre had the highest box office revenue.
t test compared to the next two highest average grossing genres, Adventure and Sci-Fi, showed a statistically significant difference between these and the fourth highest revenue. __The team can confidently make the recomendation that movies in the Animation, Adventure and Sci-Fi genre might make high box office revenues.__


###   Net revenue by genre
Using the average gross revenue and subtracting the budget column from the IMDB database that describes the amount of money budgeted to make the film, the team aggregated and calculated the average net revenue.

(![Net Profit](/Images/top_net.png))

Animation, Musical, and Comedy genre tags have the top three average net revenues. ___We make the recomendation that, for highest profit margins, Computing Vision should produce movies that can be lables as Animation, Musical, and Comedy.__


### Popularity by genre
Using the 'popularity' column from the "The Movies" database, the team investigated what genres were the highest in popular opinion. The team found Adventure is the most popular genre, while Documentaries received the highest vote score on average, but concluded the Documentaries vote score was an outlier, having few votes all with high scores and skewing the average. __We recommend that, for a goal of high popularity and engagement, a movie with the Adventure tag would perform well.__

![Popularity](/Images/top_popularity.png)


![Top votes](/Images/top_votes.png)



### In conclusion our recommendations to Computing Vision are:
#### Make movies that can be labled as Animation, Action, and/or Sci-fi to achieve the highest box office performance.
#### Make movies that can be labled as Animation and Musical to achieve the highest net revenue, ie profit.
#### Make movies that can be labled as Adventure to achieve maximum popularity and public appeal.

### Next Steps
Preliminary data exploration has already begun to discover which writers, directors, and actors are associated with 
high performing movies, and who Computing Vision may seek to involve in the creative process in the future.
*See Trevor's Notebook Appendix
