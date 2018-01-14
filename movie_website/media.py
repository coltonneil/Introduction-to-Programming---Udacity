#define class Category
class Category():
    #used to create a list of all categories so that we can loop through them later without calling each one explicitly
    all_cats = []
    #initialize category, takes title as an input and creates an empty list to store movies
    def __init__(self,category_title):
        self.title = category_title
        self.movies = []
        Category.all_cats.append(self)
    #takes input as a list of movie objects, and adds each one to the categories list of movies
    def addMovies(self,movies):
        for movie in movies:
            self.movies.append(movie)
    #define class Movie
class Movie():
    #initialize Movie, takes in a string for title, a string for the poster url, a string for the summary, an int for the rating, and a string for the youtube trailer url
    def __init__(self, movie_title, movie_poster_image_url,movie_summary,movie_rating, movie_trailer_youtube_url):
        self.title = movie_title
        self.poster_image_url = movie_poster_image_url
        self.summary = movie_summary
        self.rating = movie_rating
        self.trailer_youtube_url = movie_trailer_youtube_url
