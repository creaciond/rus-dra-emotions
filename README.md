# Evaluating Sentiment in Russian Drama
Course paper for the 2019/20 academic year at DH Masters, HSE.

## About
The ultimate goal of this paper is to analyse whether any sentiment analysis is applicable to Russian Drama Corpus. Apart from problems of sentiment analysis as a task itself, there also are several issues when trying to apply it to dramatic text. With this research, I want to find out whether it would make any sense at all to use some of the popular instruments with Russian drama.

I'm going to test several approaches and answer the following questions:

1) how different lexicons will perform on our material?

2) if we ask people to perform manual annotation, how different would it be?

3) how difficult will it be to design a machine learning model to get what we need?

## Contents

|**Content**|**File(s)**|**Additional**|
|:---------:|:---------:|:------------:|
|downloading data for the experiments|[get_data.py](./get_data.py), [preprocessing.py](./preprocessing.py)|thanks DraCor API!|
|experiment 1: Russian WordNet package for Python|[wiki_ru_wordnet.ipynb](./wiki_ru_wordnet.ipynb)||
|experiment 2: out-of-the-box solution, dostoyevsky|[dostoyevsky.ipynb](./dostoyevsky.ipynb)||
|preparing experiment 3: using sentiment lexicons for Russian to parse plays|[extract_sentiment_from_plays.py](./extract_sentiment_from_plays.py)||
|experiment 3: analyzing performance of various Russian lexicons of different origins|[lexicons.ipynb](./lexicons.ipynb)||

## Literature

to upload later :)
