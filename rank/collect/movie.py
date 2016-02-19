def get_comments(title: str) -> list:
    from rank.collect.source.lm import LMSource
    import os
    lm = LMSource()
    lm.auth(os.getenv("lm_user"), os.getenv("lm_pass"))
    return [comment for comment in lm.search(title)]
