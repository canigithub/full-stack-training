class Movie():
    """
        This class contains movie title, box art, poster image, trailer URL and IMDB data title.
        IMDB data title is used to provide the rating from IMDB.
    """

    def __init__(self, title, box_art, poster_image_url, trailer_youtube_url, imdb_data_title):
        self.title = title
        self.box_art = box_art
        self.poster_image_url = poster_image_url
        self.trailer_youtube_url = trailer_youtube_url
        self.imdb_data_title = imdb_data_title
