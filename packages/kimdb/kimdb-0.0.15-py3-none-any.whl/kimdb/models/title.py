# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union

# Local
from .imaged_title import ImagedTitle

from .base_name import BaseName
from .base_company import BaseCompany
from .base_list import BaseList

from .video import Video

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Title ------------------------------------------------------------- #

class Title(ImagedTitle):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        id,
        title: str,
        poster_url: str,
        rating: Optional[float],
        rating_count: Optional[int],
        release_date: Optional[str],
        genres: Optional[Union[str, List[str]]],
        actors: List[BaseName],
        directors: List[BaseName],
        creators: List[Union[BaseName, BaseCompany]],
        description: Optional[str],
        date_published: str,
        keywords: Optional[List[str]],
        trailer: Optional[Video],

        related_titles: List[ImagedTitle],
        lists: List[BaseList]
    ):
        super().__init__(id, title, poster_url)

        self.rating = rating
        self.rating_count = rating_count
        self.release_date = release_date

        if isinstance(genres, str):
            genres = [genres]

        self.genres = genres
        self.actors = actors
        self.directors = directors
        self.creators = creators
        self.description = description
        self.date_published = date_published
        self.keywords = keywords
        self.trailer = trailer

        self.related_titles = related_titles
        self.lists = lists


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #




    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_dict(
        cls,
        d: dict,
        related_titles: List[ImagedTitle],
        lists: List[BaseList]
    ):
        aggregate_rating = d['aggregateRating'] if 'aggregateRating' in d else {}
        rating = float(aggregate_rating['ratingValue']) if 'ratingValue' in aggregate_rating else None
        rating_count = aggregate_rating['ratingCount'] if 'ratingCount' in aggregate_rating else None

        return cls(
            id=d['url'].strip('/').split('/')[-1],
            title=d['name'],
            poster_url=d['image'],
            rating=rating,
            rating_count=rating_count,
            release_date=cls._d_val(d, 'datePublished'),
            genres=d['genre'] if 'genre' in d else None,
            actors=cls.__get_users_companies(d['actor']) if 'actor' in d else [],
            directors=cls.__get_users_companies(d['director']) if 'director' in d else [],
            creators=cls.__get_users_companies(d['creator']) if 'creator' in d else [],
            description=d['description'] if 'description' in d else None,
            date_published=d['datePublished'],
            keywords=d['keywords'].split(',') if 'keywords' in d else [],
            trailer=Video.from_dict(d['trailer']) if 'trailer' in d else None,
            related_titles=related_titles,
            lists=lists
        )


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def __get_users_companies(l: Union[dict, List[dict]]) -> List[Union[BaseName, BaseCompany]]:
        if isinstance(l, dict):
            l = [l]

        return [
            BaseName(e['url'].strip('/').split('/')[-1], e['name'])
            if 'name' in e
            else BaseCompany(e['url'].strip('/').split('/')[-1])
        for e in l]


# ---------------------------------------------------------------------------------------------------------------------------------------- #
