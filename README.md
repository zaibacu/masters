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
`cat test_text.txt | python word_getter.py | python bow.py -f data/test.dict.txt`

Training
========
`vw data/comments.train.data -l 10 -c --passes 25 --holdout_off -f data/comments.model`

Prediction
==========
`vw data/comments.data -p pred.txt --quiet`