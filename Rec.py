import lenskit.datasets as ds
import csv
import pandas as pd
from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser
from os import path

MOVIE_DATA_LOC ="ml-latest-small"
SEARCH_RESULT_COUNT = 10
MOVIES_TO_RECOMMEND = 10
pd.set_option('display.max_columns', 7)


class RecommendProgram(object):
    username = "curr.csv"

    def __init__(self, username):
        if path.exists(username + ".csv"):
            self.username = username + ".csv"
        else:
            with open(self.username, 'w') as csvfile:
                field_names = ['item', 'title', 'genres', 'ratings']
                file_writer = csv.DictWriter(csvfile, delimiter=',',
                                             quotechar='|', quoting=csv.QUOTE_MINIMAL, fieldnames=field_names)
                file_writer.writeheader()

        self.user_data = self.load_user_file()
        self.data = ds.MovieLens(MOVIE_DATA_LOC)
        self.combined = self.data.ratings.join(self.data.movies['genres'], on='item')
        self.combined = self.combined.join(self.data.movies['title'], on='item')
        self.enriched_movies = self.data.movies.copy()
        self.enriched_movies.rename(columns={"movieId": "item"})
        counts = self.data.ratings.groupby(by="item").count()
        counts = counts.rename(columns={'user': 'count'})

        self.enriched_movies = self.enriched_movies.join(counts['rating'], on='item')
        self.removed = pd.merge(self.data.ratings, counts['count'], on='item')
        self.removed = self.removed.sort_values(by='count', ascending=False)
        print(self.removed)
        self.removed = self.removed.loc[self.removed['count'] > 10]
        print(self.removed)

    def search_movies(self):
        command = None
        while command != "done":
            command = input()
            result = self.enriched_movies[self.enriched_movies['title'].str.contains(command)]
            result = result.sort_values(by='rating', ascending=False)

            index = 1
            for i, movie in result[0:SEARCH_RESULT_COUNT].iterrows():
                print(index, movie['title'], movie['genres'])
                index += 1

            choose = int(input("type number"))
            movie = result.iloc[choose - 1:choose]
            movie = movie.reset_index()
            print(movie)
            rate = input("How do you rate this from 0 to 5\n")
            self.add_new_movie_rating(movie, rate)

    def search_movie(self, title):

        result = self.enriched_movies[self.enriched_movies['title'].str.contains(title)]
        result = result.sort_values(by='rating', ascending=False)
        result = result.reset_index()

        index = 1
        for i, movie in result[0:SEARCH_RESULT_COUNT].iterrows():
            print(index, movie['title'], movie['genres'])
            index += 1

        return result[0:SEARCH_RESULT_COUNT]

    def show_movies_to_rate(self):
        confirmed_movies = self.load_user_file()
        movies = self.enriched_movies.sort_values(by='rating', ascending=False)
        movies = movies.reset_index()
        movies = movies.loc[movies['rating'] > 1000]
        print(movies.head(5))

        for i, movie in movies.iterrows():
            if movie['item'] in confirmed_movies:
                continue
            print(movie['title'])
            print("if seen movie, rate out of 5. otherwise press enter for more or done to quit")
            command = input()
            if command == "done":
                break
            if command == "":
                continue
            else:
                self.add_new_movie_rating(movie, int(command))

    def show_movies_to_rate(self, is_wb):
        confirmed_movies = self.load_user_file()
        movies = self.enriched_movies.sort_values(by='rating', ascending=False)
        movies = movies.reset_index()
        print(movies.head(5))

        for i, movie in movies.iterrows():
            if movie['item'] in confirmed_movies:
                continue
            print(movie['title'])
            return movie

    def load_user_file(self):
        confirmed_movies = []
        with open(self.username, newline='') as file:
            rating_reader = csv.DictReader(file)
            for row in rating_reader:
                confirmed_movies.append(int(row['item']))

        return confirmed_movies

    def add_new_movie_rating(self, movie, rate):
        with open(self.username, "a", newline='') as f:
            names = ['item', 'title', 'genres', 'ratings']
            wr = csv.DictWriter(f, fieldnames=names)
            wr.writerow({names[0]: movie['item'], names[1]: movie['title'],
                         names[2]: movie['genres'], names[3]: rate})

    def recommend_movies(self):
        first_data = {}

        with open(self.username, newline='') as csvfile:
            ratings_reader = csv.DictReader(csvfile)
            for row in ratings_reader:
                if (row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6):
                    first_data.update({int(row['item']): float(row['ratings'])})

        user_user = UserUser(10, min_nbrs=5)
        print(self.removed)
        algo = Recommender.adapt(user_user)
        algo.fit(self.removed)
        rec1 = algo.recommend(-1, 10, ratings=pd.Series(first_data))
        joined_data = rec1.join(self.data.movies['genres'], on='item')
        joined_data = joined_data.join(self.data.movies['title'], on='item')
        print(joined_data[joined_data.columns[2:]])
        return joined_data

    def fetch_more_movie_data(self):
        # box office, language
        pass

    def filter_movie_input_collection(self):
        # post-2000, genre, box office, language
        # by choosing an option the random would filter input
        pass

    def remove_useless_data(self):
        # low number of rated movies
        # very old  movies
        pass


ACTION, COMEDY = 1.5, 1.5
DOCUMENTARY = 0.5

# print(combined.head(5))

""" my code -------------------------------- """
"""
dd = data.movies
rating_counts = data.ratings.groupby(['item']).count()


new_data = dd.join(rating_counts['rating'], on='item')
new_data = new_data.sort_values(by='rating', ascending=False)

print(new_data)

confirmed = []

with open("newer_data.csv", newline='') as csvfile:
    ratings_reader = csv.DictReader(csvfile)
    for row in ratings_reader:
        confirmed.append(int(row['item']))

with open("newer_data.csv", "a", newline='') as f:
    names = ['item', 'title', 'genres', 'ratings']
    wr = csv.DictWriter(f, fieldnames=names)

    for movie in new_data.itertuples():
        if movie.Index in confirmed:
            continue
        if not re.search('\(2[0-9][1-2][8-9]\)', movie.title):
            continue
        print("please rate this out of 5, dear ho: ", movie.title)
        print("if you haven't watched it press enter!")
        r = input()
        if r == 'done':
            break

        wr.writerow({names[0]: movie.Index, names[1]: movie.title,
                     names[2]: movie.genres, names[3]: r})


print("adfgds")

first_data = {}

with open("newer_data.csv", newline='') as csvfile:
    ratings_reader = csv.DictReader(csvfile)
    for row in ratings_reader:
        if (row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6):
            num = y = 1
            first_data.update({int(row['item']): num * float(row['ratings']) * y})

num_recs = 30  # <---- This is the number of recommendations to generate.

average_ratings = data.ratings.groupby(['item']).mean()
rating_counts = data.ratings.groupby(['item']).count()
print("meow")
print(rating_counts['rating'])

bbb = []
#df.name.str.extract(r'([\d]+)',expand=False)
years = data.movies.loc[data.movies['title'].str.contains('\(2[0-9][0-9][0-9]\)', regex=True)]
years = years.loc[~years['title'].str.contains('Action')]
print(years.head(6))
years = years.reset_index()
print(years.head(6))

years = years['item']
print(years.head(6))

#bool(re.search("2[0-9][0-9][0-9]",str(data.movies['title'])))]
#and ~re.search("Action", str(data.movies['title']))
# find promising list of movies
rating_counts = rating_counts.rename(columns={'user': 'size'})
rating_counts = rating_counts.loc[(rating_counts['size'] > 1500)]
rating_counts = rating_counts.reset_index()
print(rating_counts.head(5))

rating_counts = pd.merge(rating_counts, years, on='item')
print("ss")
print(rating_counts.head(10))

# remove user rating for movies with low number of ratings
filtered = data.ratings
filtered = pd.merge(filtered, rating_counts, on='item')
print("last")
filtered = filtered.drop(columns=['size', 'rating_y', 'timestamp_y'])
filtered = filtered.rename(columns={'rating_x': 'rating', 'timestamp_x': 'timestamp'})

print(filtered.head(5))

# recommendation algorithm
user_user = UserUser(20, min_nbrs=5)
algo = Recommender.adapt(user_user)
algo.fit(filtered)
rec1 = algo.recommend(-1, num_recs, ratings=pd.Series(first_data))

# prepare result
joined_data = rec1.join(data.movies['genres'], on='item')
joined_data = joined_data.join(data.movies['title'], on='item')
joined_data = joined_data[joined_data['genres'].str.contains('Animation|Comedy|Romance|Thriller', regex=True)]
print(joined_data[joined_data.columns[2:]])




"""

"""joined_data = joined_data[~joined_data['genres'].str.contains("Documentary")]
joined_data = joined_data[joined_data['genres'].str.contains("Comedy")]"""

""" my code -------------------------------- """
"""
average_ratings = data.ratings.groupby(['item']).mean()

sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')
joined_data = joined_data.join(data.movies['title'], on='item')
joined_data = joined_data[joined_data.columns[1:]]

print(joined_data.head(5))

average_ratings = data.ratings.groupby('item').agg(count=('user', 'size'), rating=('rating', 'mean')).reset_index()
sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')
joined_data = joined_data.join(data.movies['title'], on='item')
joined_data = joined_data[joined_data.columns[1:]]

print(joined_data.head(5))"""
"""
minimum_to_include = 70  # <-- You can try changing this minimum to include movies rated by fewer or more people

average_ratings = data.ratings.groupby(['item']).mean()
rating_counts = data.ratings.groupby(['item']).count()
# print(rating_counts)
average_ratings = average_ratings.loc[rating_counts['rating'] > minimum_to_include]
sorted_avg_ratings = average_ratings.sort_values(by="rating", ascending=False)
joined_data = sorted_avg_ratings.join(data.movies['genres'], on='item')
joined_data = joined_data.join(data.movies['title'], on='item')
# joined_data = joined_data[joined_data.columns[3:]]

print(joined_data.head(5))
print(joined_data.columns)

joined_data = joined_data[joined_data.columns[3:]]
print(joined_data.head(5))
print(joined_data.columns)

first_data = {}
second_data = {}

with open("jabril-movie-ratings.csv", newline='') as csvfile:
    ratings_reader = csv.DictReader(csvfile)
    for row in ratings_reader:
        if (row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6):
            first_data.update({int(row['item']): float(row['ratings'])})

with open("jgb-movie-ratings.csv", newline='') as csvfile:
    ratings_reader = csv.DictReader(csvfile)
    for row in ratings_reader:
        if (row['ratings'] != "") and (float(row['ratings']) > 0) and (float(row['ratings']) < 6):
            second_data.update({int(row['item']): float(row['ratings'])})

print("Rating dictionaries assembled!")
print("Sanity check:")
print("\tJabril's rating for 1197 (The Princess Bride) is " + str(first_data[1197]))
print("\tJohn-Green-Bot's rating for 1197 (The Princess Bride) is " + str(second_data[1197]))

from lenskit.algorithms import Recommender
from lenskit.algorithms.user_knn import UserUser

num_recs = 10  #<---- This is the number of recommendations to generate. You can change this if you want to see more recommendations

user_user = UserUser(10, min_nbrs=3)
algo = Recommender.adapt(user_user)
algo.fit(data.ratings)

rec1 = algo.recommend(-1, num_recs, ratings=pd.Series(first_data))

joined_data = rec1.join(data.movies['genres'], on='item')
joined_data = rec1.join(data.movies['title'], on='item')
print(joined_data)

rec2 = algo.recommend(-1, num_recs, ratings=pd.Series(second_data))

joined_data = rec2.join(data.movies['genres'], on='item')
joined_data = rec2.join(data.movies['title'], on='item')
print(joined_data)

combined_rating_dict = {}
for k in first_data:
    if k in second_data:
        combined_rating_dict.update({k: float((first_data[k] + second_data[k]) / 2)})
    else:
        combined_rating_dict.update({k: first_data[k]})
for k in second_data:
    if k not in combined_rating_dict:
        combined_rating_dict.update({k: second_data[k]})


combined_recs = algo.recommend(-1, num_recs, ratings=pd.Series(combined_rating_dict))  #Here, -1 tells it that it's not an existing user in the set, that we're giving new ratings, while 10 is how many recommendations it should generate

joined_data = combined_recs.join(data.movies['genres'], on='item')
joined_data = joined_data.join(data.movies['title'], on='item')
joined_data = joined_data[joined_data.columns[2:]]
print("\n\nRECOMMENDED FOR JABRIL / JOHN-GREEN-BOT HYBRID:")
print("\n\n\n\n")
print(joined_data)"""
