def get_comments(title: str) -> list:
    from rank.collect.source.lm import LMSource
    import sys
    lm = LMSource()
    lm.auth(sys.env("lm_user"), sys.env("lm_pass"))
    return [comment for comment in lm.search(title)]
