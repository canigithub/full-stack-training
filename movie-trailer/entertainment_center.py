import media
import fresh_tomatoes as ft

zootopia = media.Movie("Zootopia",
                       "https://s-media-cache-ak0.pinimg.com/originals/49/ee/c1/49eec13dddec3290e3e58f26c162f676.jpg",
                       "http://www.impawards.com/2016/posters/zootopia_ver20_xlg.jpg",
                       "https://www.youtube.com/watch?v=jWM0ct-OLsM",
                       "tt2948356")

jason_bourne = media.Movie("Jason Bourne",
                           "https://s-media-cache-ak0.pinimg.com/originals/b9/38/91/b938919174f99460e96e57022f016077.jpg",
                           "http://wallpapers4screen.com/Uploads/16-7-2016/32180/thumb2-jason-bourne-poster-2016-action-thriller.jpg",
                           "https://www.youtube.com/watch?v=F4gJsKZvqE4",
                           "tt4196776")

operation_mekong = media.Movie("Operation Mekong",
                               "https://asianfilmstrike.files.wordpress.com/2016/09/094819-92984285_1000x1000.jpg",
                               "http://www.wellgousa.com/sites/default/files/theatrical/Heropage-980x560_58.jpg",
                               "https://www.youtube.com/watch?v=vcyef27rZ-w",
                               "tt6044910")

movies = [zootopia, jason_bourne, operation_mekong]

# calls open_movies_page function inside fresh_tomatoes
# to generate the movie trailers html file.
ft.open_movies_page(movies)
