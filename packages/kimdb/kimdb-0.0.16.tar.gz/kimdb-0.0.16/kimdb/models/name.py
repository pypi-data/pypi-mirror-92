# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List, Union

# Local
from .base_name import BaseName
from .imaged_title import ImagedTitle

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# -------------------------------------------------------------- class: Name ------------------------------------------------------------- #

class Name(BaseName):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        id: str,
        name: str,
        image_url: str,
        job_titles: Union[str, List[str]],
        description: Optional[str],
        birth_date: Optional[str],
        known_for_titles: List[ImagedTitle],
        filmography_titles: List[ImagedTitle]
    ):
        super().__init__(id, name)

        self.image_url = image_url

        if isinstance(job_titles, str):
            job_titles = [job_titles]

        self.job_titles = job_titles
        self.description = description
        self.birth_date = birth_date

        self.known_for_titles = known_for_titles
        self.filmography_titles = filmography_titles


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_dict(
        cls,
        d: dict,
        known_for_titles: List[ImagedTitle],
        filmography_titles: List[ImagedTitle]
    ):
        return cls(
            id=d['url'].strip('/').split('/')[1],
            name=d['name'],
            image_url=d['image'],
            job_titles=cls._d_val(d, 'jobTitle'),
            description=cls._d_val(d, 'description'),
            birth_date=cls._d_val(d, 'birthDate'),
            known_for_titles=known_for_titles,
            filmography_titles=filmography_titles
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #
