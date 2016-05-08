About
=====
Various tools joined together to make Audience rank algorithm

Usage
=====
```bash
cat data.txt | python filter.py | python rank.py > results.txt
```

Creating dict
=============
`cat test_text.txt | python word_getter.py | python word_counter.py | python group_levenshtein.py > data/test.dict.txt`

Creating BOW
============
`cat test_text.txt | sh iter.sh "sh bow_pipe.sh"`

Training
========
`vw data/comments.train.data -l 10 -c --passes 25 --holdout_off -f data/model.vw`

Prediction
==========
`vw -t -i data/model.vw data/comments.data -p pred.txt --quiet`

Starting API
============
`gunicorn api:api --bind localhost:8080 --worker-class aiohttp.worker.GunicornWebWorker`