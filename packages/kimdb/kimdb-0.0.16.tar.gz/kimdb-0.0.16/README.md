# kimdb

![PyPI - version](https://img.shields.io/pypi/v/kimdb?style=flat-square)
![PyPI - license](https://img.shields.io/pypi/l/kimdb?label=package%20license&style=flat-square)
![PyPI - python version](https://img.shields.io/pypi/pyversions/kimdb?logo=pypi&style=flat-square)
![PyPI - downloads](https://img.shields.io/pypi/dm/kimdb?logo=pypi&style=flat-square)

![GitHub - last commit](https://img.shields.io/github/last-commit/kkristof200/py_imdb?style=flat-square)
![GitHub - commit activity](https://img.shields.io/github/commit-activity/m/kkristof200/py_imdb?style=flat-square) 

![GitHub - code size in bytes](https://img.shields.io/github/languages/code-size/kkristof200/py_imdb?style=flat-square)
![GitHub - repo size](https://img.shields.io/github/repo-size/kkristof200/py_imdb?style=flat-square)
![GitHub - lines of code](https://img.shields.io/tokei/lines/github/kkristof200/py_imdb?style=flat-square)

![GitHub - license](https://img.shields.io/github/license/kkristof200/py_imdb?label=repo%20license&style=flat-square)

## Description

IMDB scraper

## Install

~~~~bash
pip install kimdb
# or
pip3 install kimdb
~~~~

## Usage

~~~~python
from kimdb import IMDB

imdb = IMDB(debug=True)

top_movies = imdb.top_movies()
top_movies[0].jsonprint()

top_series = imdb.top_series()
top_series[0].jsonprint()

most_popular_movies = imdb.most_popular_movies()
most_popular_movies[0].jsonprint()

most_popular_series = imdb.most_popular_movies()
most_popular_series[0].jsonprint()

title = imdb.get_title(top_movies[0].id)
title.jsonprint()

list = imdb.get_list(title.lists[0].id)
list.jsonprint()

user = imdb.get_user(list.owner.id)
user.jsonprint()

name = imdb.get_name(title.actors[0].id)
name.jsonprint()
~~~~ 

## Dependencies

[beautifulsoup4](https://pypi.org/project/beautifulsoup4), [jsoncodable](https://pypi.org/project/jsoncodable), [kcu](https://pypi.org/project/kcu), [ksimpleapi](https://pypi.org/project/ksimpleapi), [noraise](https://pypi.org/project/noraise), [requests](https://pypi.org/project/requests)