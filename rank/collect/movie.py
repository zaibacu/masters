def get_comments(title: str) -> list:
    from rank.collect.source.lm import LMSource
    from rank.collect.source.torrent_lt import TorrentLtSource
    import os
    lm = LMSource()
    lm.auth(os.getenv("lm_user"), os.getenv("lm_pass"))
    torrent_lt = TorrentLtSource()
    torrent_lt.auth(os.getenv("torrentlt_user"), os.getenv("torrentlt_pass"))

    lm_comments = [comment for comment in lm.search(title)]
    torrentlt_comments = [comment for comment in torrent_lt.search(title)]
    return lm_comments + torrentlt_comments
