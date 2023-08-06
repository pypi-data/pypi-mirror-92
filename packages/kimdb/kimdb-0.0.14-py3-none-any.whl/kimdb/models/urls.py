# -------------------------------------------------------------- class: Urls ------------------------------------------------------------- #

class URLs:

    # ------------------------------------------------------ Public properties ------------------------------------------------------- #

    HOME = 'https://www.imdb.com'
    CHART = '{}/chart'.format(HOME)

    TOP_250_MOVIES = '{}/top'.format(CHART)
    TOP_250_SERIES = '{}/toptv'.format(CHART)

    MOST_POPULAR_100_MOVIES = '{}/moviemeter'.format(CHART)
    MOST_POPULAR_100_SERIES = '{}/tvmeter'.format(CHART)

    TITLE = '{}/title'.format(HOME)
    LIST = '{}/list'.format(HOME)
    USER = '{}/user'.format(HOME)
    NAME = '{}/name'.format(HOME)


    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def title(cls, id: str) -> str:
        return '{}/{}'.format(cls.TITLE, id)

    @classmethod
    def list(cls, id: str) -> str:
        return '{}/{}'.format(cls.LIST, id)

    @classmethod
    def user(cls, id: str) -> str:
        return '{}/{}'.format(cls.USER, id)

    @classmethod
    def name(cls, id: str) -> str:
        return '{}/{}'.format(cls.NAME, id)

    @classmethod
    def keyed_url(cls, key: str, id: str) -> str:
        return '{}/{}/{}'.format(cls.HOME, key, id)


# ---------------------------------------------------------------------------------------------------------------------------------------- #
