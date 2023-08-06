# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Dict, List, Union

# Pip
from ksimpleapi import Api

# Local
from .models import *
from ._parser import Parser

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: IMDB -------------------------------------------------------------- #

class IMDB(Api):

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        user_agent: Optional[Union[str, List[str]]] = None,
        proxy: Optional[Union[str, List[str]]] = None,
        keep_cookies: bool = False,
        default_cookies: Optional[Dict[str, Dict[str, str]]] = None,
        cookies_file_path: Optional[str] = None,
        store_pickled_cookies: bool = False,
        max_request_try_count: int = 1,
        sleep_s_between_failed_requests: Optional[float] = 0.5,
        debug: bool = False
    ):
        super().__init__(
            user_agent=user_agent,
            proxy=proxy,
            keep_cookies=keep_cookies,
            default_cookies=default_cookies,
            cookies_file_path=cookies_file_path,
            store_pickled_cookies=store_pickled_cookies,
            max_request_try_count=max_request_try_count,
            sleep_s_between_failed_requests=sleep_s_between_failed_requests,
            extra_headers= {
                'Host': 'www.imdb.com',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
            },
            debug=debug
        )

        self.parser = Parser(debug=debug)


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    def top_movies(
        self,
        excluded_ids: Optional[List[str]] = None
    ) -> List[BaseTitle]:
        try:
            return [t for t in self.parser.parse_chart(self._get(URLs.TOP_250_MOVIES)) if not excluded_ids or t.id not in excluded_ids]
        except Exception as e:
            if self.debug:
                print(e)

            return []

    def top_series(
        self,
        excluded_ids: Optional[List[str]] = None
    ) -> List[BaseTitle]:
        try:
            return [t for t in self.parser.parse_chart(self._get(URLs.TOP_250_SERIES)) if not excluded_ids or t.id not in excluded_ids]
        except Exception as e:
            if self.debug:
                print(e)

            return []

    def most_popular_movies(
        self,
        excluded_ids: Optional[List[str]] = None
    ) -> List[BaseTitle]:
        try:
            return [t for t in self.parser.parse_chart(self._get(URLs.MOST_POPULAR_100_MOVIES)) if not excluded_ids or t.id not in excluded_ids]
        except Exception as e:
            if self.debug:
                print(e)

            return []

    def most_popular_series(
        self,
        excluded_ids: Optional[List[str]] = None
    ) -> List[BaseTitle]:
        try:
            return [t for t in self.parser.parse_chart(self._get(URLs.MOST_POPULAR_100_SERIES)) if not excluded_ids or t.id not in excluded_ids]
        except Exception as e:
            if self.debug:
                print(e)

            return []

    def get_title(
        self,
        id: str
    ) -> Optional[Title]:
        return self.parser.parse_title(self._get(URLs.title(id)))

    def get_user(
        self,
        id: str
    ) -> Optional:
        return self.parser.parse_user(self._get(URLs.user(id)))

    def get_name(
        self,
        id: str
    ) -> Optional:
        return self.parser.parse_name(self._get(URLs.name(id)))

    def get_list(
        self,
        id: str
    ) -> Optional:
        return self.parser.parse_list(self._get(URLs.list(id)))


# ---------------------------------------------------------------------------------------------------------------------------------------- #
