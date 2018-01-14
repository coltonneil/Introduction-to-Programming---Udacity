import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }

        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }

        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }

        #trailer-video {
            width: 100%;
            height: 100%;
        }

        .movie-container {
            margin-bottom: 20px;
            padding-top: 20px;
        }

        .movie {
            padding: 20px;
            box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
            transition: all .375s;
            transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
        }

        .movie:hover {
            cursor: pointer;
            box-shadow: 0 14px 28px rgba(0, 0, 0, 0.25), 0 10px 10px rgba(0, 0, 0, 0.22);
        }

        .movie:hover>.movie-details {
            color: black;
            opacity: 1;
        }

        .movie:hover>.movie-poster {
            opacity: .05;
        }


        .movie-details {
            position: absolute;
            top: 0;
            padding: 40px;
            left: 0;
            opacity: 0;
            transition: all .375s;

            transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
        }

        .movie-poster {
            width: 220px;
            height: 342px;
                        transition: all .375s;

            transition-timing-function: cubic-bezier(0.4, 0.0, 0.2, 1);
        }

        .rating-container {
            width:120px;
            margin: 0 auto;
        }

        .rating-svg{

        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }

        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
    </style>
    <script type="text/javascript" charset="utf-8">
        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-container', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
                'id': 'trailer-video',
                'type': 'text-html',
                'src': sourceUrl,
                'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
            $('.movie-container').hide().first().show("fast", function showNext() {
                $(this).next("div").show("fast", showNext);
            });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single category entry html template
category_content = '''<div class="col-md-12 category-tile text-center">
    <h1>{category_name}</h1>
</div>'''
# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-container text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal"
    data-target="#trailer">
    <div class="movie">
    <img class="movie-poster" src="{poster_image_url}">

    <div class="movie-details">
        <div class="movie-title">
        <h2>{movie_title}</h2>
    </div>
        <p>{movie_summary}</p>
            <div class="rating-container">
        <svg class="rating-svg" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 68 11.5">
            <defs>
                <linearGradient id="_{fill_id}_a">
                    <stop offset="{movie_rating}%" stop-color="#ffdf00" />
                    <stop offset="{movie_rating}%" stop-color="#ffdf00" stop-opacity="0" />
                </linearGradient>
                <linearGradient id="_{fill_id}_b" x2="68" y1="5.75" y2="5.75" gradientUnits="userSpaceOnUse" xlink:href="#_{fill_id}_a" />
            </defs>
            <path class="rating-svg-path" fill="url(#_{fill_id}_b)" d="M 62,8.8000002 65.71,11.5 64.29,7.1400002 68,4.5000002 H 63.45 L 62,2e-7 l -1.45,4.5 H 56 l 3.71,2.64 L 58.29,11.5 Z m -14,0 L 51.71,11.5 50.29,7.1400002 54,4.5000002 H 49.45 L 48,4e-7 46.55,4.5000002 H 42 l 3.71,2.64 L 44.29,11.5 Z m -14,0 L 37.71,11.5 36.29,7.1400002 40,4.5000002 H 35.45 L 34,0 32.55,4.5000002 H 28 l 3.71,2.64 L 30.29,11.5 Z m -14,0 L 23.71,11.5 22.29,7.1400002 26,4.5000002 H 21.45 L 20,4e-7 18.55,4.5000002 H 14 l 3.71,2.64 L 16.29,11.5 Z m -14,0 L 9.71,11.5 8.29,7.1400002 12,4.5000002 H 7.45 L 6,2e-7 l -1.45,4.5 H 0 l 3.71,2.64 L 2.29,11.5 Z"
            />
        </svg>
    </div>
    </div>
    </div>
</div>
'''

#dynamically creates HTML from categories and movies objects
#input list of objects of class type category which in turn contain all movie objects
#functon loops through categories and uses a nested loop to get the movies from each category
def create_movie_tiles_content(categories):
    content = ''
    cat_index = 0
    for category in categories:
        content += category_content.format(category_name=category.title)
        mov_index = 0
        cat_index += 1
        for movie in category.movies:
            youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.trailer_youtube_url)
            youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.trailer_youtube_url)
            trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None
            content += movie_tile_content.format(movie_title = movie.title,poster_image_url = movie.poster_image_url,movie_summary = movie.summary,fill_id = str(cat_index)+'_'+str(mov_index),movie_rating = movie.rating * 20,trailer_youtube_id = trailer_youtube_id)
            mov_index += 1
    return content

#writes and opens html file
#input list of objects of class type category
def open_movies_page(categories):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(
      movie_tiles=create_movie_tiles_content(categories))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible
