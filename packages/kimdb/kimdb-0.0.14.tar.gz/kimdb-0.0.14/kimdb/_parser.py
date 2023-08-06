# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, List
from requests import Response
import json

# Pip
from bs4 import BeautifulSoup as bs
from kcu import strings
from noraise import noraise

# Local
from .models import *

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------- class: Parser ------------------------------------------------------------ #

class Parser:

    # ------------------------------------------------------------- Init ------------------------------------------------------------- #

    def __init__(
        self,
        debug: bool = False
    ):
        self.debug = debug


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @noraise()
    def parse_title(self, response: Optional[Response]) -> Optional[Title]:
        soup = bs(response.text, 'lxml')

        related_title_as = [img.parent for img in soup.find_all('img', class_='loadlate hidden rec_poster_img')]
        _related_title_ids = []
        related_titles = []

        for related_title_a in related_title_as:
            related_title = self.__parse_related_title(related_title_a)

            if related_title and related_title.id not in _related_title_ids:
                _related_title_ids.append(related_title.id)
                related_titles.append(related_title)

        lists = [self.__parse_base_list(e.find('a')) for e in soup.find_all('div', class_='list_name')]

        return Title.from_dict(
            d=self.__extract_json(response),
            related_titles=related_titles,
            lists=[l for l in lists if l]
        )

    @noraise()
    def parse_name(self, response: Optional[Response]) -> Optional[Name]:
        soup = bs(response.text, 'lxml')

        return Name.from_dict(
            d=self.__extract_json(response),
            known_for_titles=[self.__parse_known_for_title(e) for e in soup.find_all('img', class_='wtw-option')],
            filmography_titles=[self.__parse_filmography_title(a) for a in soup.find('div', id='filmography').find_all('a') if a.has_attr('href') and a['href'].startswith('/title/') and not (a.parent.has_attr('class') and a.parent['class'] == 'filmo-episodes')]
        )

    @noraise()
    def parse_chart(self, response: Optional[Response]) -> Optional[List[ImagedTitle]]:
        soup = bs(response.text, 'lxml')

        return [self.__parse_chart_list_title(td.find('a')) for td in soup.find_all('td', class_='posterColumn')]

    @noraise()
    def parse_list(self, response: Optional[Response]) -> Optional[TitleList]:
        soup = bs(response.text, 'lxml')
        user_a = soup.find('span', id='list-overview-summary').find('a')

        return TitleList(
            id=soup.find('meta', property='pageId')['content'],
            name=soup.find('meta', {'name':'description'})['content'],
            owner=BaseUser(
                id=user_a['href'].strip('/').split('/')[1],
                username=user_a.text.strip()
            ),
            titles=[self.__parse_chart_list_title(e.parent) for e in soup.find_all('img', class_='loadlate')]
        )

    @noraise()
    def parse_user(self, response: Optional[Response]) -> Optional[User]:
        soup = bs(response.text, 'lxml')
        profile = soup.find('div', class_='user-profile userId')

        return User(
            id=profile['data-userid' if profile.has_attr('data-userid') else 'data-userId'],
            username=profile.find('h1').text.strip(),
            lists=[self.__parse_base_list(e) for e in soup.find_all('a', class_="list-name")]
        )


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @noraise()
    def __parse_related_title(self, element) -> Optional[ImagedTitle]:
        img = element.find('img')

        return ImagedTitle(
            id=element['href'].strip('/').split('/')[1],
            title=img['title'],
            poster_url=self.__normalize_url(img['loadlate']),
        )

    @noraise()
    def __parse_known_for_title(self, element) -> Optional[ImagedTitle]:
        return ImagedTitle(
            id=element['data-tconst'],
            title=element['title'],
            poster_url=self.__normalize_url(element['src']),
        )

    @noraise()
    def __parse_filmography_title(self, element) -> Optional[BaseTitle]:
        return BaseTitle(
            id=element['href'].strip('/').split('/')[1],
            title=element.text.strip()
        )

    @noraise()
    def __parse_chart_list_title(self, element) -> Optional[ImagedTitle]:
        img = element.find('img')

        return ImagedTitle(
            id=element['href'].strip('/').split('/')[1],
            title=img['alt'],
            poster_url=self.__normalize_url(img['src']),
        )

    @noraise()
    def __parse_base_list(self, element) -> Optional[BaseList]:
        return BaseList(
            id=element['href'].strip('/').split('/')[1],
            name=element.text.strip()
        )

    @noraise()
    def __extract_json(self, response: Optional[Response]) -> Optional[dict]:
        return json.loads(strings.between(response.text, '<script type="application/ld+json">', '</script>').strip())

    @staticmethod
    def __normalize_url(url: str) -> str:
        return url.split('_V1_')[0] + '_V1_.jpg'


# ---------------------------------------------------------------------------------------------------------------------------------------- #
