def get_comments(title: str) -> list:
    from rank.collect.source.lm import LMSource
    from rank.collect.source.torrent_lt import TorrentLtSource
    from rank.collect.source.filmai_in import FilmaiInSource
    import os
    lm = LMSource()
    lm.auth(os.getenv("lm_user"), os.getenv("lm_pass"))
    torrent_lt = TorrentLtSource()
    torrent_lt.auth(os.getenv("torrentlt_user"), os.getenv("torrentlt_pass"))
    filmai_in = FilmaiInSource()

    lm_comments = [comment for comment in lm.search(title)]
    torrent_lt_comments = [comment for comment in torrent_lt.search(title)]
    filmai_in_comments = [comment for comment in filmai_in.search(title)]
    return lm_comments + torrent_lt_comments + filmai_in_comments
