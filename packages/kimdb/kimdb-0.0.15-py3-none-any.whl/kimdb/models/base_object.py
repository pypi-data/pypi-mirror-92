# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Hashable
from abc import abstractclassmethod

# Pip
from jsoncodable import JSONCodable
from kcu import kjson

# Local
from .urls import URLs
from .enums import EntryType

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: BaseObject ---------------------------------------------------------- #

class BaseObject(JSONCodable):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        id: str
    ):
        self.id = id
        self.type = EntryType.from_id(id)


    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    @property
    def url(self) -> str:
        return URLs.keyed_url(self.type.url_key, self.id)


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @staticmethod
    def _d_val(d: dict, key: Hashable, def_val: Optional[any] = None) -> Optional[any]:
        return kjson.get_value(d, key=key, default_value=def_val)


# ---------------------------------------------------------------------------------------------------------------------------------------- #
