# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional

# Local
from .base_object import BaseObject

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Video ------------------------------------------------------------- #

class Video(BaseObject):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        id: str,
        name: Optional[str],
        description: Optional[str],
        thumbnail_url: Optional[str]
    ):
        super().__init__(id)

        self.name = name
        self.description = description
        self.thumbnail_url = thumbnail_url


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def from_dict(
        cls,
        d: dict
    ):
        return cls(
            d['embedUrl'].strip('/').split('/')[-1],
            d['name'] if 'name' in d else None,
            d['description'] if 'description' in d else None,
            d['thumbnailUrl'] if 'thumbnailUrl' in d else None
        )


# ---------------------------------------------------------------------------------------------------------------------------------------- #
