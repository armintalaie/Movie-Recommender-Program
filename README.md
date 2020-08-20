#Movie Recommender Web Application

##What this program does:
- user can input movie rating of movies they have watched:
    - searching and rating
    - random movie suggestions to rate
- using the app's algorithm, it will provide the user with movies to watch next based on the movies rated


##How this program does it:
- it is based on a 25million input database of movies and user ratings
- the database is sorted, filtered and modified to remove unwanted data
- after input and rating collection from user a machine learning collaborate filtering/matrix factorization is applied


##technical breakdown of project:
- Pandas and Python are used to extract and classify the data
- imported "Lenskit" Machine learning algorithms are fitted to the data
- user-friendly website is implemented using HTML,CSS and JavaScript
- the algorithm, and website is developed and combined using Django