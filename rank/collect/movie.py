def get_comments(title: str, data: dict = None) -> list:
    from rank.collect.source.lm import LMSource
    from rank.collect.source.torrent_lt import TorrentLtSource
    from rank.collect.source.filmai_in import FilmaiInSource
    import os
    lm = LMSource()

    def get_param(key):
        if data and key in data:
            return data[key]
        else:
            return os.getenv(key)

    lm.auth(get_param("lm_user"), get_param("lm_pass"))
    torrent_lt = TorrentLtSource()
    torrent_lt.auth(get_param("torrentlt_user"), get_param("torrentlt_pass"))
    filmai_in = FilmaiInSource()

    try:
        lm_comments = [comment for comment in lm.search(title)]
    except:
        lm_comments = []

    try:
        torrent_lt_comments = [comment for comment in torrent_lt.search(title)]
    except:
        torrent_lt_comments = []

    try:
        filmai_in_comments = [comment for comment in filmai_in.search(title)]
    except:
        filmai_in_comments = []
    return lm_comments + torrent_lt_comments + filmai_in_comments
